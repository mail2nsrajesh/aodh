#
# Copyright 2014 Cisco Systems,Inc.
#
# Author: Pradeep Kilambi <pkilambi@cisco.com>
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import mock

from ceilometer.central import manager
from ceilometer.network.services import lbaas
from ceilometer.openstack.common import context
from ceilometer.openstack.common.fixture import mockpatch
from ceilometer.openstack.common import test


class _BaseTestLBPollster(test.BaseTestCase):

    @mock.patch('ceilometer.pipeline.setup_pipeline', mock.MagicMock())
    def setUp(self):
        super(_BaseTestLBPollster, self).setUp()
        self.addCleanup(mock.patch.stopall)
        self.context = context.get_admin_context()
        self.manager = manager.AgentManager()


class TestLBPoolPollster(_BaseTestLBPollster):

    def setUp(self):
        super(TestLBPoolPollster, self).setUp()
        self.pollster = lbaas.LBPoolPollster()
        fake_pools = self.fake_get_pools()
        self.useFixture(mockpatch.Patch('ceilometer.neutron_client.Client.'
                                        'pool_get_all',
                                        return_value=fake_pools))

    @staticmethod
    def fake_get_pools():
        return [{'status': 'ACTIVE',
                 'lb_method': 'ROUND_ROBIN',
                 'protocol': 'HTTP',
                 'description': '',
                 'health_monitors': [],
                 'members': [],
                 'provider': 'haproxy',
                 'status_description': None,
                 'id': 'ce73ad36-437d-4c84-aee1-186027d3da9a',
                 'vip_id': 'cd6a6fee-e2fa-4e6c-b3c2-bfbe395752c1',
                 'name': 'mylb',
                 'admin_state_up': True,
                 'subnet_id': 'bbe3d818-bdcb-4e4b-b47f-5650dc8a9d7a',
                 'tenant_id': 'a4eb9f4938bb418bbc4f8eb31802fefa',
                 'health_monitors_status': []},
                {'status': 'INACTIVE',
                 'lb_method': 'ROUND_ROBIN',
                 'protocol': 'HTTP',
                 'description': '',
                 'health_monitors': [],
                 'members': [],
                 'provider': 'haproxy',
                 'status_description': None,
                 'id': 'ce73ad36-437d-4c84-aee1-186027d3da9a',
                 'vip_id': 'cd6a6fee-e2fa-4e6c-b3c2-bfbe395752c1',
                 'name': 'mylb02',
                 'admin_state_up': True,
                 'subnet_id': 'bbe3d818-bdcb-4e4b-b47f-5650dc8a9d7a',
                 'tenant_id': 'a4eb9f4938bb418bbc4f8eb31802fefa',
                 'health_monitors_status': []},
                {'status': 'PENDING_CREATE',
                 'lb_method': 'ROUND_ROBIN',
                 'protocol': 'HTTP',
                 'description': '',
                 'health_monitors': [],
                 'members': [],
                 'provider': 'haproxy',
                 'status_description': None,
                 'id': 'fe7rad36-437d-4c84-aee1-186027d3bdcd',
                 'vip_id': 'cd6a6fee-e2fa-4e6c-b3c2-bfbe395752c1',
                 'name': 'mylb03',
                 'admin_state_up': True,
                 'subnet_id': 'bbe3d818-bdcb-4e4b-b47f-5650dc8a9d7a',
                 'tenant_id': 'a4eb9f4938bb418bbc4f8eb31802fefa',
                 'health_monitors_status': []},
                {'status': 'UNKNOWN',
                 'lb_method': 'ROUND_ROBIN',
                 'protocol': 'HTTP',
                 'description': '',
                 'health_monitors': [],
                 'members': [],
                 'provider': 'haproxy',
                 'status_description': None,
                 'id': 'fe7rad36-437d-4c84-aee1-186027d3bdcd',
                 'vip_id': 'cd6a6fee-e2fa-4e6c-b3c2-bfbe395752c1',
                 'name': 'mylb03',
                 'admin_state_up': True,
                 'subnet_id': 'bbe3d818-bdcb-4e4b-b47f-5650dc8a9d7a',
                 'tenant_id': 'a4eb9f4938bb418bbc4f8eb31802fefa',
                 'health_monitors_status': []},
                ]

    def test_pool_get_samples(self):
        samples = list(self.pollster.get_samples(self.manager, {}))
        self.assertEqual(3, len(samples))
        for field in self.pollster.FIELDS:
            self.assertEqual(self.fake_get_pools()[0][field],
                             samples[0].resource_metadata[field])

    def test_pool_volume(self):
        samples = list(self.pollster.get_samples(self.manager, {}))
        self.assertEqual(1, samples[0].volume)
        self.assertEqual(0, samples[1].volume)
        self.assertEqual(2, samples[2].volume)

    def test_get_pool_meter_names(self):
        samples = list(self.pollster.get_samples(self.manager, {}))
        self.assertEqual(set(['network.services.lb.pool']),
                         set([s.name for s in samples]))


