#!/usr/bin/env python
"""
Copyright 2019 Vadim Khitrin <me@vkhitrin.com>

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
import os
import re
import ansible_runner
import yaml
from collections import namedtuple


def run(step_playbook):
    # save playbook to file

    with open('/tmp/playbook.yml', 'w') as playbook_outfile:
        playbook_outfile.write(yaml.dump(step_playbook,
                                         default_flow_style=True))
        playbook_outfile.close()
    # run supplied playbook:
    # if we are on an undercloud , with an overcloud inventory file :)
    # TODO: less static please :)
    if os.path.isfile('/home/stack/bzaf/hosts.yaml'):
        playbook_run = ansible_runner.run(
                      inventory='/home/stack/bzaf/hosts.yaml',
                      private_data_dir='/tmp',
                      playbook='/tmp/playbook.yml',
                      verbosity=2)
    else:
        playbook_run = ansible_runner.run(
            private_data_dir='/tmp',
            playbook='/tmp/playbook.yml',
            verbosity=2)

    print("{}: {}".format(playbook_run.status, playbook_run.rc))
    if playbook_run.stats['failures']:
        print(playbook_run.stats['failures'])
        execution_successful = False
    else:
        execution_successful = True
        playbook_run.stats['failures'] = ''

# create a namedtuple to hold the execution rc and stdout/err
    execution_result = namedtuple('execution_result',
                                  ['execution_sucesfull', 'rc', 'stdout',
                                   'stderr'])
    stdout = fix_ansi_list(playbook_run.stdout.readlines())
    execution_result = execution_result(execution_successful,
                                        playbook_run.rc, stdout,
                                        playbook_run.stats['failures'])
    return execution_result


def ansi_escaped(string):
    ansi_escape = re.compile(r'''
    \x1B    # ESC
    [@-_]   # 7-bit C1 Fe
    [0-?]*  # Parameter bytes
    [ -/]*  # Intermediate bytes
    [@-~]   # Final byte
    ''', re.VERBOSE)
    return ansi_escape.sub('', string)


def fix_ansi_list(list_to_fix):
    return list(map(ansi_escaped, list_to_fix))
