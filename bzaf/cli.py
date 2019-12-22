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


import argparse
import bzaf.version
from bzaf.utils import bugzilla
from bzaf.utils import logger
from bzaf.utils import summary


def parse_args():
    """
    Parses arguments from user input that will be used during invocation
    """
    parser = argparse.ArgumentParser(description='Bugzilla Auto Verification'
                                                 'Tool')
    parser.add_argument('--debug', help='show debug', action='store_true')
    bz_login_group = parser.add_mutually_exclusive_group(required=False)
    bz_login_group.add_argument('--interactive-login', action='store_true',
                                help='use interactive login if no cached '
                                     'credentials')
    bz_login_group.add_argument('--access-api-key',
                                help='use api token key instead of '
                                     'interactive login')
    parser.add_argument('--private-comments-only', action='store_true',
                        help='Executes spec from private comments only',
                        required=False)
    parser.add_argument('--version', action='version',
                        version=bzaf.version.__version__)
    parser.add_argument('--bugzilla', required=True,
                        help='Bugzilla API entry point to use')
    bz_arg_group = parser.add_mutually_exclusive_group(required=True)
    bz_arg_group.add_argument('--bug-id', action='append',
                              help='Bugzilla bug # to be verified')
    bz_arg_group.add_argument('--bugzilla-query', help='Bugzilla search URL, '
                                                       'provides list of bugs'
                                                       'to be verified')
    parser.add_argument('--current-status', required=True,
                        help='current status for bug to be verified')
    parser.add_argument('--verified-status', required=True,
                        help='set status for bug which verified')
    parser.add_argument('--verified-resolution', required=True,
                        help='set resolution for bug which verified')
    # TODO(vkhitrin: Implement noop logic, execute program without executing
    #                bzaf spec and without updating bug
    # TODO: Consider migrating this argument to a workflow specific to RHOS-QE
    parser.add_argument('--job-env', required=False,
                        help='delimited job env list of strings for '
                             'verification, matching '
                             'between the automation job and bzaf '
                             'verification spec, Example: --job-env \'$dfg,'
                             '3cont_2comp\'')
    return parser.parse_args()


def main():
    # Parse arguments
    args = parse_args()
    # Initi logger
    bzaf_logger = logger.configure_logger(args.debug)
    # Init variables
    valid_bugs = []
    bzurl = args.bugzilla
    access_api_key = args.access_api_key
    bzaf_logger.debug('Set API key to: {}'.format(access_api_key))
    interactive_login = args.interactive_login
    bzaf_logger.debug('Set interactive login to: {}'.format(interactive_login))
    private_comment_only = args.private_comments_only
    bzaf_logger.debug('Set private comments only to: {}'
                      .format(private_comment_only))
    current_status = args.current_status
    bzaf_logger.debug('Set current status to: {}'.format(current_status))
    verified_status = args.verified_status
    bzaf_logger.debug('Set verified status to: {}'.format(verified_status))
    resolution = args.verified_resolution
    bzaf_logger.debug('Set verified resolution to: {}'.format(resolution))
    job_env = args.job_env  # Not generic, consider refactor
    bzaf_logger.debug('Set job_env list to: {}'.format(job_env))

    # Try to connect to bugzilla XMLRPC API endpoint
    bugzilla_instance = bugzilla.discover_bugzilla_endpoint(bzurl,
                                                            access_api_key)

    # Attempt to authenticate with bugzilla instance
    bugzilla.authenticate_with_bugzilla_instance(bugzilla_instance,
                                                 interactive_login)
    # Fetch bugs from bugzilla instance
    bugs = bugzilla.fetch_bugs_from_bugzilla(bugzilla_instance, args.bug_id,
                                             args.bugzilla_query)
    # Discover valid bugs that should be attempted to be verified
    valid_bugs = bugzilla.discover_valid_bugs(bugs, current_status)
    # Display valid bugs to be queried
    summary.valid_bugs_table(valid_bugs)
    # Iterate over valid bugs and attempt to verify
    verified_bugs = bugzilla.verify_valid_bugs(valid_bugs, verified_status,
                                               resolution, bugzilla_instance,
                                               private_comment_only)
    # Prepare execution summary
    summary.prepare_summary(bugs, valid_bugs, verified_bugs)


if __name__ == '__main__':
    main()
