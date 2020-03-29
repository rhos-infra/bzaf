=================
Design Philosophy
=================

Overview
========

The goal of this project is to implement an ‘auto verification’
workflow which aims to be generic and multi-product.

‘auto verification’ is a procedure where an automated CI job will
verify (set bug state as ‘VERIFIED’) relevant bugs.

Auto Verification Workflow
==========================

Bzaf flow example:
==========================

- Access an bugzilla instance by api key
- recurse over bz query bugs (or get a single bz):
    - in each bz recurse the comments from last to first:
        - if a valid bzaf spec is found and is in a private comment:
            - try to match "job_env:" (bz comment) parameter list with the supplied ``--job-env`` (bzaf cli command):
                - if there is a match, execute the bzaf spec's commands via the specified backend:
                    - if the execution is succesfull (matches the spec's rc code ("rc:0" ):
                        - verify the bz and put a comment with the commands' execution output.

Bzaf flow optional tweaks  :

- bzaf executed spec comments may be private.
- only the last valid bzaf spec comment will be executed in each bz.
- to block bzaf from recursing a bz's comments , you can leave the string "``bzaf_skip``" in a private comment.


Step 1 - Bugzilla Bugs Of Interest (“The what”)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Based on a standard, a bug will be marked as ‘Bug Of Interest’.

Marked bugs are at the central of the workflow.

Relevant CI job will go through all marked BZs relevant
to that job and will attempt to perform a user defined logic
in an automated way in order to attempt to verify the bug.
Having some sort of user defined input is beneficial due to:

1. Lowering the barrier of entry - this will allow people from different
backgrounds to set rules which will be performed in an automated way
without being proficient in the workflow.

2. Multi product - will allow various users with many use cases to
leverage single automation.

3. ‘Truly generic’ - define a robust software like interface (set of rules/API)
which will allow automation to scale with use cases without defining hard
coded scenarios.



Step 2 - CI auto-verification Of Bugs Of Interest (“The why”)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

CI is an integral part of product development.

Engineers maintain robust CI infrastructures for their products and strive
to have an automation for each supported use case that is being
provided/sold to the customers/community.

CI is being run and validated on each release which is
deemed as worthy by the engineers.
Leveraging the CI for each release will allow engineers to execute
automation in order to check and validate bugs with
minimal interaction for each release.

Step 3 - auto-verification Procedure (“The how”)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Based on user defined logic, procedures will be executed and will
be handled accordingly.
