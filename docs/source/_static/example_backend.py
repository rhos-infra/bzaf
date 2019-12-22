# Import BaseBackend
from bzaf.api.backends import BaseBackend
# Import JSON schema to be used in validation
from bzaf.api.schemas.example import schema
# Import global bzaf logger
from bzaf.utils import logger

# Subsribe to global logger
bzaf_logger = logger.subscribe_to_logger()

# Mock step that will be used when initalizing an initial object
MOCK_STEP = {
    "cmd": "true",
    "rc": 0
}


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
