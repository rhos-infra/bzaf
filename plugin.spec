---
config:
    plugin_type: test
    entry_point: ./infrared/main.yml

subparsers:
    bzaf:
        description: Executes Bzaf auto-verifiation tool
        include_groups: ["Ansible options", "Inventory", "Common options",
                         "Answers file"]
        groups:
            - title: Bzaf command line attributes
              options:
                  bzaf_cmd_attrd:
                      type: Value
                      default: " -h"
                      help: |
                          command line attributes for bzaf:
                          usage: bzaf [-h] [--debug]
                                      (--interactive-login | --access-api-key ACCESS_API_KEY)
                                      [--version] --bugzilla BUGZILLA
                                      (--bzid BZID | --bz-query BZ_QUERY) --current-status
                                      CURRENT_STATUS --verified-status VERIFIED_STATUS
                                      --verified-resolution VERIFIED_RESOLUTION --job-env JOB_ENV

                          Bugzilla Auto VerificationTool

                          optional arguments:
                            -h, --help            show this help message and exit
                            --debug               show debug
                            --interactive-login   use interactive login if no cached credentials
                            --access-api-key ACCESS_API_KEY
                                                  use api token key instead of interactive login
                            --version             show program's version number and exit
                            --bugzilla BUGZILLA   Bugzilla API entry point to use
                            --bug-id BZID           Bugzilla bug # to be verified
                            --bugzilla-query BZ_QUERY   Bugzilla search URL,
                          provides list of bugs tobe
                                                  verified
                            --current-status CURRENT_STATUS
                                                  current status for bug to be verified
                            --verified-status VERIFIED_STATUS
                                                  set status for bug which verified
                            --verified-resolution VERIFIED_RESOLUTION
                                                  set resolution for bug which verified
                            --job-env JOB_ENV     delimited job env list of strings for verification,
                                                  matching between the automation job and bzaf
                                                  verification spec, Example: --job-env
                                                  '$dfg,3cont_2comp'
                  refsec:
                      type: Value
                      help: |
                          specific gerrit patch refsec to
                          checkout, example:
                          --refsec refs/changes/66/665966/7
                      default: ''
