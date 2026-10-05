"""Build the native n8n documentation monitor; no host runtime service."""
import json
import argparse
import subprocess
from pathlib import Path

ROOT = Path(__file__).parent
parser = argparse.ArgumentParser()
parser.add_argument('--validation-output', type=Path)
args = parser.parse_args()
POSITIONS = {'Daily 07:00': [0, 0], 'Manual Start': [0, 160], 'Read INDEX': [220, 0], 'Models and Index': [440, 0], 'Read Lenovo ASP': [660, 0], 'Latest Document Families': [880, 0], 'Read Remote Version': [1100, 0], 'Changed Documents': [1320, 0], 'Each Changed PDF': [0, 440], 'Download PDF': [220, 440], 'Save Original': [440, 440], 'Filename Changed': [660, 440], 'Remove Previous Filename': [880, 340], 'Saved Document': [1100, 440], 'Update INDEX': [220, 700], 'Save INDEX': [440, 700]}
nodes = []


def add(var, name, typ, parameters, version=1, auth=False, sample=None, position=None):
    config = {'name': name, 'parameters': parameters,
              'position': POSITIONS[name]}
    if auth:
        config['credentials'] = {'nextCloudApi': {
            'id': '6MEdI2Cs7tEUiM7o', 'name': 'Nextcloud - operator automation'}}
    nodes.append((var, {'type': 'n8n-nodes-base.' + typ, 'version': version,
                        'config': config, 'output': [sample or {}]}))


def code(var, name, source):
    subprocess.run(['node', '--check'], input='async function check(){\n' + source + '\n}',
                   text=True, check=True, capture_output=True)
    samples = {'models': {'model': {'fullGuid': 'example', 'folder': 'WR5220 G3'}},
               'families': {'source_url': 'https://lenovopress.lenovo.com/lp1705.pdf'},
               'changed': {'source_url': 'https://lenovopress.lenovo.com/lp1705.pdf',
                           'destination_url': 'http://nextcloud.edge.internal/remote.php/webdav/example.pdf', 'old_path': None},
               'render': {'html': '<!doctype html>', 'updated': 1, 'documents': 15}}
    add(var, name, 'code', {'mode': 'runOnceForAllItems', 'jsCode': source}, 2, sample=samples.get(var))


def http(var, name, method, url, auth=False, format='text', extra=None, never_error=False):
    params = {'method': method, 'url': url, 'options': {'timeout': 120000,
              'response': {'response': {'fullResponse': True, 'responseFormat': format,
              'neverError': never_error, **({'outputPropertyName': 'data'} if format == 'file' else {})}}}}
    if auth:
        params.update(authentication='predefinedCredentialType', nodeCredentialType='nextCloudApi')
    params.update(extra or {})
    add(var, name, 'httpRequest', params, 4.4, auth,
        {'statusCode': 200, 'headers': {'etag': '"sample"'}, 'body': {}})


add('daily', 'Daily 07:00', 'scheduleTrigger', {'rule': {'interval': [
    {'field': 'days', 'daysInterval': 1, 'triggerAtHour': 7, 'triggerAtMinute': 0}]}}, 1.4)
add('manual', 'Manual Start', 'manualTrigger', {}, position=[0, 180])
http('read', 'Read INDEX', 'GET',
     'http://nextcloud.edge.internal/remote.php/webdav/technical-documentation/lenovo/originals/INDEX.html', True)
code('models', 'Models and Index', r'''
const models = [{
  folder: 'WR5220 G3',
  fullGuid: '339E8F3F-BAD4-4F7D-BDAA-5E6C1DD8827E/E003AB30-9C7D-403E-B672-7B5EFB52C070/5D07DC93-3C2A-4986-BBB4-A04A44FAB99E',
  press: [{key:'product-guide', title:'Product Guide Lenovo Wentian WR5220 G3', url:'https://lenovopress.lenovo.com/lp1705.pdf', language:'zh'}],
  labels: {
    'lenovo_wentian_wr5220g3_user_guide': ['user-manual', 'User Manual Lenovo Wentian WR5220 G3'],
    'lenovo_wentian_os_installation_guide': ['os-installation-guide', 'OS Installation Guide Lenovo Wentian'],
    'lenovo_bmc_g3_commands_guide': ['bmc-ipmi-specification', 'IPMI Command Specification Lenovo BMC'],
    'lenovo_bmc_event_reference_guide': ['bmc-event-reference', 'Event Reference Guide Lenovo BMC'],
    'lenovo_snmp_ug_g3': ['bmc-snmp-reference', 'SNMP Reference Guide Lenovo BMC'],
    'bmc_user_guide': ['bmc-enterprise-user-guide', 'User Guide Lenovo BMC Enterprise G3'],
    'lenovo_bmc_g3_redfish_guide': ['bmc-redfish-specification', 'Redfish Interface Specification Lenovo BMC G3'],
    'lxce_bomc_cplus_ug': ['bomc-user-guide', 'User Guide Lenovo XClarity Essentials BoMC cPlus'],
    'lxce_onecli_cplus_ug': ['onecli-user-guide', 'User Guide Lenovo XClarity Essentials OneCLI cPlus'],
    'lxce_ux_cplus_ug': ['updatexpress-user-guide', 'User Guide Lenovo XClarity Essentials UpdateXpress cPlus'],
    'lxpm_wentian_ug': ['lxpm-user-guide', 'User Guide Lenovo XClarity Provisioning Manager Wentian'],
    'wr5220g3_bios_setup_spec': ['bios-setup-specification', 'BIOS Setup Specification Lenovo Wentian WR5220 G3'],
    'psu_label_matrix': ['psu-label-matrix', 'PSU Label Matrix Lenovo'],
    'vmware_code_recipe_file': ['vmware-code-recipe', 'VMware Code Recipe File']
  }
}];
return models.map(model => ({json:{model}}));
''')
http('asp', 'Read Lenovo ASP', 'GET', 'https://api.asp.atlenovo.com/asp/isg/infomartion/getUserGuide',
     format='json', extra={'sendQuery': True, 'queryParameters': {'parameters': [
         {'name': 'fullGuid', 'value': '={{ $json.model.fullGuid }}'}]}})
