"""Generate the compact native n8n workflow and optional validation input."""
import argparse
import ast
import json
from pathlib import Path
import subprocess

ROOT = Path(__file__).parent
parser = argparse.ArgumentParser()
parser.add_argument('--validation-output', type=Path)
args = parser.parse_args()
ast.parse((ROOT / 'job-command.py').read_text())
COMMAND = '/usr/bin/python3 /opt/pdf-cleanup/job-command.py '
SSH = {'sshPrivateKey': {'id': 'OsTkP0IAXod5QjbI', 'name': 'SSH - n8n core edge AI execution'}}
NC = {'nextCloudApi': {'id': '6MEdI2Cs7tEUiM7o', 'name': 'Nextcloud - operator automation'}}
POSITIONS = {
    'Subworkflow Input': [0, 0], 'Normalize Request': [224, 0], 'Each PDF': [448, 0],
    'Download Original Snapshot': [672, 240], 'Create Temporary Job': [896, 240],
    'Capture Job': [1120, 240], 'Upload Working Copy': [1344, 240],
    'Run PDF Cleanup CLI': [672, 576], 'CLI Succeeded': [896, 576],
    'Download Cleaned PDF': [1120, 480], 'Publish Cleaned PDF': [1344, 480],
    'Previous Cleaned Filename': [1568, 480], 'Remove Previous Cleaned PDF': [1792, 384],
    'Remove Temporary Job': [2016, 672], 'Read Cleanup INDEX': [672, 960],
    'Return Result': [896, 960], 'Save Cleanup INDEX': [1120, 960],
}
nodes = []


def add(var, name, typ, parameters, version=1, credentials=None, error=False, sample=None):
    config = {'name': name, 'parameters': parameters, 'position': POSITIONS[name]}
    if credentials:
        config['credentials'] = credentials
    if error:
        config['onError'] = 'continueRegularOutput'
    nodes.append((var, {'type': 'n8n-nodes-base.' + typ, 'version': version,
                        'config': config, 'output': [sample or {}]}))


def code(var, name, source, sample=None):
    subprocess.run(['node', '--check'], input='async function check(){\n' + source + '\n}',
                   text=True, check=True, capture_output=True)
    add(var, name, 'code', {'mode': 'runOnceForAllItems', 'jsCode': source}, 2, sample=sample)


def ssh(var, name, parameters):
    add(var, name, 'ssh', {'authentication': 'privateKey', **parameters}, credentials=SSH,
        error=True, sample={'code': 0, 'stdout': '{}', 'success': True})


def http(var, name, method, url, extra=None, file=False, response_format=None, stop=False):
    parameters = {'authentication': 'predefinedCredentialType', 'nodeCredentialType': 'nextCloudApi',
                  'method': method, 'url': url, 'options': {'timeout': 120000,
                  'response': {'response': {'responseFormat': response_format or ('file' if file else 'text'),
                  'fullResponse': True, 'neverError': not (file or stop),
                  **({'outputPropertyName': 'data'} if file else {})}}}}
    if extra:
        parameters.update(extra)
    add(var, name, 'httpRequest', parameters, 4.4, NC, error=not (file or stop),
        sample={'statusCode': 200, 'error': None, 'headers': {'etag': '"example-etag"'}})


def branch(var, name, expression):
    add(var, name, 'if', {'conditions': {'options': {'caseSensitive': True,
        'typeValidation': 'strict', 'version': 2}, 'conditions': [{'leftValue': expression,
        'rightValue': True, 'operator': {'type': 'boolean', 'operation': 'equals'}}],
        'combinator': 'and'}}, 2.2)


sample_request = {'path': '', 'filename': '', 'execution_id': '1',
    'previous_path': None, 'previous_cleaned_url': None,
    'original_path': '', 'cleaned_path': '', 'original_url': '', 'cleaned_url': ''}

add('subflow', 'Subworkflow Input', 'executeWorkflowTrigger', {
    'inputSource': 'workflowInputs', 'workflowInputs': {'values': [
        {'name': 'files', 'type': 'array'}]}}, 1.1)
