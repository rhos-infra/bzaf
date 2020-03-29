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


import inspect
import jsonschema
import pkgutil
import sys

from bzaf.utils import exceptions
from importlib import import_module
from pathlib import Path


class BaseBackend(object):
    """
    bzaf base backend object

    All backends should inherit from this object

    Attributes:
        name = Backend name
        valid = Whether backend is valid
        version = Requested version from APIRequest object
        min_version = Minimum version allowed for backend
        max_version = Maximum version allowed for backend
        schema = json_schema to be used to verify that the supplied setp
                 is valid according to the backends's requirments
        step - Instructions to perform according to backend
    """
    def __init__(self, name, version, min_version, max_version, schema, step):
        self.name = name
        self.valid = False
        self.version = version
        self.min_version = min_version
        self.max_version = max_version
        self.schema = schema
        self.step = step

    def version_is_valid(self):
        """
        Validates that the requested version is supported by backend

        Returns a boolean represnting if requested version is supported
        """
        if self.min_version <= self.version <= self.max_version:
            self.valid = True
        return self.valid

    def validate_schema(self):
        """
        Validates that the verification step is obeying the required
        schema

        Returns True if backend schema is valid
        """
        try:
            jsonschema.validate(instance=self.step, schema=self.schema)
        except jsonschema.exceptions.ValidationError as e:
            raise exceptions.bzafInvalidSpecException(e)
        return True

    def execute_backend(self):
        """
        Executes backend

        This function should ve overriden by each individual backend

        Returns False if this method is invoked directly and not overriden
        by backend
        """
        print("Unable to execute BaseBackend, please invoke from real backend",
              "or backend does not override 'execute_backend' method")
        return False


def import_backends():
    """
    Imports all valid backends from bzaf/api/backends directory

    All valid backends are inherited from BaseBackend object

    Returns:
        exposed_backends: List of valid backend objects based on inherited
                          from BaseBackend object
    """
    # TODO(vkhitrin): Perform additional checks if imported backend is valid
    # Init variables
    backend_classes = []
    exposed_backends = {}
    # Iterate over files in bzaf/api/backends directory
    for (_, name, _) in pkgutil.iter_modules([Path(__file__).parent]):
        # Import all modules in directory
        imported_module = import_module('.' + name, package=__name__)
        # Iterate over imported modules
        for i in dir(imported_module):
            attribute = getattr(imported_module, i)
            # If class in module inherits from BaseBackend,
            # add to valid backends
            if (
                inspect.isclass(attribute) and
                issubclass(attribute, BaseBackend) and
                attribute != BaseBackend
            ):
                setattr(sys.modules[__name__], name, attribute)
                backend_classes.append(attribute)
        # Expose supported backends
        for b_c in backend_classes:
            backend_instance = b_c()
            backend_name = backend_instance.name
            exposed_backends[backend_name] = b_c
    return exposed_backends