code('families', 'Latest Document Families', r'''
const result = [];
for (const [i, item] of $input.all().entries()) {
  const model = $('Models and Index').all()[i].json.model;
  const families = new Map();
  for (const row of item.json.body.data) {
    const filename = decodeURIComponent(row.url.split('?')[0].split('/').pop());
    let family = filename.toLowerCase().replace(/\.pdf$/, '').replace(/[_-]v\d+(?:\.\d+)*$/, '');
    if (/^lenovo_bmc_event_reference_guide_g[35]$/.test(family)) family = 'lenovo_bmc_event_reference_guide';
    const label = model.labels[family] ?? [family, row.title.trim().replace(/\s+V?\d+(?:\.\d+)*$/i, '')];
    const doc = {key:model.folder+'/'+label[0], title:label[1], folder:model.folder,
      source_title:row.title.trim(), source_updated:row.updated, source_url:row.url,
      path:model.folder+'/'+filename, language:row.isChinese ? 'zh' : 'en', source:'asp'};
    const old = families.get(doc.key);
    if (!old || doc.source_updated > old.source_updated) families.set(doc.key, doc);
  }
  for (const doc of families.values()) result.push({json:doc, pairedItem:{item:i}});
  for (const press of model.press) result.push({json:{key:model.folder+'/'+press.key,
    title:press.title, folder:model.folder, path:model.folder+'/'+press.url.split('?')[0].split('/').pop(),
    source_title:'Lenovo Press '+press.key, source_url:press.url, source_updated:null,
    language:press.language, source:'press'}, pairedItem:{item:i}});
}
return result;
''')
http('head', 'Read Remote Version', 'HEAD', '={{ $json.source_url }}')
code('changed', 'Changed Documents', r'''
const html = $('Read INDEX').first().json.data;
const catalog = JSON.parse(html.match(/<script id="catalog-data" type="application\/json">([\s\S]*?)<\/script>/)[1]);
const previous = new Map(catalog.documents.map(d => [d.key, d]));
const candidates = $('Latest Document Families').all();
const result = [];
for (const [i,item] of $input.all().entries()) {
  const doc = {...candidates[i].json};
  const h = item.json.headers;
  doc.remote_validator = {etag:h.etag ?? null, last_modified:h['last-modified'] ?? null,
    content_length:Number(h['content-length']) || null};
  if (doc.source === 'press') doc.source_updated = h['last-modified'] ? new Date(h['last-modified']).toISOString().slice(0,10) : null;
  const old = previous.get(doc.key);
  const v = old?.remote_validator;
  const sameBytes = v && (doc.remote_validator.etag && v.etag
    ? doc.remote_validator.etag === v.etag
    : doc.remote_validator.last_modified === v.last_modified && doc.remote_validator.content_length === v.content_length);
  if (old && old.source_url === doc.source_url && old.source_updated === doc.source_updated && sameBytes) continue;
  doc.title = old?.title ?? doc.title;
  doc.old_path = old?.path !== doc.path ? old?.path ?? null : null;
  const dav = 'http://nextcloud.edge.internal/remote.php/webdav/technical-documentation/lenovo/originals/';
  doc.destination_url = dav + doc.path.split('/').map(encodeURIComponent).join('/');
  doc.old_url = doc.old_path ? dav + doc.old_path.split('/').map(encodeURIComponent).join('/') : null;
  result.push({json:doc, pairedItem:{item:i}});
}
return result;
''')
add('batch', 'Each Changed PDF', 'splitInBatches', {'batchSize': 1, 'options': {}}, 3, position=[0, 420])
http('download', 'Download PDF', 'GET', '={{ $json.source_url }}', format='file')
http('upload', 'Save Original', 'PUT', "={{ $('Each Changed PDF').item.json.destination_url }}", True,
     extra={'sendBody': True, 'contentType': 'binaryData', 'inputDataFieldName': 'data'})
