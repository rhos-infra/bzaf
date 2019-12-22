================
Ansible Backend
================

Overview
========

``bzaf`` can execute `ansible <https://www.ansible.com/>`_
playbooks in order to verify bugs.

Ansible is a robust automation platform that we can leverage in
order to execute complex scenarios easily.

Example
=======

Basic scenario
--------------

Execute a single playbook with a single task on localhost:

  .. code-block:: yaml

     bzaf:
       version: 1
       verification_steps:
         - name: ansible test
           backend: ansible
           playbook:
             - hosts: localhost
               tasks:
                 - shell: which openstack

Multi Play Scenario
-------------------

Execute a playbook on several hosts:

  .. code-block:: yaml

     bzaf:
       version: 1
       verification_steps:
         - name: ansible test
           backend: ansible
           playbook:
             - hosts: localhost
               tasks:
                 - shell: which openstack
             - hosts: tester
               tasks:
                 - shell: which ls

Spec
====

**Minimal microversion:** 1

**Maximum microversion:** 1

Attributes
----------

playbook
^^^^^^^^

Ansible playbook (formatted in YAML) that will be executed.
