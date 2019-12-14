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

from __future__ import absolute_import
from bzaf.api.utils import exceptions
from pathlib import Path
import inspect
from importlib import import_module
import jsonschema
import pkgutil
import sys


class BaseBackend(object):
    def __init__(self, name, version, min_version, max_version, schema, step):
        self.name = name
        self.valid = False
        self.version = version
        self.min_version = min_version
        self.max_version = max_version
        self.schema = schema
        self.step = step

    def version_is_valid(self):
        if self.min_version <= self.version <= self.max_version:
            self.valid = True
        return self.valid

    def validate_schema(self):
        try:
            jsonschema.validate(instance=self.step, schema=self.schema)
        except jsonschema.exceptions.ValidationError as e:
            raise exceptions.bzafInvalidSpecException(e)
        return True

    def execute_backend(self):
        print('Unable to execute BaseBackend, please invoke from real backend',
              'or backend does not override \'execute_backend\' method')
        return False


def import_backends():
    backend_classes = []
    exposed_backends = {}
    for (_, name, _) in pkgutil.iter_modules([Path(__file__).parent]):
        imported_module = import_module('.' + name, package=__name__)
        for i in dir(imported_module):
            attribute = getattr(imported_module, i)
            if (inspect.isclass(attribute) and
                    issubclass(attribute, BaseBackend) and
                    attribute != BaseBackend):
                setattr(sys.modules[__name__], name, attribute)
                backend_classes.append(attribute)
        for b_c in backend_classes:
            backend_instance = b_c()
            backend_name = backend_instance.name
            exposed_backends[backend_name] = b_c
    return exposed_backends
