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
import jsonschema
import yaml


def _validate_initial_bzaf_yaml(bzaf_yaml):
    schema = {
        "type": "object",
        "required": ["bzaf"],
        "properties": {
            "bzaf": {
                "type": "object",
                "required": ["version", "verification_steps"],
                "properties": {
                    "version": {
                        "type": "number"
                    },
                    "verification_steps": {
                        "type": "array"
                    }
                }
            }
        }
    }

    try:
        bzaf_json = yaml.safe_load(bzaf_yaml)
    except yaml.scanner.ScannerError as e:
        # print('Invalid YAML format, {}'.format(e))
        return False

    try:
        jsonschema.validate(instance=bzaf_json, schema=schema)
    except jsonschema.exceptions.ValidationError as e:
        # print('YAML validation failed, {}'.format(e))
        return False
    return True


def validate_bzaf_yaml(bzaf_text):
    # Attempt to validate initial spec
    if _validate_initial_bzaf_yaml(bzaf_text):



class SpecValidator():

    def __init__(self, *args, **kwargs):
        super(SpecValidator, self).__init__(*args, **kwargs)
        self.bzaf_spec = {}
        self.bzaf_microversion = {}

    def parse_spec(bz_text):
        print(bz_text)
