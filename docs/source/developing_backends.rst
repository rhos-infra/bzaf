===================
Developing Backends
===================

.. note:: Backend implementation might be changed/enhanced in the future.

Due to unlimited amount of possible use cases and implementations available,
we want to expose the ability for developers to create custom
:ref:`backends:bzaf Backends`.

Implementation
==============

Currently, all allowed backends must reside in a static
directory ``bzaf/api/backends/``.

Each backend should inherit from ``BaseBackend`` object located in path
``bzaf/api/backends/__init__.py``.

There are several methods there are inherited from ``BaseBackend``, some
of them will be overridden when developing a custom backend.

All backends should accept various attributes that should be validated
according to `JSON schema <https://json-schema.org/>`_, schemas are stored
under the ``bzaf/api/schemas/`` directory.

Developing a custom example backend
===================================

In this section we will create an example backend which executes basic
shell commands.

First we'll create a python file containing our code,
``bzaf/api/backends/example_backend.py``.

We will import all of the required and recommended ``bzaf`` dependencies:

  .. code-block:: python

     # Import BaseBackend
     from bzaf.api.backends import BaseBackend
     # Import JSON schema to be used in validation
     from bzaf.api.schemas.example import schema
     # Import global bzaf logger
     from bzaf.utils import logger

The backend should also subscribe to the global logger in order to allow
debug info:

  .. code-block:: python

     # Subsribe to global logger
     bzaf_logger = logger.subscribe_to_logger()

In the current implementation of backends, we need to create a mock
step that will used during JSON schema validation when constructing
an initial object:

  .. code-block:: python

     # Mock step that will be used when initalizing an initial object
     MOCK_STEP = {
         "cmd": "true",
         "rc": 0
     }

Now we can create our backend object:

  .. code-block:: python

     # Our backend object
     class ExampleBackend(BaseBackend):
         def __init__(self):
             # Name of the backend, will be added to list of exposed backends
             self.name = 'example'
             # Minium microversion that is allowed for the backend
             self.min_version = 1
             # Version requested by user during backend invocation
             self.version = self.min_version
             # Maximum microversion that is allowed for the backend
             # If not defined, we'll be inherit the highest microversion
             # allowed
             self.max_version = self.min_version
             # JSON schema to validate backend
             self.schema = schema
             # Verification step supplied by user
             # When not parsed yet, will use MOCK_STEP
             self.step = MOCK_STEP
             super().__init__(self.name,
                              self.min_version,
                              self.version,
                              self.max_version,
                              self.schema,
                              self.step)

We override ``execute_backend`` method with our backend's logic.

As of now, bzaf requires the backend to return a tuple with the
following keys:

- execution_successful - Bool that represents if the backend
  executed successfully

- output - String/List containing execution output

- errors - String/List containing errors

  .. code-block:: python

     # Overrdie method of BaseBackend
     def execute_backend(self):
         # Parse required arugments
         cmd = self.step['cmd']
         rc = self.step['rc']
         # Execute command
         shell_run = Popen(cmd, stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE,
                           shell=True,
                           universal_newlines=True)
         output, errors = shell_run.communicate()
         s_rc = shell_run.returncode
         # If executed return code equals desired return code
         bzaf_logger.debug('CMD: {}'.format(cmd))
         bzaf_logger.debug('OUTPUT: {}'.format(output).rstrip())
         bzaf_logger.debug('Return code: {}'.format(s_rc))
         if rc == s_rc:
             execution_successful = True
             bzaf_logger.debug('Command executed successfully with the '
                               'expected return code')
         else:
             execution_successful = False
             bzaf_logger.error('Command failed to execute with the '
                               'expected return code')
             bzaf_logger.error('Expected return code: {}'.format(rc))
             if errors:
                 bzaf_logger.error('Error: {}'.format(errors))
         # create a namedtuple to hold
         # the execution rc and stdout/err
         execution_result = namedtuple('execution_result',
                                       ['execution_successful', 'rc', 'stdout',
                                        'stderr'])
         execution_result = execution_result(execution_successful,
                                             s_rc,
                                             output,
                                             errors)
         return execution_result

**View full** :download:`bzaf/api/backends/example_backend.py
<_static/example_backend.py>`.

We will also create a schema file that will validate the backend attributes
supplied by user, ``bzaf/api/schema/example_schema.py``.

  .. code-block:: python

     schema = {
         "type": "object",
         "required": [
             "cmd",
             "rc"
         ],
         "properties": {
             "cmd": {
                 "type": "string"
             },
             "rc": {
                 "type": "integer"
             }
         },
         "additionalProperties": False
     }

**View full** :download:`bzaf/api/backends/example_schema.py
<_static/example_schema.py>`.

Now we will be able to leverage our ``example`` backend in the following way:

  .. code-block:: yaml

    bzaf:
      version: 1
      verification_steps:
        - name: test backend
          backend: example
          cmd: echo test
          rc: 0
