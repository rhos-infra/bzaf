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

from bzaf.api import api_request
from bzaf.api.schemas.bzaf import schema as bzaf_schema
from bzaf.api.schemas.verification_step import schema as step_schema
from bzaf.utils import exceptions
from bzaf.utils import logger
import jsonschema
import yaml

bzaf_logger = logger.subscribe_to_logger()


def validate_initial_bzaf_yaml(bzaf_text):
    """
    Performs initial validation of supplied text, checks if text is a valid
    bzaf spec

    Parameters:
        bzaf_text - Text parsed from comment

    Returns a JSON object if initial spec has passed schema validation
    """
    # Attempt to parse YAML from comment
    try:
        bzaf_json = yaml.safe_load(bzaf_text)
    except yaml.scanner.ScannerError as e:
        raise exceptions.bzafInvalidSpecException(e)
    except yaml.parser.ParserError as e:
        raise exceptions.bzafInvalidSpecException(e)
    # Attempt to validate YAML according to schema
    try:
        jsonschema.validate(instance=bzaf_json, schema=bzaf_schema)
    except jsonschema.exceptions.ValidationError as e:
        raise exceptions.bzafInvalidSpecException(e)
    return bzaf_json['bzaf']


def validate_bzaf_version(bzaf_api_request):
    """
    Validates supplied bzaf spec version

    Parameters:
        bzaf_api_request - bzaf API request object

    Returns true if requested API version is valid
    """
    if not bzaf_api_request.api_version_is_valid():
        raise exceptions.bzafInvalidMicroversion(bzaf_api_request.api_version)
    return True


def validate_verifications_steps(bzaf_api_request):
    """
    Validates verification_steps from bzaf spec

    Parameters:
        bzaf_api_request - bzaf API request object
    """
    steps = bzaf_api_request.verification_steps
    # Iterate over steps in bzaf spec
    for step in steps:
        step_backend = step['backend']
        # Attempt to validate step according to schema
        try:
            jsonschema.validate(instance=step, schema=step_schema)
        except jsonschema.exceptions.ValidationError as e:
            raise exceptions.bzafInvalidSpecException(e)

        if not bzaf_api_request.backend_is_valid(step_backend):
            raise exceptions.bzafInvalidBackend(step_backend)
        bzaf_api_request.validate_verification_step(step)


def validate_bzaf_job_env(bzaf_api_request, requested_job_env):
    """
    Attempt to validate bzaf job_env fetched from request
    Parameters:
    bzaf_api_request - bzaf API request object (Bug side)
    requested_job_env - job_env requested by user (CI side)
    Only If ALL items in the bug_job_env_list are present in the
    requested_job_env_list , then we have a match for verification.
    """

    bug_job_env = bzaf_api_request.job_env
    bug_job_env_list = bzaf_api_request.job_env.split(",")
    requested_job_env_list = requested_job_env.split(",")
    # check if all elements in bug_job_env_list are in requested_job_env_list:
    if not all(elm in requested_job_env_list for elm in bug_job_env_list):
        raise exceptions.bzafInvalidJobEnv(requested_job_env, bug_job_env)


def validate_bzaf_yaml(comment_text, requested_job_env):
    """
    Attempt to validate bzaf spec fetched from comment

    Parameters:
        comment_text - Text containing potential spec to be validated
        job_env - job_env requested by user

    Returns:
        request: bzaf API request
    """
    # Attempt to validate initial spec
    try:
        bzaf_spec = validate_initial_bzaf_yaml(comment_text)
        # If spec is verifeid, create bzaf API request
        request = bzaf_request = api_request.APIRequest(bzaf_spec)
        # Attempt to validate if microversion is supported
        try:
            validate_bzaf_version(bzaf_request)
        except exceptions.bzafInvalidMicroversion as e:
            bzaf_logger.debug(e)
            request = False
        # Validate job_env
        try:
            validate_bzaf_job_env(bzaf_request, requested_job_env)
        except exceptions.bzafInvalidJobEnv as e:
            bzaf_logger.debug(e)
            request = False
        # Validate verifications steps
        try:
            validate_verifications_steps(bzaf_request)
        except exceptions.bzafInvalidSpecException as e:
            bzaf_logger.debug(e)
            request = False
        except exceptions.bzafInvalidBackend as e:
            bzaf_logger.debug(e)
            request = False
        except exceptions.bzafInvalidBackendMicroversion as e:
            bzaf_logger.debug(e)
            request = False
    except exceptions.bzafInvalidSpecException:
        request = False
        bzaf_logger.debug('No valid spec found in comment')
    return request
