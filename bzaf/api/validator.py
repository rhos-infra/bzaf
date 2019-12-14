#!/usr/bin/env python
"""
Copyright 2019 Vadim Khitrin <me@vkhitrin.com>
               Pini Komarov  <pkomarov@redhat.com>

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

from bzaf.api import api_request
from bzaf.api.schemas.bzaf import schema as bzaf_schema
from bzaf.api.schemas.verification_step import schema as step_schema
from bzaf.api.utils import exceptions
import jsonschema
import yaml


def validate_initial_bzaf_yaml(bzaf_yaml):
    try:
        bzaf_json = yaml.safe_load(bzaf_yaml)
    except yaml.scanner.ScannerError as e:
        raise exceptions.bzafInvalidSpecException(e)
    except yaml.parser.ParserError as e:
        raise exceptions.bzafInvalidSpecException(e)
    try:
        jsonschema.validate(instance=bzaf_json, schema=bzaf_schema)
    except jsonschema.exceptions.ValidationError as e:
        raise exceptions.bzafInvalidSpecException(e)
    return bzaf_json['bzaf']


def validate_bzaf_version(bzaf_api_request):
    if not bzaf_api_request.api_version_is_valid():
        raise exceptions.bzafInvalidMicroversion(bzaf_api_request.api_version)
    return True


def validate_verifications_steps(bzaf_api_request):
    steps = bzaf_api_request.verification_steps
    for step in steps:
        step_backend = step['backend']
        try:
            jsonschema.validate(instance=step, schema=step_schema)
        except jsonschema.exceptions.ValidationError as e:
            raise exceptions.bzafInvalidSpecException(e)
        if not bzaf_api_request.backend_is_valid(step_backend):
            raise exceptions.bzafInvalidBackend(step_backend)
        bzaf_api_request.validate_verification_step(step)


def validate_bzaf_yaml(bzaf_text):
    """
    Attempt to validate bzaf spec fetched from comment

    :param bzaf_text - Text containing potential spec to be validated
    """
    # Attempt to validate initial spec
    try:
        bzaf_spec = validate_initial_bzaf_yaml(bzaf_text)
    except exceptions.bzafInvalidSpecException as e:
        print(e)
        request = False
    # If spec is verifeid, create bzaf API request
    request = api_request.APIRequest(bzaf_spec)
    # Attempt to validate if microversion is supported
    try:
        validate_bzaf_version(request)
    except exceptions.bzafInvalidMicroversion as e:
        print(e)
        request = False
    # Validate verifications steps
    try:
        validate_verifications_steps(request)
    except exceptions.bzafInvalidSpecException as e:
        print(e)
        request = False
    except exceptions.bzafInvalidBackend as e:
        print(e)
        request = False
    except exceptions.bzafInvalidBackendMicroversion as e:
        print(e)
        request = False
    return request
