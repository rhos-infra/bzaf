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


class bzafException(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message


class bzafInvalidSpecException(bzafException):
    def __init__(self, py_err):
        super().__init__(str(py_err))


class bzafInvalidMicroversion(bzafException):
    def __init__(self, microversion):
        message = '{} is not a valid microversion'.format(microversion)
        super().__init__(message)


class bzafInvalidBackend(bzafException):
    def __init__(self, backend):
        message = '{} is not a supported backend'.format(backend)
        super().__init__(message)


class bzafInvalidBackendMicroversion(bzafException):
    def __init__(self, backend, microversion):
        message = '{} is not part of microversion {}'.format(backend,
                                                             microversion)
        super().__init__(message)


class bzafConnectivityException(bzafException):
    def __init__(self, url):
        message = ('Unable to connect to URL {}, view additional errors '
                   'above'.format(url))
        super().__init__(message)


class bzafBugzillaAPIError(bzafException):
    def __init__(self):
        message = ('Bugzilla error, check if destination exposes Bugzilla API'
                   ', view additionl errors above')
        super().__init__(message)


class bzafNoValidBugs(bzafException):
    def __init__(self):
        message = 'No valid bugs were found according to search criteria'
        super().__init__(message)


class bzafLoginError(bzafException):
    def __init__(self, login_exception):
        message = ('Python bugzilla login exception, \n {}'
                   .format(login_exception))
        super().__init__(message)


class bzafNoCredentials(bzafException):
    def __init__(self):
        message = 'Failed to authenticate, no cached bugzilla credentials'
        super().__init__(message)
