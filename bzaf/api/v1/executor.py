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


def execute(spec):
    # Iterate over steps in spec
    for step in spec['steps']:
        for step_attr in  spec['steps'][step]:
            step_name = spec['steps'][step]['name']
            step_backend = spec['steps'][step]['backend']
            step_cmd = spec['steps'][step]['cmd']
            step_rc = spec['steps'][step]['rc']
            # Execute command when using 'shell' backend
        if step_backend == 'shell':
            result = shell.run(step_cmd, step_rc)
            if not result:
                return False
    return True