code('normalize', 'Normalize Request', r'''
const validate = path => {
  if (typeof path !== 'string' || !path.toLowerCase().endsWith('.pdf') ||
      /[\\\x00-\x1f]/.test(path) || path.split('/').some(part=>!part || part==='.' || part==='..') ||
      path.split('/').pop()==='.pdf')
    throw new Error('path must be a relative PDF path inside originals');
  return path;
};
return $input.all().flatMap((item,index) => {
const inputs = item.json.files ?? [item.json];
if (!Array.isArray(inputs) || !inputs.length) throw new Error('files must be a non-empty array of relative PDF paths');
return inputs.map(input => {
const path = validate(input.path);
const previousPath = input.previous_path ? validate(input.previous_path) : null;
if (previousPath && (previousPath===path || previousPath.split('/').slice(0,-1).join('/')!==path.split('/').slice(0,-1).join('/')))
  throw new Error('previous_path must name a different PDF in the same folder');
const filename = path.split('/').pop();
if (input.mode !== undefined && input.mode !== 'cleanup')
  throw new Error('Only cleanup is supported; use the standalone CLI for dry-run');
const originalPath = '/technical-documentation/lenovo/originals/' + path;
const cleanedPath = '/technical-documentation/lenovo/cleaned/' + path;
const dav = 'http://nextcloud.edge.internal/remote.php/webdav';
const url = path => dav + path.split('/').map(encodeURIComponent).join('/');
return {json:{path, filename, previous_path:previousPath,
  original_path:originalPath, cleaned_path:cleanedPath,
  original_url:url(originalPath), cleaned_url:url(cleanedPath),
  previous_cleaned_url:previousPath ? url('/technical-documentation/lenovo/cleaned/'+previousPath) : null,
  execution_id:String($execution.id)},pairedItem:{item:index}};
});
});
''', sample_request)
add('each', 'Each PDF', 'splitInBatches', {'batchSize': 1, 'options': {}}, 3)
http('download', 'Download Original Snapshot', 'GET', '={{ $json.original_url }}', file=True)
ssh('createJob', 'Create Temporary Job', {'resource': 'command', 'operation': 'execute', 'cwd': '/tmp',
    'command': '={{ ' + json.dumps(COMMAND) + " + JSON.stringify({action:'create',"
    "execution_id:$('Normalize Request').item.json.execution_id}).base64Encode() }}"})
code('captureJob', 'Capture Job', r'''
const response = $input.first().json;
const job = JSON.parse(response.stdout ?? '{}');
if (response.code !== 0 || job.ok !== true) throw new Error(job.error ?? response.error ?? 'Job creation failed');
return [{json:{...$('Normalize Request').item.json, ...job},
  binary:$('Download Original Snapshot').item.binary}];
''', {**sample_request, 'job_dir': '/tmp/pdf-cleanup-example1'})
ssh('upload', 'Upload Working Copy', {'resource': 'file', 'operation': 'upload',
    'binaryPropertyName': 'data', 'path': "={{ $json.job_dir + '/input' }}", 'options': {'fileName': 'source.pdf'}})
ssh('run', 'Run PDF Cleanup CLI', {'resource': 'command', 'operation': 'execute', 'cwd': '/tmp',
    'command': '={{ ' + json.dumps(COMMAND) + " + JSON.stringify({action:'process',"
    "job_dir:$('Capture Job').item.json.job_dir, execution_id:$('Capture Job').item.json.execution_id,"
    "upload_ok:$json.success === true}).base64Encode() }}"})
branch('cliValid', 'CLI Succeeded', r'''={{ (() => {
  try { return $json.code === 0 && JSON.parse($json.stdout).ok === true; }
  catch { return false; }
})() }}''')
ssh('downloadOutput', 'Download Cleaned PDF', {'resource': 'file', 'operation': 'download',
    'path': "={{ $('Capture Job').item.json.job_dir + '/output/cleaned.pdf' }}",
    'binaryPropertyName': 'cleaned', 'options': {'fileName': "={{ $('Capture Job').item.json.filename }}"}})
http('publishPdf', 'Publish Cleaned PDF', 'PUT', "={{ $('Capture Job').item.json.cleaned_url }}", {
    'sendBody': True, 'contentType': 'binaryData', 'inputDataFieldName': 'cleaned'})
branch('previousCleaned', 'Previous Cleaned Filename',
       "={{ Boolean($('Capture Job').item.json.previous_path) && !$json.error && [200,201,204].includes($json.statusCode) }}")
http('deletePrevious', 'Remove Previous Cleaned PDF', 'DELETE',
     "={{ $('Capture Job').item.json.previous_cleaned_url }}")
ssh('release', 'Remove Temporary Job', {'resource': 'command', 'operation': 'execute', 'cwd': '/tmp',
    'command': '={{ ' + json.dumps(COMMAND) + " + JSON.stringify({action:'release',"
    "job_dir:$('Capture Job').item.json.job_dir, execution_id:$('Capture Job').item.json.execution_id}).base64Encode() }}"})
http('readIndex', 'Read Cleanup INDEX', 'GET',
     'http://nextcloud.edge.internal/remote.php/webdav/technical-documentation/lenovo/originals/INDEX.html', stop=True)
