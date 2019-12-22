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

import bugzilla
from bzaf.api import validator
from bzaf.utils import exceptions
from bzaf.utils import logger
import bzaf.version
import requests


bzaf_logger = logger.subscribe_to_logger()


def discover_bugzilla_endpoint(bugzilla_url, api_key=None):
    """
    Attempts to discover if a given URL contains an exposed Bugzilla API

    Parameters:
        bugzilla_url - URL of potential Bugzilla
        api_key - API key to use when attempting to connect to Bugzilla API
    """
    # Try to connect to bugzilla XMLRPC API endpoint
    try:
        bzaf_logger.debug('Bugzilla API URL: {}'.format(bugzilla_url))
        if api_key:
            bugzilla_instance = bugzilla.Bugzilla(bugzilla_url,
                                                  api_key=api_key)
        else:
            bugzilla_instance = bugzilla.Bugzilla(bugzilla_url)
    except requests.exceptions.ConnectionError as e:
        bzaf_logger.debug("{}".format(e))
        raise exceptions.bzafConnectivityException(bugzilla_url)
    except requests.exceptions.HTTPError as e:
        bzaf_logger.debug("{}".format(e))
        raise exceptions.bzafConnectivityException(bugzilla_url)
    except bugzilla.BugzillaError as e:
        bzaf_logger.debug("{}".format(e))
        raise exceptions.bzafBugzillaAPIError()
    return bugzilla_instance


def authenticate_with_bugzilla_instance(bugzilla_instance,
                                        interactive_login=False):
    """
    Authenticate with Bugzilla API

    If bugzilla_instance was created with API key, interactive login is not
    needed

    Parameters:
        bugzilla_instance: Bugzilla instance defined by
                           discover_bugzilla_endpoint function
        interactive_login: Use interactive login to cache credentials
    """
    # No credentials supplied/cached
    if not bugzilla_instance.logged_in:
        bzaf_logger.warning('No cached credentials are present on host, '
                            'supply API key or use interactive-login')
        # Interactive login - will cache credentials
        if interactive_login:
            try:
                bugzilla_instance.interactive_login()
            except bugzilla.BugzillaError as e:
                raise exceptions.bzafLoginError(e)
        else:
            raise exceptions.bzafNoCredentials()


def fetch_bugs_from_bugzilla(bugzilla_instance,
                             bugs_id_list=None,
                             bugzilla_query=None):
    """
    Attempt to fetch bugs from Bugzilla

    Parameters:
        bugzilla_instance: Bugzilla instance defined by
                           discover_bugzilla_endpoint function
        bug_id_list: Bug IDs supplied from user input
        bugzilla_query: Bugs supplied by a Bugzilla query
    """
    # Fields that will be retrieved from bugzilla API
    fields = [
        "id",
        "status",
        "resolution",
        "product",
        "summary",
        "reporter",
        "assigned_to"
    ]
    # Init bugs list from input or query
    fetched_bugs = []
    if bugs_id_list:
        for bug_id in bugs_id_list:
            fetched_bugs.append(bugzilla_instance.getbug
                                (bug_id,
                                 include_fields=fields))
    elif bugzilla_query:
        query = bugzilla_instance.url_to_query(bugzilla_query,
                                               include_fields=fields)
        fetched_bugs = bugzilla_instance.query(query)
    return fetched_bugs


def discover_valid_bugs(bugs, valid_status):
    """
    Iterates over a list of bugs and returns a list of valid bugs

    Parameters:
        bugs - List of bugs retrieved by fetch_bugs_from_bugzilla function
        valid_status - Bug status that is valid during invocation
    """
    # Init valid bugs list
    valid_bugs = []
    for bug in bugs:
        # Check if current bug status equals to status user requested
        if bug.status != valid_status:
            bzaf_logger.debug('BZ #{i} status does not '
                              'match {s}'.format(i=bug.id,
                                                 s=valid_status))
        else:
            bzaf_logger.debug('BZ #{} is valid'.format(bug.id))
            valid_bugs.append(bug)

    # Raise an error if no valid bugs are found
    if not valid_bugs:
        raise exceptions.bzafNoValidBugs()
    return valid_bugs


def add_verification_stdout_to_comment(verification_stdout, update_comment):
    """
    Appends execution output to comment

    Parameters:
        verification_stdout - Output of execution
        update_comment - Comment to be populated with text
    """
    if isinstance(verification_stdout, list):
        update_comment.extend(verification_stdout)
    if isinstance(verification_stdout, str):
        update_comment.append(verification_stdout)


def verify_valid_bugs(valid_bugs, verified_status, verified_resolution,
                      bugzilla_instance, private_comments_only=False):
    """
    Attempts to verify valid bugs

    Parameters:
        valid_bugs - List of bugs from discover_valid_bugs function
        verified_status - Status to set if bug was verified
        verified_resolution - Resolution to set if bug was verified
        bugzilla_instance: Bugzilla instance defined by
                           discover_bugzilla_endpoint function
        private_comments_only - Parse only private comments
    """
    # Init verified bugs list
    verified_bugs = []
    # Iterate over valid bugs
    for valid_bug in valid_bugs:
        bzaf_found = False
        print('\nQuery bug #{}'.format(valid_bug.id))
        comments = valid_bug.getcomments()
        # Iterate over comments in reverse order (from last to first)
        for comment in reversed(comments):
            if private_comments_only:
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
                verified_bugs.append(valid_bug)
                update_comment.append('All steps completed as '
                                      'expected\n')
                update_comment.append('Verifying bug as {s} {r}\n'
                                      .format(s=verified_status,
                                              r=verified_resolution))
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
                           resolution=verified_resolution))
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
    return verified_bugs
