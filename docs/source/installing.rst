==================
Installation Guide
==================

Supported Operating Systems
---------------------------

.. note:: bzaf itself does not contain any platform specific code and theoretically can be ran anywhere

The following operating systems were verified:

* RHEL/Fedora
* macOS

Prerequisites
-------------

.. warning:: Only Python3 is supported

bzaf does not contain any special system level requisites.

Make sure Python3 and pip are installed on system level or inside a `virtual environment <https://virtualenv.pypa.io/en/latest/>`_ (recommended).

Installation
------------

Install from source
^^^^^^^^^^^^^^^^^^^

Clone repository from remote::

  git clone https://github.com/rhos-infra/bzaf.git

Install ``bzaf`` from cloned repo::

  cd bzaf
  pip install .

Install from remote
^^^^^^^^^^^^^^^^^^^

.. note:: bzaf is currently not hosted on PyPI

Install from remote repository::

  pip install git+https://github.com/rhos-infra/bzaf.git

Uninstall
^^^^^^^^^

In order to uninstall tool from system::

  pip uninstall bzaf
