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
import subprocess
from subprocess import Popen
from collections import namedtuple


def run(cmd, rc):

    # Execute command
    shel_run = Popen(cmd.split(), stdout=subprocess.PIPE,
                     stderr=subprocess.PIPE,
                     universal_newlines=True)
    output, errors = shel_run.communicate()

    # If executed return code equals desired return code
    if rc == shel_run.returncode:
        execution_successful = True
        print('SUCCESSFUL CMD: {}, OUTPUT: {}'.format(cmd, output))
    else:
        execution_successful = False
        print('FAILED CMD: {c} OUTPUT: {err}\nRETURN RECIEVED CODE: {r}'
              '\nEXPECTED CODE: {e}'.format(c=cmd,
                                            err=errors,
                                            r=shel_run.returncode,
                                            e=rc))
# create a namedtuple to hold the execution rc and stdout/err
    execution_result = namedtuple('execution_result',
                                  ['execution_sucesfull', 'rc', 'stdout',
                                   'stderr'])
    execution_result = execution_result(execution_successful,
                                        shel_run.returncode, output, errors)
    return execution_result
