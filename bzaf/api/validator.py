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


def validate_job_env(spec, args_job_env, logger):
    spec_job_env_list = spec['bzaf']['job_env'].split(',')
    if all(spec_job_env_str in args_job_env for spec_job_env_str
           in spec_job_env_list):
        logger.info('All spec_job_env_list: {} are matched in '
                    'args_job_env: {} ,  we can continue with '
                    'auto verification..'
                    .format(spec_job_env_list, args_job_env))
        return True
    else:
        logger.info('Not all spec_job_env_list: {} are matched in '
                    'args.job_env: {}, we can\'t continue with '
                    'auto verification..'
                    .format(spec_job_env_list, args_job_env))
        return False


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


def validate_spec_types(spec):
    # Temporary check spec YAML according to types

    example_spec = """
    bzaf:
     version: 1 <- type int
     job_env: pidone,3cont_2comp  <- type comma delimited str (i.e.:dfg,
     job_topology)
     steps:
      backend: 'shell' <- type str
      cmd: 'echo some_command' <-type str
      rc: 0 <- type int
      name: 'first step'
    # or using an ansible backend:
    bzaf:
     version: 1 <- type int
     job_env: pidone,3cont_2comp  <- type comma delimited str (i.e.:dfg,
     job_topology)
     steps:
      backend: 'ansible' <- type str
      playbook: <-type yaml str
         - hosts: localhost
           tasks:
             - name: bla
               shell: |
               echo "bzaf rules!"
      name: 'first step'
      rc: 0 <- type int"""

    tmp_backend = spec['bzaf']['steps']['backend']
    if tmp_backend == 'shell':
        backend_args = spec['bzaf']['steps']['cmd']
    elif tmp_backend == 'ansible':
        backend_args = spec['bzaf']['steps']['playbook']
    tmp_rc = spec['bzaf']['steps']['rc']
    tmp_version = spec['bzaf']['version']
    job_env = spec['bzaf']['job_env']

# Todo: add individual spec verifications here
    if not (
            isinstance(tmp_rc, int) and
            isinstance(backend_args, (str, list)) and
            isinstance(tmp_backend, str) and
            isinstance(tmp_version, int) and
            isinstance(job_env, str)

    ):
        raise ValueError('error please check yaml types, '
                         'Example: {}'.format(example_spec))
    return True


def execute_spec(spec):

    if v1.executor.execute(spec):
        return True
    else:
        return False
