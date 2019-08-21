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
from bzaf.api import api_request
from bzaf.api.schemas.bzaf import schema as bzaf_schema
import jsonschema
import yaml


def validate_initial_bzaf_yaml(bzaf_yaml):
    try:
        bzaf_json = yaml.safe_load(bzaf_yaml)
    except yaml.scanner.ScannerError as e:
        print('Invalid YAML format, {}'.format(e))
        return False
    except yaml.parser.ParserError as e:
        print('Text is not in YAML format, {}'.format(e))
        return False

    try:
        jsonschema.validate(instance=bzaf_json, schema=bzaf_schema)
    except jsonschema.exceptions.ValidationError as e:
        print('YAML validation failed, {}'.format(e))
        return False

    return bzaf_json['bzaf']


def validate_bzaf_version(spec):
    request = api_request.APIRequest(spec) if spec else False
    return request if (
        isinstance(request, api_request.APIRequest) and request.is_valid()
    ) else False


def validate_bzaf_yaml(bzaf_text):
    """
    Attempt to validate bzaf spec fetched from comment

    :param bzaf_text - Text containing potential spec to be validated
    """
    # Attempt to validate initial spec
    bzaf_spec = validate_initial_bzaf_yaml(bzaf_text)
    # Attempt to validate if microversion is supported
    api_request = validate_bzaf_version(bzaf_spec)
    return api_request
