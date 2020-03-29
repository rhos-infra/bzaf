==========
About bzaf
==========

``bzaf`` is a python based `Bugzilla <https://www.bugzilla.org/>`_ auto verification tool.

``bzaf``'s main goal is to provide a robust auto verification workflow while
focusing on ease-of-use and simplicity.

``bzaf`` operates by executing auto-verification commands found in a bugzilla
comment to try to verify the said bz.

``bzaf's`` power comes into play when integrated into CI environments, to
create an auto-verification cycle.

.. toctree::
   :maxdepth: 1
   :caption: Installing

   installing

.. toctree::
   :maxdepth: 1
   :caption: Using bzaf

   user_guide
   quickstart

.. toctree::
   :maxdepth: 2
   :caption: bzaf Spec

   bzaf_spec
   bzaf_microversions
   backends

.. toctree::
   :maxdepth: 1
   :caption: Roadmap

   design_philosophy
   roadmap

.. toctree::
   :maxdepth: 1
   :caption: Developing bzaf

   contribution
   developing_backends