code('returned', 'Return Result', r'''
const ctx = $('Capture Job').item.json;
const response = $('Remove Temporary Job').item.json;
let released;
try { released = JSON.parse(response.stdout); } catch { released = {}; }
if (response.code !== 0 || released.ok !== true)
  throw new Error('Temporary job removal failed: ' + (released.error ?? response.error ?? 'SSH failure'));
const processResponse = $('Run PDF Cleanup CLI').item.json;
let processed;
try { processed = JSON.parse(processResponse.stdout); } catch { processed = {}; }
if (processResponse.code !== 0 || processed.ok !== true)
  throw new Error(processed.error ?? processResponse.error ?? 'PDF cleanup CLI failed');
const pdf = $('Publish Cleaned PDF').item.json;
if (pdf.error || ![200,201,204].includes(pdf.statusCode))
  throw new Error('Cleaned PDF upload failed: ' + JSON.stringify(pdf.error ?? pdf.statusCode));
if (ctx.previous_path) {
  const deletion = $('Remove Previous Cleaned PDF').item.json;
  if (deletion.error || ![200,204,404].includes(deletion.statusCode))
    throw new Error('Previous cleaned PDF deletion failed: '+JSON.stringify(deletion.error ?? deletion.statusCode));
}
let html = $input.first().json.data;
const pattern = /(<script id="catalog-data" type="application\/json">)([\s\S]*?)(<\/script>)/;
const catalog = JSON.parse(html.match(pattern)[2]);
const cleanedAt = $now.toISO();
const document = catalog.documents.find(doc=>doc.path===ctx.path);
if (document) {
  document.cleanup_status = 'cleaned';
  document.cleaned_at = cleanedAt;
  document.cleaned_path = ctx.path;
  catalog.generated_at = cleanedAt;
  html = html.replace(pattern,(_,a,b,c)=>a+JSON.stringify(catalog,null,2).replace(/</g,'\\u003c')+c);
}
return [{json:{ok:true,status:'cleaned',path:ctx.path,original_path:ctx.original_path,cleaned_path:ctx.cleaned_path,
  cleaned_at:cleanedAt,summary:processed.summary,temporary_job_removed:true,html}}];
''', {'ok': True, 'status': 'cleaned', 'temporary_job_removed': True, 'html': '<!doctype html>'})
http('saveIndex', 'Save Cleanup INDEX', 'PUT',
     'http://nextcloud.edge.internal/remote.php/webdav/technical-documentation/lenovo/originals/INDEX.html',
     {'sendBody': True, 'contentType': 'raw', 'rawContentType': 'text/html; charset=utf-8', 'body': '={{ $json.html }}'},
     response_format='autodetect', stop=True)


def sdk_value(value):
    if isinstance(value, str) and value.startswith('={{'):
        return 'expr(' + json.dumps(value[1:]) + ')'
    if isinstance(value, dict):
        return '{' + ','.join(json.dumps(k) + ':' + sdk_value(v) for k, v in value.items()) + '}'
    if isinstance(value, list):
        return '[' + ','.join(sdk_value(v) for v in value) + ']'
    return json.dumps(value, ensure_ascii=False)


builder = ["import { workflow, node, trigger, ifElse, splitInBatches, nextBatch, expr } from '@n8n/workflow-sdk';"]
for var, obj in nodes:
    factory = 'trigger' if var == 'subflow' else 'splitInBatches' if var == 'each' else 'ifElse' if obj['type'].endswith('.if') else 'node'
    if var == 'each':
        obj = {k: v for k, v in obj.items() if k != 'type'}
    builder.append(f'const {var} = {factory}({sdk_value(obj)});')
builder.append("""
export default workflow('lenovo-pdf-cleanup', 'LenovoPdfCleanup')
 .add(subflow).to(normalize)
 .to(each.onEachBatch(download.to(createJob).to(captureJob).to(upload).to(run)
   .to(cliValid.onTrue(downloadOutput.to(publishPdf).to(previousCleaned.onTrue(deletePrevious.to(release)).onFalse(release))).onFalse(release))))
 .add(release).to(readIndex).to(returned).to(saveIndex).to(nextBatch(each));
""")
(ROOT / 'LenovoPdfCleanup01.ts').write_text('\n'.join(builder))
if args.validation_output:
    args.validation_output.write_text(json.dumps([
        {'name': obj['config']['name'], 'type': obj.get('type', 'n8n-nodes-base.splitInBatches'), 'typeVersion': obj['version'],
         'parameters': obj['config']['parameters']} for _, obj in nodes], indent=2) + '\n')
subprocess.run(['bash', '-n'], input=COMMAND + 'e30=', text=True, check=True)
print(f'Generated {len(nodes)} nodes; Python, JavaScript and SSH command syntax checked')
