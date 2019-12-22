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

import logging


def subscribe_to_logger():
    """
    Subscribes module to general logger
    """
    lg = logging.getLogger(__name__)
    return lg


def configure_logger(debug=False):
    """
    Initializes a logger handler to log events

    Paramas:
        debug - Enable debug mode during invocation
    """
    log_level = logging.FATAL
    if debug:
        log_level = logging.DEBUG
    formatter = logging.Formatter(fmt='%(levelname)s '
                                      '%(module)s %(message)s')
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)

    logger = subscribe_to_logger()
    logger.setLevel(log_level)
    logger.addHandler(handler)
    return logger
