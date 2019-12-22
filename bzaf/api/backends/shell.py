#!/usr/bin/env python
"""
Copyright 2019 Vadim Khitrin <me@vkhitrin.com>
               Pini Komarov  <pkomarov@redhat.com>

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

from bzaf.api.backends import BaseBackend
from bzaf.api.schemas.shell import schema
from bzaf.utils import logger
from collections import namedtuple
import subprocess
from subprocess import Popen

MOCK_STEP = {
    "cmd": "true",
    "rc": 0
}

bzaf_logger = logger.subscribe_to_logger()


class ShellBackend(BaseBackend):
    def __init__(self):
        self.name = 'shell'
        self.min_version = 1
        self.version = self.min_version
        self.max_version = self.min_version
        self.schema = schema
        self.step = MOCK_STEP
        super().__init__(self.name,
                         self.min_version,
                         self.version,
                         self.max_version,
                         self.schema,
                         self.step)

    # Overrdie method of BaseBackend
    def execute_backend(self):
        # Parse required arugments
        cmd = self.step['cmd']
        rc = self.step['rc']
        # Execute command
        shell_run = Popen(cmd, stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE,
                          shell=True,
                          universal_newlines=True)
        output, errors = shell_run.communicate()
        s_rc = shell_run.returncode
        # If executed return code equals desired return code
        bzaf_logger.debug('CMD: {}'.format(cmd))
        bzaf_logger.debug('OUTPUT: {}'.format(output).rstrip())
        bzaf_logger.debug('Return code: {}'.format(s_rc))
        if rc == s_rc:
            execution_successful = True
            bzaf_logger.debug('Command executed successfully with the '
                              'expected return code')
        else:
            execution_successful = False
            bzaf_logger.error('Command failed to execute with the '
                              'expected return code')
            bzaf_logger.error('Expected return code: {}'.format(rc))
            if errors:
                bzaf_logger.error('Error: {}'.format(errors))
        # create a namedtuple to hold
        # the execution rc and stdout/err
        execution_result = namedtuple('execution_result',
                                      ['execution_successful', 'rc', 'stdout',
                                       'stderr'])
        execution_result = execution_result(execution_successful,
                                            s_rc,
                                            output,
                                            errors)
        return execution_result
