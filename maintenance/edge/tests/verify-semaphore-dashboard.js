const fs = require('fs');
const vm = require('vm');
const assert = require('assert');
const html = fs.readFileSync(`${__dirname}/../dashboard/index.html`, 'utf8');
const code = html.slice(html.indexOf('    async function waitControllerUpdate'), html.indexOf('    function escapeHtml'));
async function scenario(taskStatus, output, states) {
  const messages = [];
  let stateCalls = 0;
  const context = {
    setTimeout: callback => callback(), AbortSignal,
    escapeHtml: value => value,
    showToast: (message, level) => messages.push([message, level]),
    apiFetch: async url => ({ok: true, json: async () => {
      if (url.endsWith('/output')) return [{output}];
      if (url.endsWith('controller-update.json')) return states[Math.min(stateCalls++, states.length - 1)];
      return {status: taskStatus};
    }}),
  };
  vm.createContext(context);
  vm.runInContext(code, context);
  const success = await context.pollTask(123, 'Semaphore', 1);
  return {success, messages, stateCalls};
}
(async () => {
  let r = await scenario('success', 'SEMAPHORE_UPDATE_ID=operation-1', [
    {status: 'success', operation: 'old-operation'},
    {status: 'pending', operation: 'operation-1'},
    {status: 'success', operation: 'operation-1'},
  ]);
  assert(r.success && r.stateCalls === 3);
  r = await scenario('success', 'SEMAPHORE_UPDATE_ID=operation-1', [{status: 'error', operation: 'operation-1'}]);
  assert(!r.success && !r.messages.some(([m]) => m.includes('completed successfully')));
  r = await scenario('stopped', '', []);
  assert(!r.success && r.stateCalls === 0);
  r = await scenario('success', 'normal component update', []);
  assert(r.success && r.stateCalls === 0);
  console.log('SEMAPHORE_DASHBOARD_CONTRACT=PASS|REAL_NETWORK_CALLS=NO');
})().catch(error => {console.error(error); process.exit(1);});
