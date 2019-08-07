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
import ansible_runner
import yaml


def run(step_playbook):
    # save playbook to file

    with open('/tmp/playbook.yml', 'w') as playbook_outfile:
        playbook_outfile.write(yaml.dump(step_playbook,
                                         default_flow_style=True))
        playbook_outfile.close()
    # run supplied playbook
    playbook_run = ansible_runner.run(private_data_dir='/tmp',
                                      playbook='/tmp/playbook.yml')
    print("{}: {}".format(playbook_run.status, playbook_run.rc))
    if playbook_run.stats['failures']:
        print(playbook_run.stats['failures'])
        return False
    return True
