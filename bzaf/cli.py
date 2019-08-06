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
import argparse
import bugzilla
import bzaf.version
from bzaf.api import validator
import requests
import logging
import colorlog
import sys
import yaml

logger = logging.getLogger(__name__)


def parse_args():
    parser = argparse.ArgumentParser(description='Bugzilla Auto Verification'
                                                 'Tool')
    parser.add_argument('--debug', help='show debug', action='store_true')
    parser.add_argument('--fatal', help='any error is fatal',
                        action='store_true')
    bz_login_group = parser.add_mutually_exclusive_group(required=True)
    bz_login_group.add_argument('--interactive-login', action='store_true',
                                help='use interactive login if no cached '
                                     'credentials')
    bz_login_group.add_argument('--access-api-key',
                                help='use api token key instead of '
                                     'interactive login')
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
    return parser.parse_args()


def configure_logger(debug=False):
    LOG_FORMAT = '%(log_color)s%(message)s'
    log_level = logging.INFO

    if debug:
        log_level = logging.DEBUG

    logger.setLevel(log_level)

    logger_formatter = colorlog.ColoredFormatter(
        LOG_FORMAT,
        log_colors=dict(
            DEBUG='blue',
            INFO='green',
            WARNING='yellow',
            ERROR='red',
            CRITICAL='bold_red,bg_white',
        )
    )

    sh = logging.StreamHandler()
    sh.setFormatter(logger_formatter)
    logger.addHandler(sh)


def prepare_summary(bugs, valid_bugs, auto_verified_bugs, comments):
    print('*** SUMMARY     ***')
    print('Queried bugs: {}'.format(bugs))
    print('Valid bugs: {}'.format(valid_bugs))
    print('Auto verified bugs: {}'.format(auto_verified_bugs))
    if comments:
        print(comments)
    print('*** SUMMARY END ***')


