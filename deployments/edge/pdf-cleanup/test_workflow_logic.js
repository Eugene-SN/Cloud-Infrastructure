const assert = require('node:assert/strict');
const nodes = require(process.argv[2]);
const AsyncFunction = Object.getPrototypeOf(async function(){}).constructor;
const code = name => new AsyncFunction('$input', '$', '$execution', '$now', nodes.find(n=>n.name===name).parameters.jsCode);
const item = json => ({json});
(async () => {
  const normalize = code('Normalize Request');
  const trigger = () => ({isExecuted:false});
  for (const path of ['../x.pdf','folder/../x.pdf','/x.pdf','folder//x.pdf','folder/./x.pdf','x\\y.pdf','x\n.pdf','x\0.pdf','.pdf']) {
    await assert.rejects(normalize({all:()=>[item({path})]}, trigger, {id:'1'}), /path/);
  }
  await assert.rejects(normalize({all:()=>[item({})]}, trigger, {id:'1'}), /path/);
  const good = await normalize({all:()=>[item({path:'Model A/subfolder/指南 #%.pdf'})]}, trigger, {id:'1'});
  assert.equal(good[0].json.cleaned_path, '/technical-documentation/lenovo/cleaned/Model A/subfolder/指南 #%.pdf');
  assert(good[0].json.cleaned_url.endsWith('Model%20A/subfolder/%E6%8C%87%E5%8D%97%20%23%25.pdf'));
  const revision=await normalize({all:()=>[item({path:'Model A/manual-v2.pdf',previous_path:'Model A/manual-v1.pdf'})]},trigger,{id:'1'});
  assert(revision[0].json.previous_cleaned_url.endsWith('/cleaned/Model%20A/manual-v1.pdf'));
  const many=await normalize({all:()=>[item({path:'Model A/a.pdf'}),item({path:'Model B/b.pdf'})]},trigger,{id:'1'});
  assert.equal(many.length,2);assert.deepEqual(many.map(x=>x.pairedItem.item),[0,1]);
  const batch=await normalize({all:()=>[item({files:[{path:'Model A/a.pdf'},{path:'Model B/b.pdf'}]})]},trigger,{id:'1'});
  assert.equal(batch.length,2);assert.deepEqual(batch.map(x=>x.pairedItem.item),[0,0]);
  await assert.rejects(normalize({all:()=>[item({files:[]})]},trigger,{id:'1'}),/files/);
  for (const previous_path of ['../bad.pdf','Model B/manual-v1.pdf','Model A/manual-v2.pdf'])
    await assert.rejects(normalize({all:()=>[item({path:'Model A/manual-v2.pdf',previous_path})]},trigger,{id:'1'}),/path/);
  const returned = code('Return Result');
  const run = async ({processOk=true, status=204, releaseOk=true, deletionStatus=null}={}) => {
    const outputs = {
      'Capture Job':item({path:'Model A/test.pdf',original_path:'/originals/test.pdf',cleaned_path:'/cleaned/test.pdf',previous_path:deletionStatus!==null?'old.pdf':null}),
      'Run PDF Cleanup CLI':item({code:0,stdout:JSON.stringify({ok:processOk,error:'CLI failure'})}),
      'Publish Cleaned PDF':item({statusCode:status}),
      'Remove Temporary Job':item({code:0,stdout:JSON.stringify({ok:releaseOk})})
    };
    if (deletionStatus!==null) outputs['Remove Previous Cleaned PDF']=item({statusCode:deletionStatus});
    const lookup = name => ({isExecuted:Boolean(outputs[name]),item:outputs[name],first:()=>outputs[name]});
    const html='<script id="catalog-data" type="application/json">'+JSON.stringify({documents:[{path:'Model A/test.pdf',cleanup_status:'pending'},{path:'Model B/other.pdf',cleanup_status:'cleaned',cleaned_at:'earlier'}]})+'</script>';
    return returned({first:()=>item({data:html})}, lookup,{id:'1'},{toISO:()=> '2026-10-05T17:00:00+03:00'});
  };
  assert.equal((await run())[0].json.temporary_job_removed,true);
  const result=(await run())[0].json;
  const index=JSON.parse(result.html.match(/<script id="catalog-data" type="application\/json">([\s\S]*?)<\/script>/)[1]);
  assert.equal(index.documents[0].cleanup_status,'cleaned');
  assert.equal(index.documents[0].cleaned_path,'Model A/test.pdf');
  assert.equal(index.documents[1].cleaned_at,'earlier');
  await assert.rejects(run({processOk:false}), /CLI failure/);
  await assert.rejects(run({status:500}), /upload failed/);
  await assert.rejects(run({releaseOk:false}), /removal failed/);
  assert.equal((await run({deletionStatus:204}))[0].json.ok,true);
  assert.equal((await run({deletionStatus:404}))[0].json.ok,true);
  await assert.rejects(run({deletionStatus:403}),/deletion failed/);
  const expr=nodes.find(n=>n.name==='Previous Cleaned Filename').parameters.conditions.conditions[0].leftValue;
  const predicate=new Function('$','$json','return '+expr.slice(3,-2));
  assert.equal(predicate(()=>({item:item({previous_path:'Model A/old.pdf'})}),{statusCode:201}),true);
  assert.equal(predicate(()=>({item:item({previous_path:'Model A/old.pdf'})}),{statusCode:500}),false);
  assert.equal(predicate(()=>({item:item({previous_path:null})}),{statusCode:201}),false);
  console.log('Relative paths, mirrored output/Unicode URLs, cross-folder/traversal rejection, revision deletion only after upload, success/CLI/upload/removal outcomes passed');
})().catch(error=>{console.error(error);process.exitCode=1;});
