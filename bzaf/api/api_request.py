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

from __future__ import print_function
import bzaf.api.backends

print(bzaf.api.backends.BACKENDS)

API_VERSION_HISTORY = """
    1 - Introducing shell backend
"""

MIN_API_VERSION = 1
MAX_API_VERSION = 1


class APIRequest(object):
    """
    A bzaf API request

    Attributes:
        spec: bzaf spec defined
        api_version: Version requested
        verification_stes: Verification steps to perform
        valid: Whether API microversion is valid
        backends: Supported backends for microversion
    """
    def __init__(self, bzaf_spec):
        self.spec = bzaf_spec
        self.api_version = self.spec['version']
        self.verification_steps = self.spec['verification_steps']
        self.valid = False
        self.backends = []

    def is_valid(self):
        if MIN_API_VERSION <= self.api_version <= MAX_API_VERSION:
            self.valid = True
        else:
            print("'{}' is not a valid microversion".format(self.api_version))
        return self.valid

    def detect_backends(self):
        return True

    # def validate_step(self, step):
    #     try:
    #         jsonschema.validate(instance=step, schema=schema)
    #     except jsonschema.exceptions.ValidationError as e:
    #         print('YAML validation failed, {}'.format(e))
    #         return False

    #     if not step['backend'] in backends.EXPOSED_BACKENDS:
    #         print('{} is not part of backends'.format(step['backend']))
    #         return False
    #     return True