add('renamed', 'Filename Changed', 'if', {'conditions': {'options': {'caseSensitive': True,
    'typeValidation': 'strict'}, 'conditions': [{'leftValue': "={{ Boolean($('Each Changed PDF').item.json.old_path) }}",
    'rightValue': True, 'operator': {'type': 'boolean', 'operation': 'equals'}}], 'combinator': 'and'}}, 2.2)
http('remove', 'Remove Previous Filename', 'DELETE', "={{ $('Each Changed PDF').item.json.old_url }}", True, never_error=True)
code('receipt', 'Saved Document', r'''
const response = $input.first().json;
if (response.statusCode >= 300 && response.statusCode !== 404) throw new Error('WebDAV deletion failed: '+response.statusCode);
const doc = {...$('Each Changed PDF').item.json};
const h = $('Download PDF').item.json.headers;
doc.remote_validator = {etag:h.etag ?? null, last_modified:h['last-modified'] ?? null,
  content_length:Number(h['content-length']) || doc.remote_validator.content_length};
doc.size = doc.remote_validator.content_length;
doc.saved_at = $now.toISO();
doc.edition = null;
doc.pages = null;
delete doc.old_path; delete doc.old_url; delete doc.destination_url;
return [{json:doc}];
''')
code('render', 'Update INDEX', r'''
let html = $('Read INDEX').first().json.data;
const pattern = /(<script id="catalog-data" type="application\/json">)([\s\S]*?)(<\/script>)/;
const catalog = JSON.parse(html.match(pattern)[2]);
const documents = new Map(catalog.documents.map(d => [d.key,d]));
for (const item of $input.all()) documents.set(item.json.key, item.json);
catalog.documents = [...documents.values()];
catalog.folders = [...new Set([...catalog.folders, ...catalog.documents.map(d=>d.folder)])].sort();
catalog.generated_at = $now.toISO();
const data = JSON.stringify(catalog, null, 2).replace(/</g,'\\u003c');
html = html.replace(pattern, (_,a,b,c)=>a+data+c);
const escape = s => String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const folders = catalog.folders.map(folder => {
  const docs = catalog.documents.filter(d => d.folder === folder);
  return '<details><summary>'+escape(folder)+' — '+docs.length+' документов</summary><ul>'+docs.map(d=>
    '<li><a href="'+escape(d.path.split('/').map(encodeURIComponent).join('/'))+'">'+escape(d.title)+'</a></li>').join('')+'</ul></details>';
}).join('');
html = html.replace(/<div class="noscript">[\s\S]*?<\/div>/, '<div class="noscript">'+folders+'<p>Для поиска и постраничного просмотра включите JavaScript.</p></div>');
html = html.replace('Дата источника — дата обновления в каталоге производителя.', 'Дата источника — дата обновления в каталоге производителя; для Lenovo Press — Last-Modified PDF.');
return [{json:{html, updated:$input.all().length, documents:catalog.documents.length}}];
''')
http('publish', 'Save INDEX', 'PUT',
     'http://nextcloud.edge.internal/remote.php/webdav/technical-documentation/lenovo/originals/INDEX.html', True,
     format='autodetect',
     extra={'sendBody': True, 'contentType': 'raw', 'rawContentType': 'text/html; charset=utf-8', 'body': '={{ $json.html }}'})


def sdk(value):
    if isinstance(value, str) and value.startswith('='):
        return 'expr(' + json.dumps(value[1:]) + ')'
    if isinstance(value, dict):
        if set(value) == {'id', 'name'}:
            return 'newCredential(' + json.dumps(value['name']) + ')'
        return '{' + ','.join(json.dumps(k) + ':' + sdk(v) for k,v in value.items()) + '}'
    if isinstance(value, list):
        return '[' + ','.join(sdk(v) for v in value) + ']'
    return json.dumps(value, ensure_ascii=False)


builder = ["import { workflow, node, trigger, ifElse, splitInBatches, nextBatch, newCredential, expr } from '@n8n/workflow-sdk';"]
for var, obj in nodes:
    factory = 'trigger' if var in ('daily','manual') else 'ifElse' if var == 'renamed' else 'splitInBatches' if var == 'batch' else 'node'
    if var == 'batch':
        obj = {k:v for k,v in obj.items() if k != 'type'}
    builder.append(f'const {var} = {factory}({sdk(obj)});')
builder.append("""
export default workflow('technical-documentation-sync', 'TechnicalDocumentationSync01')
 .add(daily).to(read).to(models).to(asp).to(families).to(head).to(changed)
 .to(batch.onEachBatch(download.to(upload).to(renamed.onTrue(remove.to(receipt).to(nextBatch(batch))).onFalse(receipt.to(nextBatch(batch)))))
   .onDone(render.to(publish)))
 .add(manual).to(read);
""")
(ROOT / 'TechnicalDocumentationSync01.ts').write_text('\n'.join(builder))
if args.validation_output:
    args.validation_output.write_text(json.dumps([
        {'name':obj['config']['name'], 'type':obj.get('type','n8n-nodes-base.splitInBatches'),
         'typeVersion':obj['version'], 'parameters':obj['config']['parameters']} for _,obj in nodes]))
print(f'Generated {len(nodes)} native nodes; JavaScript syntax checked')
