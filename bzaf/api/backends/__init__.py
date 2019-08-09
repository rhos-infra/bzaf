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
from os.path import dirname
import inspect
import pkgutil
import sys


class BaseBackend(object):
    def __init__(self, name, version, min_version, max_version, schema, steps):
        self.name = name
        self.valid = False
        self.version = version
        self.min_version = min_version
        self.max_version = max_version
        self.schema = schema
        self.steps = steps

    def is_valid(self):
        if self.min_version <= self.version <= self.max_version:
            self.valid = True
        print(self.valid)
        return self.valid

    def validate_schema(self):
        print(self.steps)
        pass

    def execute_backend(self):
        pass

# Doesn't work on python3
def import_backends(version):
    backend_modules = []
    backend_classes = []
    directory = dirname(__file__)
    for importer, package_name, _ in pkgutil.iter_modules([directory]):
        full_package_name = '%s.%s' % (directory, package_name)
        if full_package_name not in sys.modules:
            module = importer.find_module(package_name).load_module(full_package_name)
            backend_modules.append(module)
            for b_m in backend_modules:
                for name, obj in inspect.getmembers(b_m):
                    if inspect.isclass(obj) and name != 'BaseBackend':
                        backend_classes.append(obj)
                        test = obj(version)
                        print(test)
                        print(test.is_valid())
    return backend_classes
