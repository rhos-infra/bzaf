=================
How Bzaf Works
=================

Bzaf flow:

- Access a bugzilla instance by api key
- recurse over bz query bugs (or get a single bz):
    - in each bz recurse the comments from last to first:
        - if a valid bzaf spec is found and is in a private comment:
            - try to match "job_env:" (bz comment) parameter list with the supplied ``--job-env`` (bzaf cli command):
                - if there is a match, execute the bzaf spec's commands via the specified backend:
                    - if the execution is succesfull (matches the spec's rc code ("rc:0" ):
                        - verify the bz and put a comment with the commands' execution output.

Caveats :

- bzaf spec comments must be private.
- only the last bzaf spec comment will be checked in each bz.
- to block bzaf from recursing a bz's comments , you can leave the string "``bzaf_skip``" in a private comment.
- bzaf fails and errors are not commented in the bz , only successful runs. (spec validation and commands failures or rc mismatch will not be commented in the bz)

Example BZ verified by bzaf and the CI:
https://bugzilla.redhat.com/show_bug.cgi?id=1719185#c6