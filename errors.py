

class FileDoesNotExistError(Exception):
    """Raised when file is not found in place where it is expected to be.
    """

    def __str__(self):
        return 'File does not exist where it should be'

# Compilation Errors
class CompilationTimeLimitExceededError(Exception):
    """Raised when compilation time limit is exceeded.

    Args:
        given (int): Time of compilation in milliseconds when it was stopped by engine
        expected (int):  Time limit of compilation

    Attributes:
        given (int): Time of compilation in milliseconds when it was stopped by engine
        expected (int):  Time limit of compilation

    """

    def __init__(self, given, expected):
        self.given, self.expected = given, expected

    def __str__(self):
        return 'Compilation timed out - {0} ms ({1} expected ms)'.format(self.given, self.expected)


class CompilationMemoryLimitExceededError(Exception):
    """Raised when compilation memory limit is exceeded.

    Args:
        given (int): Compilation memory use when it was stopped by engine
        expected (int):  Compilation memory limit

    Attributes:
        given (int): Compilation memory use when it was stopped by engine
        expected (int):  Compilation memory limit

    """

    def __init__(self, given, expected):
        self.given, self.expected = given, expected

    def __str__(self):
        return 'Compilation memory limit exceeded - {0} kB ({1} kB expected)'.format(self.given, self.expected)


class CompilationFailedError(Exception):
    """Raised when compilation has not finished successfully.

    Args:
        retuncode (int): Return code of compilation process
        stderr (str): Stderr of compilation process

    Attributes:
        retuncode (int): Return code of compilation process
        stderr (str): Stderr of compilation process

    """

    def __init__(self, returncode, stderr):
        self.returncode, self.stderr = returncode, stderr

    def __str__(self):
        return 'Compilation failed ({0} return code):\n{1}'.format(self.returncode, self.stderr)


# Execution Errors
class ProgramIsNotCompiled(Exception):
    """Raised on attempt to execute program that is not compiled.
    """

    def __str__(self):
        return 'Program has not been compiled yet.'

class ExecutionTimeLimitExceededError(Exception):
    """Raised when execution time limit is exceeded.

    Args:
        given (int): Time of execution in milliseconds when it was stopped by engine
        expected (int):  Time limit of execution

    Attributes:
        given (int): Time of execution in milliseconds when it was stopped by engine
        expected (int):  Time limit of execution

    """
    
    def __init__(self, given, expected):
        self.given, self.expected = given, expected

    def __str__(self):
        return 'Execution timed out - {0} ms ({1} expected ms)'.format(self.given, self.expected)


class ExecutionMemoryLimitExceededError(Exception):
    """Raised when execution memory limit is exceeded.

    Args:
        given (int): Execution memory use when it was stopped by engine
        expected (int):  Execution memory limit

    Attributes:
        given (int): Execution memory use when it was stopped by engine
        expected (int):  Execution memory limit

    """
    
    def __init__(self, given, expected):
        self.given, self.expected = given, expected

    def __str__(self):
        return 'Execution memory limit exceeded - {0} kB ({1} kB expected)'.format(self.given, self.expected)


class ExecutionFailedError(Exception):
    """Raised when execution has not finished successfully.

    Args:
        retuncode (int): Return code of execution process
        stderr (str): Stderr of execution process

    Attributes:
        retuncode (int): Return code of execution process
        stderr (str): Stderr of execution process

    """
    
    def __init__(self, returncode, stderr):
        self.returncode, self.stderr = returncode, stderr

    def __str__(self):
        return 'Execution failed ({0} return code):\n{1}'.format(self.returncode, self.stderr)