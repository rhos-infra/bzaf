==========
User Guide
==========

Bugzilla
========

In order to leverage ``bzaf``, a user must have
credentials (username+password or API key) to a bugzilla instance.

Every bugzilla is unique and may contain various different attributes,
the user must be familiar with the bugzilla.

All communication with bugzilla is done through
`python-bugzilla <https://pypi.org/project/python-bugzilla/>`_.

CLI
===

After following the :ref:`installing:Installation Guide`, ``bzaf`` binary will be present.

Arguments
---------

-h, --help
^^^^^^^^^^

**Required**: False

**Description**:  Will display tool's help

**Example**::

  bzaf --help


--debug
^^^^^^^

**Required**: False

**Description**:  Will display additional debug verbose

**Example**::

  bzaf --debug


--fatal
^^^^^^^

**Required**: False

**Description**: Any issue will cause the tool to quit

**Example**::

  bzaf --fatal


--interactive-login
^^^^^^^^^^^^^^^^^^^

**Required**: True, mutually exclusive with ``--access-api-key``

**Description**:  Will prompt the user to enter credentials to
authenticate with bugzilla instance, will not prompt the user to
enter credentials if they're cached

**Example**::

  bzaf --interactive-login


--access-api-key
^^^^^^^^^^^^^^^^

**Required**: True, mutually exclusive with ``--interactive-login``

**Description**: Authenticate with bugzilla instance using an
API key (bugzilla 5+)

**Example**::

  bzaf --access-api-key QRaG8wgBkSGRBJfx5MKNvKMoVpxao2MUxI68MqLo

--version
^^^^^^^^^

**Required**: False

**Description**: Display tool's version

**Example**::

  bzaf --version

--bugzilla
^^^^^^^^^^

**Required**: True

**Mutually exclusive**: False

**Description**: URL of bugzilla instance to authenticate with

**Example**::

  bzaf --bugzilla http://localhost


--bzid
^^^^^^

**Required**: True, mutually exclusive with ``--bz-query``

**Description**: Bugzilla bug ID# to query, multiple arguments
can be provided

**Example**::

  bzaf --bzid 1 --bzid 2

--bz-query
^^^^^^^^^^

**Required**: True, mutually exclusive with ``--bzid``

**Description**: Bugzilla saved/advanced search query to use to query bugs

**Example**::

  bzaf --bz-query http://localhost/buglist.cgi?bug_status=__open__&list_id=2&order=Importance&query_format=specific

--current-status
^^^^^^^^^^^^^^^^

**Required**: True

**Description**: Set state of the bug required to be considered as
potential bug to be verified

**Example**::

  bzaf --current-status OPEN

--verified-status
^^^^^^^^^^^^^^^^^

**Required**: True

**Description**: Set state of bug if it were successfully
verified

**Example**::

  bzaf --verified-status VERIFIED

--verified-resolution
^^^^^^^^^^^^^^^^^^^^^

**Required**: True

**Description**: Set resolution of bug if it were successfully
verified (not required by all states)

**Example**::

  bzaf --verified-resolution FIXED
