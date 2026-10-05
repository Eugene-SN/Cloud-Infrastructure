"""Preserve corrected repeat evidence without replacing the quality series."""
import datetime
import hashlib
import json
import shutil
import sys
from pathlib import Path

root = Path(sys.argv[1]).resolve()
artifact = Path(__file__).resolve().parent
manifest = json.loads((artifact / 'manifest.json').read_text())
evidence_path = artifact / 'evidence.json'
evidence = json.loads(evidence_path.read_text())
records = [json.loads(path.read_text()) for path in (root / 'out/results').glob('*.json')]
assert len(records) == len(manifest['unique_documents']) == 49
assert {row['sha256'] for row in records} == {row['sha256'] for row in manifest['unique_documents']}
for row in records:
    assert row['status'] == 'passed', row['path']
    assert row['candidate_hashes'] == evidence['candidate_hashes']
    assert row['result']['validation'] == 'passed'
    assert row['source_sha256_after'] == row['sha256']
    assert row['second_pass']['status'] == 'no_targets' and not row['second_pass']['targets']
    if row['result']['cleanup_method'] == 'exact_copy':
        assert row['native_evidence_origin'] == 'verified_identical_bytes'
        assert row['result']['input_sha256'] == row['result']['output_sha256']
    else:
        assert row['native_evidence_origin'] == 'written_stage_inspected_by_output_validator'
        assert row['inspected_stage_sha256'] == row['result']['output_sha256']
assert sum(row['result']['pages'] for row in records) == 6398
for name, row in evidence['base_and_candidate_files'].items():
    assert hashlib.sha256((root / 'candidate' / name).read_bytes()).hexdigest() == row['candidate_sha256']

destination = artifact / 'repeat-results'
destination.mkdir(exist_ok=True)
for path in (root / 'out/results').glob('*.json'):
    shutil.copyfile(path, destination / path.name)
for index in range(2):
    shutil.copyfile(root / f'repeat-{index}.log', artifact / 'logs' / f'repeat-{index}.log')

evidence['status'] = 'passed'
evidence['first_series_second_pass_status'] = 'superseded: source native evidence used by the original harness'
evidence['second_detection_targets'] = 0
evidence['second_detection_check'] = {
    'status': 'passed',
    'documents': 49,
    'pages': 6398,
    'native_evidence_origin': 'actual validated written stage, or verified identical input/output bytes',
    'candidate_source_identical_to_quality_series': True,
    'result_directory': 'repeat-results',
    'recorded_at': datetime.datetime.now(datetime.timezone.utc).isoformat(),
}
evidence['temporary_artifact_cleanup']['repeat_check_status'] = 'evidence_preserved_cleanup_pending'
evidence_path.write_text(json.dumps(evidence, ensure_ascii=False, indent=2) + '\n')
print(json.dumps(evidence['second_detection_check'], ensure_ascii=False))
