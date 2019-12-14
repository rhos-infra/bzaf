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

# TODO(vkhitrin): Add backend support

from __future__ import print_function
import bzaf.api.backends
import jsonschema

API_VERSION_HISTORY = """
    1 - Introducing shell, ansible backends
"""

MIN_API_VERSION = 1
MAX_API_VERSION = 1
EXPOSED_BACKENDS = bzaf.api.backends.import_backends()


class APIRequest(object):
    """
    A bzaf API request

    Attributes:
        spec: bzaf spec defined
        api_version: Version requested
        verification_stes: Verification steps to perform
        version_valid: Whether API microversion is valid
    """
    def __init__(self, bzaf_spec):
        self.spec = bzaf_spec
        self.api_version = self.spec['version']
        self.verification_steps = self.spec['verification_steps']
        self.version_valid = False
        self.backend_steps = []

    def version_is_valid(self):
        if MIN_API_VERSION <= self.api_version <= MAX_API_VERSION:
            self.version_valid = True
        return self.version_valid

    def backend_is_valid(self, backend):
        requested_backend = backend
        # Check if supplied backend is part of exposed backends
        if requested_backend not in EXPOSED_BACKENDS:
            return False

    def validate_verification_step(self, step):
        verified_backend = step['backend']
        backend_class = EXPOSED_BACKENDS[verified_backend]
        # Construct initial class
        backend_instance = backend_class()
        # Configure required values in class
        backend_instance.version = self.api_version
        backend_instance.step = step
        # Verify a valid invocation of backend
        backend_instance.is_valid()
        backend_instance.validate_schema()
        self.backend_steps.append(backend_instance)
        return True

    def execute_bzaf_request(self):
        for backend_step in self.backend_steps:
            backend_step.execute_backend()
