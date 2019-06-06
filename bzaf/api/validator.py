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
from bzaf.api import v1
from strictyaml import load, Map, Int, as_document
import sys


SCHEME = Map({'version': Int()})

SUPPORTED_VERSIONS = {
                        1: v1
                     }


def _get_spec_version(version_string):
    version = int(version_string.text)
    return version


def validate_initial_spec(spec):
    # Check if version in present in spec
    if 'version' in spec:
        version_dict = as_document({'version': spec['version'].text})
    try:
        load(version_dict.as_yaml(), SCHEME)
        version = _get_spec_version(spec['version'])

    except Exception as e:
        print(e)
        sys.exit(1)

    # Check if version is supported
    if version in SUPPORTED_VERSIONS:
        print('version {} is supported :)'.format(version))
    else:
        print('version {} is not supported'.format(version))
        sys.exit(1)

    # Copy spec and remove version
    modified_spec = as_document(spec.data)
    del modified_spec['version']
    # Continue validating spec based on version
    SUPPORTED_VERSIONS[version].spec.validate(modified_spec)


def execute_spec(spec):
    version = _get_spec_version(spec['version'])
    # Copy spec and remove version
    modified_spec = as_document(spec.data)
    del modified_spec['version']
    # Executed validated spec based on version
    if SUPPORTED_VERSIONS[version].executor.execute(modified_spec):
        return True
    else:
        return False
