========
Overview
========

bzaf Spec
=========
``bzaf`` spec is a YAML based input that is used by the tool
to achieve automatic verification workflow::

    With Shell backend:

    bzaf:
     version: 1
     job_env: pidone,3cont_2comp,$product_version?
     steps:
      backend: 'shell'
      cmd: 'rpm_compare resource-agents-4.1.1-33.el8.x86_64'
      name: first step
      rc: 0

    With Ansible backend:

      bzaf:
      version: 1
      job_env: 'pidone,3cont_2comp,$product_version?'
      steps:
        backend: 'ansible'
        playbook:
         - hosts: controller
           become: true
           tasks:
             - name: check_pacemaker rpm
               shell: |
                   rpm_compare pacemaker-2.0.2-3.el8.x86_64
        name: first step
        rc: 0

Goals of ``bzaf`` spec:

* Human readable and machine readable
* Extendable
* Robust

bzaf Microversions
==================

.. image:: _static/bzaf_microversion.png

`bzaf` uses the concept of microversions in order to expose the
available capabilities to the user.

At it's core, `bzaf` is being designed as an automatic workflow that is part
of a product's CI.
This requires the tool to be backwards compatible while exposing
new capabilities without breaking new and old scenarios.

Each microversion will contain it's set of capabilities, refer to
:ref:`bzaf_microversions:Microversions` to learn more.
