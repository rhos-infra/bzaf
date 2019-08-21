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
from pathlib import Path
import inspect
from importlib import import_module
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


# Fix
def import_backends(version):
    backend_modules = []
    backend_classes = []
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
            print(b_c.name)
    return backend_classes
