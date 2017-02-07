#
# Copyright 2015 NEC Corporation.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import os

from tempest import config
from tempest.test_discover import plugins

import aodh
from aodh.tests.tempest import config as tempest_config


class AodhTempestPlugin(plugins.TempestPlugin):

    def load_tests(self):
        base_path = os.path.split(os.path.dirname(
            os.path.abspath(aodh.__file__)))[0]
        test_dir = "aodh/tests/tempest"
        full_test_dir = os.path.join(base_path, test_dir)
        return full_test_dir, base_path

    def register_opts(self, conf):
        config.register_opt_group(conf,
                                  config.service_available_group,
                                  tempest_config.service_option)
        config.register_opt_group(conf,
                                  tempest_config.alarming_group,
                                  tempest_config.AlarmingGroup)

    def get_opt_lists(self):
        return [
            (tempest_config.alarming_group.name,
             tempest_config.AlarmingGroup),
            ('service_available', tempest_config.service_option)
        ]
