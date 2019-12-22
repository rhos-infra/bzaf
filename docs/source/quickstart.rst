==========
Quickstart
==========

.. note:: In the future, we will ship a private Bugzilla container image that everyone could bring up and test the tool

Installing the tool
===================

Install the tool in a virtual environment from remote master::

    virtualenv venv_bzaf
    source venv_bzaf/bin/activate

    pip install git+https://github.com/rhos-infra/bzaf.git

CLI Invocation Example
======================

Using interactive-login with bugs ID#
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

``bzaf`` allows multiple bugs (``--bug-id``) to be attempted at the same time::

    bzaf --debug --bugzilla \
    https://partner-bugzilla.redhat.com \
    --interactive-login --bug-id 1618759 \
    --current-status ON_QA \
    --verified-status VERIFIED \
    --verified-resolution VERIFIED

Using API key
^^^^^^^^^^^^^

If needed, ``bzaf`` can leverage Bugzilla API key without prompting for credentials::

    export BZAF_API_KEY "YOUR_API_KEY"
    bzaf --debug --bugzilla \
    https://partner-bugzilla.redhat.com \
    --access-api-key $BZAF_API_KEY --bug-id 1618759 \
    --current-status ON_QA \
    --verified-status VERIFIED \
    --verified-resolution VERIFIED

More info on API keys can be found `here <https://bugzilla.readthedocs.io/en/latest/integrating/auth-delegation.html>`_.

Using Bugzilla Query
^^^^^^^^^^^^^^^^^^^^
In some scenarios, the list of bugs need to be verified may change,
we can use a Bugzilla query in order to supply the required bugs::

    export BZAF_QUERY "YOUR_BZAF_QUERY"
    bzaf --debug --bugzilla \
    https://partner-bugzilla.redhat.com \
    --access-api-key $BZAF_API_KEY \
    --current-status ON_QA \
    --verified-status VERIFIED \
    --verified-resolution VERIFIED \
    --bugzilla-query $BZAF_QUERY

Bugzilla query is the same query used in search which appears in the
URL field in the browser.

Infrared Invocation Example
===========================

`Infrared <https://infrared.readthedocs.io/en/latest/>`_ is a
plugin based tool which provides a CLI to Ansible based projects.

``bzaf`` repository contains an infrared plugin which install and
executes the tool.

Once infrared is installed::

    infrared plugin add  https://github.com/rhos-infra/bzaf --src-path infrared
    export BZAF_API_KEY "YOUR_API_KEY"
    export BZAF_QUERY "YOUR_BZAF_QUERY"
    ir bzaf -vv \
    --bzaf_cmd_attrd " --debug --fatal \
    --bugzilla https://partner-bugzilla.redhat.com \
    --access-api-key $BZAF_API_KEY \
    --current-status ON_QA --verified-status VERIFIED --verified-resolution VERIFIED \
    --bugzilla-query $BZAF_QUERY
