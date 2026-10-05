const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const directory = process.argv[2];
const fixture = JSON.parse(fs.readFileSync(__dirname+'/test-fixtures.json','utf8'));
const nodes = JSON.parse(fs.readFileSync(directory+'/nodes.json'));
const html = '<!doctype html><script id="catalog-data" type="application/json">'+JSON.stringify(fixture.catalog)+'</script><div class="noscript"></div>';
const catalog = JSON.parse(html.match(/<script id="catalog-data" type="application\/json">([\s\S]*?)<\/script>/)[1]);
const asp = fixture.asp;
async function run(name,input,previous={}) {
  const source = nodes.find(n=>n.name===name).parameters.jsCode;
  const context = vm.createContext({$input:{all:()=>input,first:()=>input[0]},
    $:name=>({all:()=>previous[name],first:()=>previous[name][0]}),
    $now:{toISO:()=> '2026-10-05T14:00:00+03:00'}});
  return JSON.parse(JSON.stringify(await vm.runInContext('(async function(){'+source+'})()',context)));
}
(async()=>{
  const models = await run('Models and Index',[]);
  const families = await run('Latest Document Families',[{json:{body:asp}}],{'Models and Index':models});
  assert.equal(families.length,15);
  assert.equal(families.find(d=>d.json.key.endsWith('/bmc-event-reference')).json.path,'WR5220 G3/lenovo_bmc_event_reference_guide_g5_v4.pdf');
  assert.equal(families.filter(d=>d.json.key.endsWith('/lxpm-user-guide')).length,1);
  const headers = families.map(({json:d})=>{
    const v=catalog.documents.find(old=>old.key===d.key)?.remote_validator;
    return {json:{headers:{etag:v?.etag??'"new"','last-modified':v?.last_modified??'Tue, 21 Apr 2026 10:00:00 GMT','content-length':String(v?.content_length??12345)}}};
  });
  const previous={'Read INDEX':[{json:{data:html}}],'Latest Document Families':families};
  let changed = await run('Changed Documents',headers,previous);
  assert.deepEqual(changed.map(x=>x.json.key.split('/')[1]).sort(),['bios-setup-specification','psu-label-matrix','vmware-code-recipe']);
  const manual = families.findIndex(d=>d.json.key.endsWith('/user-manual'));
  const revised = structuredClone(headers); revised[manual].json.headers.etag='"replacement"';
  changed = await run('Changed Documents',revised,previous);
  assert(changed.some(d=>d.json.key.endsWith('/user-manual')));
  const renamed=structuredClone(families); renamed[manual].json.source_url=renamed[manual].json.source_url.replace('v18','v19');renamed[manual].json.path=renamed[manual].json.path.replace('v18','v19');
  changed=await run('Changed Documents',revised,{...previous,'Latest Document Families':renamed});
  const doc=changed.find(d=>d.json.key.endsWith('/user-manual')).json;
  assert(doc.old_path.endsWith('v18.pdf')); assert(doc.path.endsWith('v19.pdf'));
  assert.equal(doc.title,'User Manual Lenovo Wentian WR5220 G3');
  const other=structuredClone(models);other[0].json.model.folder='Second Model';
  const additional=await run('Latest Document Families',[{json:{body:asp}}],{'Models and Index':other});
  assert(additional.every(d=>d.json.key.startsWith('Second Model/')&&d.json.path.startsWith('Second Model/')));
  const rendered=await run('Update INDEX',[{json:{...doc,title:'<script>PDF</script>',size:12345,remote_validator:{etag:'"replacement"'},edition:null,pages:null}}],{'Read INDEX':[{json:{data:html}}]});
  assert(rendered[0].json.html.includes('&lt;script&gt;PDF&lt;/script&gt;'));
  const updated=JSON.parse(rendered[0].json.html.match(/<script id="catalog-data" type="application\/json">([\s\S]*?)<\/script>/)[1]);
  assert.equal(updated.documents.length,12);
  assert(updated.documents.find(d=>d.key===doc.key).path.endsWith('v19.pdf'));
  await assert.rejects(()=>run('Latest Document Families',[{json:{body:{status:500}}}],{'Models and Index':models}));
  console.log('PASS: current-family deduplication, missing documents, same-URL ETag replacement, versioned filename replacement, stable labels, model isolation, HTML escaping, source failure stops processing');
})().catch(error=>{console.error(error);process.exitCode=1});
