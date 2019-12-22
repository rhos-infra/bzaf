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
import bugzilla
import bzaf.version
from bzaf.api import validator
from bzaf.utils import exceptions
from bzaf.utils import logger
from bzaf.utils import summary
import requests


def parse_args():
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
    bz_arg_group.add_argument('--bzid', action='append',
                              help='Bugzilla bug # to be verified')
    bz_arg_group.add_argument('--bz-query', help='Bugzilla search URL, '
                                                 'provides list of bugs to'
                                                 'be verified')
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


def add_verification_stdout_to_comment(verification_stdout, update_comment):
    if isinstance(verification_stdout, list):
        update_comment.extend(verification_stdout)
    if isinstance(verification_stdout, str):
        update_comment.append(verification_stdout)


def main():
    # Parse arguments
    args = parse_args()
    # Initi logger
    bzaf_logger = logger.configure_logger(args.debug)
    # Init variables
    query_fields = [
        "id",
        "status",
        "resolution",
        "product",
        "summary",
        "reporter",
        "assigned_to"
    ]
    valid_bugs = []
    auto_verified_bugs = []
    bzurl = args.bugzilla
    private_comment_only = args.private_comments_only
    current_status = args.current_status
    verified_status = args.verified_status
    resolution = args.verified_resolution
    job_env = args.job_env  # Not generic, consider refactor
    bzaf_logger.debug('Set current status to: {}'.format(current_status))
    bzaf_logger.debug('Set verified status to: {}'.format(verified_status))
    bzaf_logger.debug('Set verified resolution to: {}'.format(resolution))
    bzaf_logger.debug('Set job_env list to: {}'.format(job_env))

    # Try to connect to bugzilla XMLRPC API endpoint
    try:
        bzaf_logger.debug('Bugzilla API URL: {}'.format(bzurl))
        if args.access_api_key:
            bugzilla_instance = bugzilla.Bugzilla(bzurl,
                                                  api_key=args.access_api_key)
        else:
            bugzilla_instance = bugzilla.Bugzilla(bzurl)
    except requests.exceptions.ConnectionError as e:
        bzaf_logger.debug("{}".format(e))
        raise exceptions.bzafConnectivityException(bzurl)
    except requests.exceptions.HTTPError as e:
        bzaf_logger.debug("{}".format(e))
        raise exceptions.bzafConnectivityException(bzurl)
    except bugzilla.BugzillaError as e:
        bzaf_logger.debug("{}".format(e))
        raise exceptions.bzafBugzillaAPIError()

    # No credentials supplied/cached
    if not bugzilla_instance.logged_in:
        bzaf_logger.warning('No cached credentials are present on host, '
                            'supply API key or use interactive-login')
        # Interactive login - will cache credentials
        if args.interactive_login:
            try:
                bugzilla_instance.interactive_login()
            except bugzilla.BugzillaError as e:
                raise exceptions.bzafLoginError(e)
        else:
            raise exceptions.bzafNoCredentials()

    # Init bugs list from input or query
    if args.bzid:
        bzids = args.bzid
    elif args.bz_query:
        bzids = args.bz_query
        query = bugzilla_instance.url_to_query(bzids)
        query["include_fields"] = query_fields
        # set bzids as an object list containing bug objects
        bzids = bugzilla_instance.query(query)

    # Proceed if received bugs
    if bzids:
        # Iterate over Bugzilla bugs
        for bz in bzids:
            # Attempt to query bug
            try:
                # If received bug ID from user, querried bug
                if args.bzid:
                    bug = bugzilla_instance.getbug(bz,
                                                   include_fields=query_fields)
                # Use previously querried bugs if supplied by a query
                elif args.bz_query:
                    bug = bz
                bzaf_logger.debug('BZ #{b} set to {s}'.format(b=bz,
                                                              s=bug.status))
                # Check if current bug status equals to status user requested
                if bug.status != current_status:
                    bzaf_logger.debug('BZ #{i} status does not '
                                      'match {s}'.format(i=bz,
                                                         s=current_status))
                else:
                    bzaf_logger.debug('BZ #{} is valid'.format(bz))
                    valid_bugs.append(bug)
            except Exception as e:
                bzaf_logger.debug('Bug #{bi} is not valid, '
                                  'reason: {err}'.format(bi=bz,
                                                         err=e))

        # Raise an error if no valid bugs are found
        if not valid_bugs:
            raise exceptions.bzafNoValidBugs()

        # Display valid bugs to be querried
        summary.valid_bugs_table(valid_bugs)
        # Iterate over valid bugs
        for valid_bug in valid_bugs:
            bzaf_found = False
            print('\nQuery bug #{}'.format(valid_bug.id))
            comments = valid_bug.getcomments()
            # Iterate over comments in reverse order (from last to first)
            for comment in reversed(comments):
                if private_comment_only:
                    if not comment['is_private']:
                        bzaf_logger.error('Can not parse from non private '
                                          'comment #{}'
                                          .format(comment['count']))
                        continue
                text = comment['text']
                bzaf_logger.debug('Iterrating over comment #{}'
                                  .format(comment['count']))
                # Attempt to validate comment according to BZAF spec
                bzaf_request = validator.validate_bzaf_yaml(text)
                if bzaf_request:
                    print('Valid spec was found')
                    bzaf_found = True
                    break

            # If valid bzaf spec located in comment, attempt to execute it
            if bzaf_found:
                # Execute according to bzaf request
                bzaf_execution = bzaf_request.execute_bzaf_request()
                # If executed successfully
                if bzaf_execution:
                    print('Spec was executed successfully')
                    update_comment = []
                    auto_verified_bugs.append(valid_bug)
                    update_comment.append('All steps completed as '
                                          'expected\n')
                    update_comment.append('Verifying bug as {s} {r}\n'
                                          .format(s=verified_status,
                                                  r=resolution))
                    update_comment.append('Verification commands '
                                          'output:\n')
                    add_verification_stdout_to_comment(
                                 bzaf_execution.stdout, update_comment)
                    update_comment.append('')
                    update_comment.append('Generated by bzaf {}'.format
                                          (bzaf.version.__version__))
                    # Create bug update containing new status and comment
                    update = (bugzilla_instance.build_update
                              (status=verified_status,
                               comment='\n'.join(update_comment),
                               resolution=resolution))
                    try:
                        bugzilla_instance.update_bugs(valid_bug.id, update)
                        bzaf_logger.debug('Updated bug #{}'
                                          .format(valid_bug.id))
                    except Exception as e:
                        bzaf_logger.error('Failed to Update bug #{b}\n{e}'
                                          .format(b=valid_bug.id, e=e))
                    # Refresh local cache with current bug details
                    valid_bug.refresh()

            else:
                print('No valid spec was found')

        # Prepare execution summary
        summary.prepare_summary(bzids, valid_bugs, auto_verified_bugs)


if __name__ == '__main__':
    main()
