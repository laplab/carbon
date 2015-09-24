import time
import logging
import os
import os.path

from utils import Map
from process import Process
from errors import *


class Program:
    """Program object.

    Attributes:
        logger (Logger): Engine's logger
        config (dict|Map): Configuration of source's programming lang with following structure
            {
                "extension": "cpp",                             # extension of source file
                "compilation": {
                    "need": True,                               # True if compilation is needed
                    "cmd": "g++ -o {filename}.o {filename}",    # terminal command to compile source
                    "executable": "{filename}.o",               # executable name after compilation
                    "limits": {
                        "time": 1000,                           # compilation time limit
                        "vms": 104857600                        # compilation memory limit
                    }
                },
                "execution": {
                    "cmd": "./{filename}",                      # terminal command to execute program
                    "limits": {
                        "time": 1000,                           # execution time limit
                        "vms": 104857600                        # execution memory limit
                    }
                },
                "info": {
                    "lang": "C++"                               # human-readable lang name
                }
            }
        filename (str): File name of source
        compiled (bool): Is program compiled

    """

    def __init__(self, filename, config):
        """Init method of program.

        Args:
            filename (str): File name of source
            config (dict|Map): Configuration object explained in Attributes section of Program class

        Raises:
            FileDoesNotExistError: File named by filename arg is not found

        """

        # check if file exists
        if not os.path.isfile(filename):
            raise FileDoesNotExistError()

        self.filename, self.config = filename, config

        self.logger = logging.getLogger('carbon_engine')

        if not isinstance(self.config, Map):
            self.config = Map(self.config)

        self.compiled = not self.config.compilation.need

    def compile(self):
        """Compiles source and replaces source file with executable.

        Raises:
            CompilationFailedError: If compiler has threw some STDERR of has non-zero return code
            CompilationTimeLimitExceededError: If compilation exceeded time limit
            CompilationMemoryLimitExceededError: If compilation exceeded memory limit
            FileDoesNotExistError: File named by filename arg is not found

        """
        # check if compilation is needed
        if not self.config.compilation.need:
            self.logger.info('Compilation rejected - No need')
            return

        # check if file exists
        if not os.path.isfile(self.filename):
            raise FileDoesNotExistError()

        # compile source
        compiler = Process(cmd=self.config.compilation.cmd.format(filename=self.filename),
                           time_limit=self.config.compilation.limits.time,
                           memory_limit=self.config.compilation.limits.vms)
        compiler.run()

        status = compiler.status
        if status.stderr or status.returncode != 0:
            raise CompilationFailedError(status.returncode, status.stderr)

        if status.time_limit_exceeded:
            raise CompilationTimeLimitExceededError(status.time, compiler.time_limit)

        if status.memory_limit_exceeded:
            raise CompilationMemoryLimitExceededError(status.memory, compiler.memory_limit)

        # remove source file
        os.remove(self.filename)

        # file now changed to binary
        self.filename = self.config.compilation.executable.format(filename=self.filename)

        self.compiled = True

    def execute(self, input, autoremove=False):
        """Executes program and removes it if needed.

        Args:
            input (str): Input to be passed in program's STDIN
            autoremove (bool): Is autoremove of program needed

        Returns:
            Map: Status object of Process class

        Raises:
            ProgramIsNotCompiled: If program is not compiled
            ExecutionFailedError: If program has threw some STDERR or has non-zero return code
            ExecutionTimeLimitExceededError: If execution exceeded time limit
            ExecutionMemoryLimitExceededError: If execution exceeded memory limit
            FileDoesNotExistError: File named by filename parameter of class is not found

        """

        # check if file exists
        if not os.path.isfile(self.filename):
            raise FileDoesNotExistError()

        # check if compiled
        if not self.compiled:
            raise ProgramIsNotCompiled()

        # execute
        program = Process(cmd=self.config.execution.cmd.format(filename=self.filename),
                           input=input,
                           time_limit=self.config.execution.limits.time,
                           memory_limit=self.config.execution.limits.vms)
        program.run()
        
        status = program.status
        if status.stderr or status.returncode != 0:
            raise ExecutionFailedError(status.returncode, status.stderr)

        if status.time_limit_exceeded:
            raise ExecutionTimeLimitExceededError(status.time, program.time_limit)

        if status.memory_limit_exceeded:
            raise ExecutionMemoryLimitExceededError(status.memory, program.memory_limit)

        if autoremove:
            os.remove(self.filename)

        return program.status
