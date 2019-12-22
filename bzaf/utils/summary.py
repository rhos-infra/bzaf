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

from prettytable import PrettyTable


def valid_bugs_table(bugs):
    """
    Prints a table of all valid bugs

    Parameters:
        bugs - List of bugs
    """
    print("Valid bugs:")
    table = PrettyTable()
    table.field_names = [
        'Bug ID',
        'Product',
        'Bug Name',
        'Bug State',
        'Bug Author',
        'Bug Asignee'
    ]
    for bug in bugs:
        table.add_row([bug.id, bug.product, bug.summary, bug.status,
                       bug.reporter, bug.assigned_to])
    print(table)


def verified_bugs_table(verified_bugs):
    """
    Print list of bugs that were verified

    Parameters:
        verified_bugs - List of verified bugs
    """
    print("\nVerified bugs:")
    table = PrettyTable()
    table.field_names = [
        'Bug ID',
        'Product',
        'Bug Name',
        'Bug State',
        'Bug Resolution',
        'Bug Author',
        'Bug Asignee'
    ]
    for bug in verified_bugs:
        table.add_row([bug.id, bug.product, bug.summary, bug.status,
                       bug.resolution, bug.reporter, bug.assigned_to])
    print(table)


def prepare_summary(bugs, valid_bugs, auto_verified_bugs):
    """
    Prints a summary of current invocation

    Parameters:
        bugs - List of bugs
        valid_bugs - List of valid bugs
        verified_bugs - List of verified bugs
    """
    if auto_verified_bugs:
        verified_bugs_table(auto_verified_bugs)
    print('\nTotal queried bugs: {}'.format(len(bugs)))
    print('Valid bugs: {}'.format(len(valid_bugs)))
    print('Auto verified bugs: {}'.format(len(auto_verified_bugs)))