class TestLBVipPollster(_BaseTestLBPollster):

    def setUp(self):
        super(TestLBVipPollster, self).setUp()
        self.pollster = lbaas.LBVipPollster()
        fake_vips = self.fake_get_vips()
        self.useFixture(mockpatch.Patch('ceilometer.neutron_client.Client.'
                                        'vip_get_all',
                                        return_value=fake_vips))

    @staticmethod
    def fake_get_vips():
        return [{'status': 'ACTIVE',
                 'status_description': None,
                 'protocol': 'HTTP',
                 'description': '',
                 'admin_state_up': True,
                 'subnet_id': 'bbe3d818-bdcb-4e4b-b47f-5650dc8a9d7a',
                 'tenant_id': 'a4eb9f4938bb418bbc4f8eb31802fefa',
                 'connection_limit': -1,
                 'pool_id': 'ce73ad36-437d-4c84-aee1-186027d3da9a',
                 'session_persistence': None,
                 'address': '10.0.0.2',
                 'protocol_port': 80,
                 'port_id': '3df3c4de-b32e-4ca1-a7f4-84323ba5f291',
                 'id': 'cd6a6fee-e2fa-4e6c-b3c2-bfbe395752c1',
                 'name': 'myvip'},
                {'status': 'INACTIVE',
                 'status_description': None,
                 'protocol': 'HTTP',
                 'description': '',
                 'admin_state_up': True,
                 'subnet_id': 'bbe3d818-bdcb-4e4b-b47f-5650dc8a9d7a',
                 'tenant_id': 'a4eb9f4938bb418bbc4f8eb31802fefa',
                 'connection_limit': -1,
                 'pool_id': 'ce73ad36-437d-4c84-aee1-186027d3da9a',
                 'session_persistence': None,
                 'address': '10.0.0.3',
                 'protocol_port': 80,
                 'port_id': '3df3c4de-b32e-4ca1-a7f4-84323ba5f291',
                 'id': 'ba6a6fee-e2fa-4e6c-b3c2-bfbe395752c1',
                 'name': 'myvip02'},
                {'status': 'PENDING_CREATE',
                 'status_description': None,
                 'protocol': 'HTTP',
                 'description': '',
                 'admin_state_up': True,
                 'subnet_id': 'bbe3d818-bdcb-4e4b-b47f-5650dc8a9d7a',
                 'tenant_id': 'a4eb9f4938bb418bbc4f8eb31802fefa',
                 'connection_limit': -1,
                 'pool_id': 'ce73ad36-437d-4c84-aee1-186027d3da9a',
                 'session_persistence': None,
                 'address': '10.0.0.4',
                 'protocol_port': 80,
                 'port_id': '3df3c4de-b32e-4ca1-a7f4-84323ba5f291',
                 'id': 'fg6a6fee-e2fa-4e6c-b3c2-bfbe395752c1',
                 'name': 'myvip03'},
                {'status': 'UNKNOWN',
                 'status_description': None,
                 'protocol': 'HTTP',
                 'description': '',
                 'admin_state_up': True,
                 'subnet_id': 'bbe3d818-bdcb-4e4b-b47f-5650dc8a9d7a',
                 'tenant_id': 'a4eb9f4938bb418bbc4f8eb31802fefa',
                 'connection_limit': -1,
                 'pool_id': 'ce73ad36-437d-4c84-aee1-186027d3da9a',
                 'session_persistence': None,
                 'address': '10.0.0.8',
                 'protocol_port': 80,
                 'port_id': '3df3c4de-b32e-4ca1-a7f4-84323ba5f291',
                 'id': 'fg6a6fee-e2fa-4e6c-b3c2-bfbe395752c1',
                 'name': 'myvip03'},
                ]

    def test_vip_get_samples(self):
        samples = list(self.pollster.get_samples(self.manager, {}))
        self.assertEqual(3, len(samples))
        for field in self.pollster.FIELDS:
            self.assertEqual(self.fake_get_vips()[0][field],
                             samples[0].resource_metadata[field])

    def test_pool_volume(self):
        samples = list(self.pollster.get_samples(self.manager, {}))
        self.assertEqual(1, samples[0].volume)
        self.assertEqual(0, samples[1].volume)
        self.assertEqual(2, samples[2].volume)

    def test_get_vip_meter_names(self):
        samples = list(self.pollster.get_samples(self.manager, {}))
        self.assertEqual(set(['network.services.lb.vip']),
                         set([s.name for s in samples]))


