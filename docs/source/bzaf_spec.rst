========
Overview
========

bzaf Spec
=========
``bzaf`` spec is a YAML based input that is used by the tool
to achieve automatic verification workflow::

  bzaf:
    version: <bzaf_version>
    verification_steps:
      <verification_steps>

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
