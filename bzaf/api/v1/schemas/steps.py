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
import sys
from strictyaml import load, Map, Int, Str

SCHEMA = Map({
    'name': Str(),
    'rc': Int(),
    'cmd': Str(),
    'backend': Str()
})


def validate_steps(spec):
    # Validate each step in spec
    for step in spec:
        try:
            load(step.as_yaml(), SCHEMA)
        # Schema validation failed
        except Exception as e:
            print(e)
            sys.exit(1)
