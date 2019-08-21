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

from bzaf.api.backends import BaseBackend


class AnsibleBackend(BaseBackend):
    def __init__(self, version):
        self.name = 'ansible'
        self.version = version
        self.min_version = 1
        self.max_version = self.min_version
        super(AnsibleBackend, self).__init__(self.name,
                                             self.version,
                                             self.min_version,
                                             self.max_version,
                                             'a',
                                             'a')
