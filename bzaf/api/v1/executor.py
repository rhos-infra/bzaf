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
from bzaf.api.v1.backends import shell
from bzaf.api.v1.backends import ansible


def execute(spec):
    # Iterate over steps in spec
    # step_name = step['name'].text
    step_backend = spec['steps']['backend']
    step_rc = spec['steps']['rc']
    # Execute command when using 'shell' backend
    if step_backend == 'shell':
        step_cmd = spec['steps']['cmd']
        return shell.run(step_cmd, step_rc)
    if step_backend == 'ansible':
        step_playbook = spec['steps']['playbook']
        return ansible.run(step_playbook)
