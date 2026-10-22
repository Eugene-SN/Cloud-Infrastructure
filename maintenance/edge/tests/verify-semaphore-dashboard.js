const fs = require('fs');
const vm = require('vm');
const assert = require('assert');
const html = fs.readFileSync(`${__dirname}/../dashboard/index.html`, 'utf8');
const code = html.slice(html.indexOf('    async function waitControllerUpdate'), html.indexOf('    function escapeHtml'));
async function scenario(taskStatus, output, states) {
  const messages = [];
  let stateCalls = 0;
  let taskCalls = 0;
  const statuses = Array.isArray(taskStatus) ? taskStatus : [taskStatus];
  const context = {
    setTimeout: callback => callback(), AbortSignal,
    escapeHtml: value => value,
    showToast: (message, level) => messages.push([message, level]),
    apiFetch: async url => ({ok: true, json: async () => {
      if (url.endsWith('/output')) return [{output}];
      if (url.endsWith('controller-update.json')) return states[Math.min(stateCalls++, states.length - 1)];
      const status = statuses[Math.min(taskCalls++, statuses.length - 1)];
      if (status === 'offline') throw new Error('Network unavailable');
      return {status};
    }}),
  };
  vm.createContext(context);
  vm.runInContext(code, context);
  const success = await context.pollTask(123, 'Semaphore');
  return {success, messages, stateCalls, taskCalls};
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
  r = await scenario([...Array(200).fill('running'), 'success'], 'normal component update', []);
  assert(r.success && r.taskCalls === 201, 'long-running tasks must wait for their actual result');
  assert(!r.messages.some(([m]) => m.includes('timed out')));
  r = await scenario(['offline', 'offline', 'running', 'success'], 'normal component update', []);
  assert(r.success && r.taskCalls === 4, 'connection loss must not turn into a failed update');
  assert(r.messages.some(([m]) => m.includes('reconnect')), 'explain that the task outcome is unknown while disconnected');
  r = await scenario('error', '', []);
  assert(!r.success && r.messages.some(([, level]) => level === 'bad'));
  r = await scenario('success', 'SEMAPHORE_UPDATE_ID=operation-1', [
    ...Array(335).fill({status: 'pending', operation: 'operation-1'}),
    {status: 'success', operation: 'operation-1'},
  ]);
  assert(r.success && r.stateCalls === 336, 'a pending external Semaphore update is not a failed update');
  console.log('SEMAPHORE_DASHBOARD_CONTRACT=PASS|REAL_NETWORK_CALLS=NO');
})().catch(error => {console.error(error); process.exit(1);});