def main():
    # Init variables
    valid_bugs = []
    auto_verified_bugs = []
    auto_verified_comments = []
    args = parse_args()
    configure_logger(args.debug)
    bzurl = args.bugzilla
    fatal = args.fatal
    if fatal:
        logger.debug('Any error is FATAL, will quit')
    else:
        logger.debug('Will continue if error is not FATAL')
    current_status = args.current_status
    verified_status = args.verified_status
    resolution = args.verified_resolution
    logger.debug('Set current status to: {}'.format(current_status))
    logger.debug('Set verified status to: {}'.format(verified_status))
    logger.debug('Set verified resolution to: {}'.format(resolution))

    # Try to connect to bugzilla XMLRPC API endpoint
    try:
        if args.access_api_key:
            bugzilla_instance = bugzilla.Bugzilla(bzurl,
                                                  api_key=args.access_api_key)
        else:
            bugzilla_instance = bugzilla.Bugzilla(bzurl)
        logger.debug('Bugzilla API URL: {}'.format(bzurl))
    except requests.exceptions.ConnectionError as e:
        logger.debug("{}".format(e))
        logger.error('{} is unreachable'.format(bzurl))
        sys.exit(1)
    except requests.exceptions.HTTPError as e:
        logger.debug("{}".format(e))
        logger.error('Can not connect to {}'.format(bzurl))
        sys.exit(1)
    except bugzilla.BugzillaError as e:
        logger.debug("{}".format(e))
        logger.error('Bugzilla python bindings error, use --debug')
        sys.exit(1)

    # No credentials supplied/cached
    if not bugzilla_instance.logged_in:
        logger.warning("No cached credentials")
        # Interactive login - will cache credentials
        if args.interactive_login:
            try:
                bugzilla_instance.interactive_login()
            except bugzilla.BugzillaError as e:
                logger.debug("{}".format(e))
                if fatal:
                    logger.error('Bugzilla python bindings error, use --debug')
                    sys.exit(1)
                else:
                    logger.warning('Bugzilla python bindings error, '
                                   'use --debug')
        else:
            if fatal:
                logger.error("No credentials to auth, quitting")
                sys.exit(1)
            else:
                logger.warning('No credentials to auth, proceeding with '
                               'limited functionality')

    # init bz,bzs or bzlist from query
    if args.bzid:
        bzids = args.bzid or args.bz_query
    elif args.bz_query:
        bzids = args.bz_query
        query = bugzilla_instance.url_to_query(bzids)
        query["include_fields"] = ["id", "status", "summary", "assigned_to"]
        # set bzids as an object list containing bug objects
        bzids = bugzilla_instance.query(query)

    if bzids:
        # Iterate over Bugzilla bugs #
        for bz in bzids:
            # Attempt to find bug #
            try:
                if args.bzid:
                    bug = bugzilla_instance.getbug(bz)
                elif args.bz_query:
                    bug = bz
                logger.debug('BZ #{b} set to {s}'.format(b=bz, s=bug.status))
                # Check if current bug status equals to status user requested
                if bug.status != current_status:
                    if fatal:
                        logger.error('BZ #{i} status does not match {s}, '
                                     'quitting'.format(i=bz, s=current_status))
                        sys.exit(1)
                    else:
                        logger.warning('BZ #{i} status does not '
                                       'match {s}'.format(i=bz,
                                                          s=current_status))
                else:
                    logger.info('BZ #{} is valid'.format(bz))
                    valid_bugs.append(bug)
            except Exception as e:
                if fatal:
                    logger.error('{}, quitting'.format(e))
                    sys.exit(1)
                else:
                    logger.warning('{}, skipping'.format(e))

        if not valid_bugs:
            logger.error("No valid bugs were found, quitting")
            sys.exit(1)
        logger.info('Proceeding with the following valid BZs:')
        logger.info(valid_bugs)
        # Iterate over valid bugs
        for valid_bug in valid_bugs:
            bzaf_found = False
            comments = valid_bug.getcomments()
            # Iterate over comments in reverse order (from last to first)
            for comment in comments[::-1]:
                if 'bzaf' in comment['text']:
                    bzaf_found = True
                    try:
                        example_spec = """
                        bzaf:
                         version: 1 <- type int
                         steps:
                          backend: 'shell' <- type str
                          cmd: 'echo some_command' <-type str
                          rc: 0 <- type int
                          """
                        logger.info(comment)
                        bzaf_spec = yaml.load(comment['text'])
                        # Temporary check spec YAML according to types
                        # TODO: Move check to spec validation
                        tmp_rc = bzaf_spec['bzaf']['steps']['rc']
                        tmp_cmd = bzaf_spec['bzaf']['steps']['cmd']
                        tmp_backend = bzaf_spec['bzaf']['steps']['backend']
                        tmp_version = bzaf_spec['bzaf']['version']
                        if not (
                            isinstance(tmp_rc, int) and
                            isinstance(tmp_cmd, str) and
                            isinstance(tmp_backend, str) and
                            isinstance(tmp_version, int)
                        ):
                            raise ValueError('error please check yaml types, '
                                             'ex: {}'.format(example_spec))

                        logger.info('BZ #{} Valid bzaf spec '
                                    'found'.format(valid_bug.id))
                        break

                    # Temporary fix: failed to locate bzaf spec in comment
                    except Exception as e:
                        pass
                else:
                    logger.debug('discarding {} no valid bzaf '
                                 'spec'.format(comment))

            if bzaf_found:
                # Execute valid specs
                if validator.execute_spec(bzaf_spec['bzaf']):
                    update_comment = []
                    auto_verified_bugs.append(valid_bug)
                    update_comment.append('All steps completed as expected\n')
                    update_comment.append('Verifying bug as {s} {r}'
                                          .format(s=verified_status,
                                                  r=resolution))
                    update_comment.append('')
                    update_comment.append('Generated by bzaf {}'
                                          .format(bzaf.version.__version__))
                    # Create bug update containing new status and comment
                    update = (bugzilla_instance
                              .build_update(status=verified_status,
                                            comment='\n'.join(update_comment),
                                            resolution=resolution))
                    try:
                        bugzilla_instance.update_bugs(valid_bug.id, update)
                        logger.info('Updated bug {}'.format(valid_bug.id))
                    except Exception as e:
                        logger.error('Failed to Update bug #{b}\n{e}'
                                     .format(b=valid_bug.id, e=e))
                        sys.exit(1)

                else:
                    logger.error("Failed to verify bug")

        # Prepare execution summary
        prepare_summary(len(bzids), len(valid_bugs), len(auto_verified_bugs),
                        auto_verified_comments)


if __name__ == '__main__':
    main()
