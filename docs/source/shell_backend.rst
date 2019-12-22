=============
Shell Backend
=============

Overview
========

``bzaf`` can execute shell commands in order to verify bugs.

Shell is the most basic implementation of a backend which is robust and
allows many various robust scenarios to be verified.


Example
=======

Basic scenario
--------------

Execute a single command and expect a return code equal to 0:

  .. code-block:: yaml

    bzaf:
      version: 1
      verification_steps:
        - name: Check existence of command
          backend: shell
          cmd: which openstack
          rc: 0

Negative Testing Scenario
-------------------------

Execute a command and expect to fail with a return code of 1:

  .. code-block:: yaml

    bzaf:
      version: 1
      verification_steps:
        - name: Check existence of command
          backend: shell
          cmd: which openstack
          rc: 1

Multi Step Scenario
-------------------

Execute several commands in serial:

  .. code-block:: yaml

    bzaf:
      version: 1
      verification_steps:
        - name: Check existence of command
          backend: shell
          cmd: which openstack
          rc: 0
        - name: Execute command
          backend: shell
          cmd:  openstack
          rc: 0

Spec
====

**Minimal microversion:** 1

**Maximum microversion:** 1

Attributes
----------

cmd
^^^

Shell command that will be executed.

rc
^^

Expected return code of command execution.
