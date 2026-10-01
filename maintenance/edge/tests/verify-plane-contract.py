#!/usr/bin/env python3
"""Read-only checks of native merged Compose and update topology drift gates."""
import copy
import pathlib
import runpy

root = pathlib.Path(__file__).resolve().parents[1]
module = runpy.run_path(root / 'scripts/update-plane')
config = module['config']()
validate = module['validate_topology']
signature = module['topology_signature']
validate(config)
assert signature(config) == signature(copy.deepcopy(config))
for description, change in (
    ('extra public service', lambda d: d['services'].update({'new-public': {}})),
    ('missing routed service', lambda d: d['services'].pop('live')),
    ('changed internal port', lambda d: d['services']['api']['ports'][0].update(target=9001)),
    ('public bind', lambda d: d['services']['web']['ports'][0].update(host_ip='0.0.0.0')),
    ('changed upload bucket', lambda d: d['services']['api']['environment'].update(AWS_S3_BUCKET_NAME='new-bucket')),
    ('extra integration member', lambda d: d['services']['beat-worker']['networks'].update(edge_internal={})),
    ('embedded database dependency', lambda d: d['services']['api']['depends_on'].update({'plane-db': {}})),
):
    candidate = copy.deepcopy(config); change(candidate)
    try:
        validate(candidate)
    except RuntimeError:
        pass
    else:
        raise AssertionError('drift accepted: ' + description)
# Reset/override must not hide a vendor-only dependency change from the
# separate unmerged graph comparison made in update-plane.preflight.
candidate = copy.deepcopy(config)
candidate['services']['worker']['depends_on']['new-worker-dependency'] = {}
assert signature(config) != signature(candidate)
assert 'pgdata' not in config.get('volumes', {})
assert module['PERSISTENT'] == set(config['services']) - {'migrator'}
print('PLANE_NATIVE_COMPOSE_CONTRACT=PASS|DRIFT_CASES=8|SECRETS_PRINTED=0')