class TestLBMemberPollster(_BaseTestLBPollster):

    def setUp(self):
        super(TestLBMemberPollster, self).setUp()
        self.pollster = lbaas.LBMemberPollster()
        fake_members = self.fake_get_members()
        self.useFixture(mockpatch.Patch('ceilometer.neutron_client.Client.'
                                        'member_get_all',
                                        return_value=fake_members))

    @staticmethod
    def fake_get_members():
        return [{'status': 'ACTIVE',
                 'protocol_port': 80,
                 'weight': 1,
                 'admin_state_up': True,
                 'tenant_id': 'a4eb9f4938bb418bbc4f8eb31802fefa',
                 'pool_id': 'ce73ad36-437d-4c84-aee1-186027d3da9a',
                 'address': '10.0.0.3',
                 'status_description': None,
                 'id': '290b61eb-07bc-4372-9fbf-36459dd0f96b'},
                {'status': 'INACTIVE',
                 'protocol_port': 80,
                 'weight': 1,
                 'admin_state_up': True,
                 'tenant_id': 'a4eb9f4938bb418bbc4f8eb31802fefa',
                 'pool_id': 'ce73ad36-437d-4c84-aee1-186027d3da9a',
                 'address': '10.0.0.5',
                 'status_description': None,
                 'id': '2456661eb-07bc-4372-9fbf-36459dd0f96b'},
                {'status': 'PENDING_CREATE',
                 'protocol_port': 80,
                 'weight': 1,
                 'admin_state_up': True,
                 'tenant_id': 'a4eb9f4938bb418bbc4f8eb31802fefa',
                 'pool_id': 'ce73ad36-437d-4c84-aee1-186027d3da9a',
                 'address': '10.0.0.6',
                 'status_description': None,
                 'id': '45630b61eb-07bc-4372-9fbf-36459dd0f96b'},
                {'status': 'UNKNOWN',
                 'protocol_port': 80,
                 'weight': 1,
                 'admin_state_up': True,
                 'tenant_id': 'a4eb9f4938bb418bbc4f8eb31802fefa',
                 'pool_id': 'ce73ad36-437d-4c84-aee1-186027d3da9a',
                 'address': '10.0.0.6',
                 'status_description': None,
                 'id': '45630b61eb-07bc-4372-9fbf-36459dd0f96b'},
                ]

    def test_get_samples_not_empty(self):
        samples = list(self.pollster.get_samples(self.manager, {}))
        self.assertEqual(3, len(samples))
        for field in self.pollster.FIELDS:
            self.assertEqual(self.fake_get_members()[0][field],
                             samples[0].resource_metadata[field])

    def test_pool_volume(self):
        samples = list(self.pollster.get_samples(self.manager, {}))
        self.assertEqual(1, samples[0].volume)
        self.assertEqual(0, samples[1].volume)
        self.assertEqual(2, samples[2].volume)

    def test_get_meter_names(self):
        samples = list(self.pollster.get_samples(self.manager, {}))
        self.assertEqual(set(['network.services.lb.member']),
                         set([s.name for s in samples]))


