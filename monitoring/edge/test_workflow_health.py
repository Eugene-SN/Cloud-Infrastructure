"""Offline execution-state and incident tests; never open production SQLite."""
import copy
import json
import runpy
import sqlite3
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path


class WorkflowHealthTest(unittest.TestCase):
    def setUp(self):
        self.monitor = runpy.run_path(str(Path(__file__).with_name('edge-monitor')))
        self.temp = tempfile.TemporaryDirectory(prefix='edge-workflow-health-', dir='/tmp')
        self.database = Path(self.temp.name)/'executions.sqlite'
        self.now = 1800000000
        self.config = {'n8n_workflows': {
            'database': str(self.database), 'consecutive_failure_threshold': 3,
            'stale_cadence_multiplier': 3,
            'workflows': [{'id': 'critical', 'cadence_s': 300}]}}
        with sqlite3.connect(self.database) as db:
            db.executescript('CREATE TABLE workflow_entity '
                '(id TEXT,name TEXT,active INT,nodes TEXT,settings TEXT,createdAt TEXT);'
                'CREATE TABLE execution_entity (workflowId TEXT,mode TEXT,status TEXT,startedAt TEXT);')
            db.execute('INSERT INTO workflow_entity VALUES (?,?,?,?,?,?)',
                ('critical', 'Critical', 1, json.dumps([{
                    'type': 'n8n-nodes-base.scheduleTrigger',
                    'parameters': {'rule': {'interval': [{'field':'minutes','minutesInterval':5}]}}
                }]), '{"executionTimeout":120}', self.timestamp(self.now-2000)))

    def tearDown(self):
        self.temp.cleanup()

    def timestamp(self, value):
        return datetime.fromtimestamp(value, timezone.utc).isoformat()

    def execution(self, status, ago, mode='trigger'):
        with sqlite3.connect(self.database) as db:
            db.execute('INSERT INTO execution_entity VALUES (?,?,?,?)',
                       ('critical',mode,status,self.timestamp(self.now-ago)))

    def health(self):
        return self.monitor['collect_n8n_workflows'](self.config, now=self.now)

    def test_single_failure_is_not_incident(self):
        self.execution('success',400);self.execution('error',100)
        self.assertEqual(self.health()['state'],'OK')

    def test_repeated_failures_and_scheduled_recovery(self):
        self.execution('success',950)
        for age in (700,400,100):self.execution('error',age)
        self.assertEqual(self.health()['state'],'DEGRADED')
        self.execution('success',20,'manual')
        self.assertEqual(self.health()['state'],'DEGRADED')
        self.execution('success',10)
        self.assertEqual(self.health()['state'],'OK')

    def test_stale_and_no_success(self):
        self.assertEqual(self.health()['state'],'DEGRADED')
        self.execution('success',1100)
        self.assertEqual(self.health()['state'],'DEGRADED')
        self.execution('success',1000)
        self.assertEqual(self.health()['state'],'OK')

    def test_schedule_contract_drift(self):
        self.execution('success',10)
        with sqlite3.connect(self.database) as db:db.execute('UPDATE workflow_entity SET active=0')
        self.assertEqual(self.health()['state'],'DEGRADED')

    def test_one_domain_and_recovery_notification(self):
        sent=[]
        notify=self.monitor['update_notifications']
        notify.__globals__['post_mattermost']=lambda payload:sent.append(payload) or True
        notify.__globals__['STATE_PATH']=Path(self.temp.name)/'monitor-state.json'
        normal={'id':'n8n-workflow-health','name':'Critical n8n workflows','scope':'EDGE',
                'category':'Integration','state':'OK','suppressed':False,'diagnostics':[],
                'cause':'healthy','impact':'scheduled integrations'}
        bad={**normal,'state':'DEGRADED','cause':'3 consecutive failures'}
        state={'notification_model':2,'incidents':{}}
        for incident in (normal,bad,bad,normal):notify({normal['id']:incident},state)
        self.assertEqual(len(sent),2)
        self.assertEqual(state['incidents'][normal['id']]['state'],'OK')


if __name__=='__main__':unittest.main()
