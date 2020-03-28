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

import ansible_runner
import os
import re
import ruamel.yaml
import tempfile

from bzaf.api.backends import BaseBackend
from bzaf.api.schemas.ansible import schema
from bzaf.utils import logger
from collections import namedtuple

# TODO(vkhitirn): Enhance backend to support additional feature such as
#                 inventory

MOCK_STEP = {
    'playbook': [
        {
            'hosts': 'localhost',
            'tasks': [
                {
                    'shell': 'whoami'
                }
            ]
        }
    ]
}

# Subscribe to logger
bzaf_logger = logger.subscribe_to_logger()


def handle_ansi_chars(string):
    """
    Handles ANSI characters

    Returns a string with omitted ANSI characters
    """
    ansi_escape = re.compile(r'''
        \x1B    # ESC
        [@-_]   # 7-bit C1 Fe
        [0-?]*  # Parameter bytes
        [ -/]*  # Intermediate bytes
        [@-~]   # Final byte
    ''', re.VERBOSE)
    return ansi_escape.sub('', string)


def fix_ansi_list(string_list_to_fix):
    """
    Fixes list of characters containing ANSI characters

    Parameters:
        string_list_to_fix: A list of strings

    Returns a list of strings with applied fixes
    """
    return list(map(handle_ansi_chars, string_list_to_fix))


class AnsibleBackend(BaseBackend):
    """
    Ansible backend object

    Executes Ansible playbook

    Attributes:
        name = Backend name
        version = Requested version from APIRequest object
        min_version = Minimum version allowed for backend
        max_version = Maximum version allowed for backend
        schema = json_schema to be used to verify that the supplied setp
                 is valid according to the backends's requirments
        step - Ansible playbook
    """
    def __init__(self):
        self.name = 'ansible'
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

    def execute_backend(self):
        """
        Execute Ansible playbook

        Returns a namedtuple describing the bzaf spec execution
        """
        # Init variables
        playbook_file_ready = None
        # Prepare Ansible kwargs
        ans_kwargs = {}
        # Create a namedtuple to hold the execution rc and stdout/err
        execution_result = namedtuple('execution_result',
                                      ['execution_successful', 'rc', 'stdout',
                                       'stderr'])
        # Create temporary file
        temp_file = tempfile.NamedTemporaryFile(suffix='.yml', mode='w+t')
        temp_file_path = temp_file.name
        bzaf_logger.debug("Created temp file '{}'".format(temp_file_path))
        # Parse step dict from playbook dict
        step_yaml = self.step['playbook']
        # Initialize YAML parsing
        yaml = ruamel.yaml.YAML()
        # Iterate over multiple possible plays in playbook
        for play in step_yaml:
            try:
                # Write play to temp file
                yaml.dump([play], temp_file)
                bzaf_logger.debug('Written content to temp file')
            except Exception as e:
                playbook_file_ready = False
                err = ("Failed to write to temporary file {f}, python "
                       "exception: {p_e}")
                bzaf_logger.error('Failed to write to temp file: {}'.format(e))
                execution_result = execution_result(False, 1, "",
                                                    err.format(f=temp_file,
                                                               p_e=e))
                break
        playbook_file_ready = True
        if playbook_file_ready:
            # Commit changes to file
            temp_file.seek(0)
            # Populate kwargs
            ans_kwargs['private_data_dir'] = '/tmp'
            bzaf_logger.debug("Set private_data_dir to '{}'"
                              .format(ans_kwargs['private_data_dir']))
            ans_kwargs['playbook'] = temp_file_path
            bzaf_logger.debug("Set playbook path to '{}'"
                              .format(temp_file_path))
            ans_kwargs['verbosity'] = 2
            bzaf_logger.debug("Set verbosity level to '{}'"
                              .format(str(ans_kwargs['verbosity'])))

            # If we are on an undercloud , with an overcloud inventory file :)
            # TODO: less static please :)
            if os.path.isfile('/home/stack/bzaf/hosts.yaml'):
                ans_kwargs['inventory'] = '/home/stack/bzaf/hosts.yaml'
                bzaf_logger.debug("Set inventory file to '{}'"
                                  .format(ans_kwargs['inventory']))

            # Execute playbook
            playbook_run = ansible_runner.run(**ans_kwargs)

            if playbook_run.stats['failures']:
                bzaf_logger.error('Failed to execute playbook')
                bzaf_logger.error('Errors: {}'
                                  .format(playbook_run.stats['failures']))
                (playbook_run.stats['failures'])
                execution_successful = False
            else:
                bzaf_logger.debug('Playbook executed successfully')
                execution_successful = True
                playbook_run.stats['failures'] = ''

            # Close and delete temporary file
            temp_file.close()
            # Fix stdout from Ansible playbook execution
            stdout = fix_ansi_list(playbook_run.stdout.readlines())
            execution_result = execution_result(execution_successful,
                                                playbook_run.rc, stdout,
                                                stdout)
        return execution_result