class TestLBHealthProbePollster(_BaseTestLBPollster):

    def setUp(self):
        super(TestLBHealthProbePollster, self).setUp()
        self.pollster = lbaas.LBHealthMonitorPollster()
        fake_health_monitor = self.fake_get_health_monitor()
        self.useFixture(mockpatch.Patch('ceilometer.neutron_client.Client.'
                                        'health_monitor_get_all',
                                        return_value=fake_health_monitor))

    @staticmethod
    def fake_get_health_monitor():
        return [{'id': '34ae33e1-0035-49e2-a2ca-77d5d3fab365',
                 'admin_state_up': True,
                 'tenant_id': "d5d2817dae6b42159be9b665b64beb0e",
                 'delay': 2,
                 'max_retries': 5,
                 'timeout': 5,
                 'pools': [],
                 'type': 'PING',
                 }]

    def test_get_samples_not_empty(self):
        samples = list(self.pollster.get_samples(self.manager, {}))
        self.assertEqual(1, len(samples))
        for field in self.pollster.FIELDS:
            self.assertEqual(self.fake_get_health_monitor()[0][field],
                             samples[0].resource_metadata[field])

    def test_get_meter_names(self):
        samples = list(self.pollster.get_samples(self.manager, {}))
        self.assertEqual(set(['network.services.lb.health_monitor']),
                         set([s.name for s in samples]))


class TestLBStatsPollster(_BaseTestLBPollster):

    def setUp(self):
        super(TestLBStatsPollster, self).setUp()
        fake_pool_stats = self.fake_pool_stats()
        self.useFixture(mockpatch.Patch('ceilometer.neutron_client.Client.'
                                        'pool_stats',
                                        return_value=fake_pool_stats))

        fake_pools = self.fake_get_pools()
        self.useFixture(mockpatch.Patch('ceilometer.neutron_client.Client.'
                                        'pool_get_all',
                                        return_value=fake_pools))

    @staticmethod
    def fake_get_pools():
        return [{'status': 'ACTIVE',
                 'lb_method': 'ROUND_ROBIN',
                 'protocol': 'HTTP',
                 'description': '',
                 'health_monitors': [],
                 'members': [],
                 'provider': 'haproxy',
                 'status_description': None,
                 'id': 'ce73ad36-437d-4c84-aee1-186027d3da9a',
                 'vip_id': 'cd6a6fee-e2fa-4e6c-b3c2-bfbe395752c1',
                 'name': 'mylb',
                 'admin_state_up': True,
                 'subnet_id': 'bbe3d818-bdcb-4e4b-b47f-5650dc8a9d7a',
                 'tenant_id': 'a4eb9f4938bb418bbc4f8eb31802fefa',
                 'health_monitors_status': []},
                ]

    @staticmethod
    def fake_pool_stats():
        return {'stats': {'active_connections': 2L,
                          'bytes_in': 1L,
                          'bytes_out': 3L,
                          'total_connections': 4L
                          }
                }

    @mock.patch('ceilometer.pipeline.setup_pipeline', mock.MagicMock())
    def _check_get_samples(self, factory, sample_name, expected_volume):
        pollster = factory()

        cache = {}
        samples = list(pollster.get_samples(self.manager, cache))
        self.assertEqual(1, len(samples))
        self.assertIsNotNone(samples)
        self.assertIn('lbstats', cache)
        self.assertEqual(set([sample_name]), set([s.name for s in samples]))

        match = [s for s in samples if s.name == sample_name]
        self.assertEqual(1, len(match), 'missing counter %s' % sample_name)
        self.assertEqual(expected_volume, match[0].volume)
        self.assertEqual('gauge', match[0].type)

    def test_lb_total_connections(self):
        self._check_get_samples(lbaas.LBTotalConnectionsPollster,
                                'network.services.lb.total.connections', 4L)

    def test_lb_active_connections(self):
        self._check_get_samples(lbaas.LBActiveConnectionsPollster,
                                'network.services.lb.active.connections', 2L)

    def test_lb_incoming_bytes(self):
        self._check_get_samples(lbaas.LBBytesInPollster,
                                'network.services.lb.incoming.bytes', 1L)

    def test_lb_outgoing_bytes(self):
        self._check_get_samples(lbaas.LBBytesOutPollster,
                                'network.services.lb.outgoing.bytes', 3L)