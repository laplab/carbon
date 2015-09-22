import shlex
from subprocess import Popen, PIPE, TimeoutExpired
from queue import Queue, Empty
from threading import Thread
import psutil
import time

from helpers import Map


class Process:
    """Allows to run processes with limits

    Attributes:
        cmd (str): Command to execute
        input (Optional[str]): Input to be passed to processes STDIN
        time_limit (Optional[int]): Time limit in milliseconds
        memory_limit (Optional[int]): Memory limit in kB
        stdout_file (Optional[str]): Name of file STDOUT should be written to
        stderr_file (Optional[str]): Name of file STDERR should be written to
        process (Popen): Popen process object
        status (Map): Current status of program including
            time_limit_exceeded (bool): Is time limit exceeded
            memory_limit_exceeded (bool): Is memory limit exceeded
            stdout (str): All STDOUT of process
            stderr (str): All STDERR of process
            time (int): Execution time on milliseconds. This attribute is None until process finished.
            memory (int): Maximum memory use in kB. This attribute is None until process finished.
            retuncode (int): Return code of process. This attribute is None until process finished.

    """

    def __init__(self, cmd, input=None, time_limit=None, memory_limit=None, stdout_file=None, stderr_file=None):
        """Init method of process

        Args:
            cmd (str): Command to execute
            input (Optional[str]): Input to be passed to processes STDIN
            time_limit (Optional[int]): Time limit in milliseconds
            memory_limit (Optional[int]): Memory limit in kB
            stdout_file (Optional[str]): Name of file STDOUT should be written to
            stderr_file (Optional[str]): Name of file STDERR should be written to

        """
        self.cmd, self.input, self.time_limit, self.memory_limit, self.stdout_file, self.stderr_file\
            = shlex.split(cmd), input, time_limit, memory_limit, stdout_file, stderr_file

        if self.input:
            self.input = self.input.encode('UTF-8')

        self.process = None

        # status variables
        self.status = Map()
        self.status.time_limit_exceeded = False
        self.status.memory_limit_exceeded = False

        self.status.stdout = None
        self.status.stderr = None
        self.status.time = None
        self.status.memory = None
        self.status.returncode = None

    def run(self):
        """Runs process with configuration set.

        """
        self.process = Popen(self.cmd, stdin=PIPE, stdout=PIPE, stderr=PIPE)
        psutil_process = psutil.Process(self.process.pid)

        # pause process to allow bootstrap code execute before it
        psutil_process.suspend()

        stdout_summary = ''
        stderr_summary = ''

        if self.memory_limit is None:
            try:
                psutil_process.resume()
                start = time.time()
                (stdout_summary, stderr_summary) = self.process.communicate(self.input, self.time_limit)
                # strange line
                self.status.time = time.time() - start
                self.status.returncode = self.process.poll()
            except TimeoutExpired:
                self.status.time_limit_exceeded = True
                self.process.kill()
        else:
            def enqueue_output(out, queue):
                for line in iter(out.readline, b''):
                    queue.put(line)
                out.close()

            stdout_queue = Queue()
            stdout_thread = Thread(target=enqueue_output, args=(self.process.stdout, stdout_queue))
            stdout_thread.daemon = True
            stdout_thread.start()

            stderr_queue = Queue()
            stderr_thread = Thread(target=enqueue_output, args=(self.process.stderr, stderr_queue))
            stderr_thread.daemon = True
            stderr_thread.start()

            max_mem = 0

            # start timer
            start = time.time()

            # bootstrap finished, resume
            psutil_process.resume()

            # write data to STDIN of program
            if self.input:
                try:
                    self.process.stdin.write(self.input)
                    self.process.stdin.close()
                except BrokenPipeError:
                    pass  # program does not accept any STDIN

            # start main cycle
            while time.time() - start <= (self.time_limit or float('inf')):
                max_mem = max(max_mem, psutil_process.memory_info().vms)
                # Memory limit exceeded
                if max_mem > self.memory_limit:
                    self.status.memory_limit_exceeded = True
                    break

                # process finished
                if self.process.poll() is not None:
                    self.status.returncode = self.process.returncode
                    break

            # Time limit exceeded
            if self.status.returncode is None:
                if not self.status.memory_limit_exceeded:
                    self.status.time_limit_exceeded = True
                self.process.kill()

            self.status.time = round((time.time() - start) * 1000)
            self.status.memory = max_mem / 1024

            stdout_thread.join()
            stderr_thread.join()

            # get lost STDOUT
            to_file = isinstance(self.stdout_file, str)
            if to_file:
                f = open(self.stdout_file, 'w')
            while True:
                try:
                    line = stdout_queue.get_nowait().decode('UTF-8')
                except Empty:
                    break
                else:
                    if to_file:
                        f.write(line)
                    stdout_summary += line
            if to_file:
                f.close()

            # get lost STDERR
            to_file = isinstance(self.stderr_file, str)
            if to_file:
                f = open(self.stderr_file, 'w')
            while True:
                try:
                    line = stderr_queue.get_nowait().decode('UTF-8')
                except Empty:
                    break
                else:
                    if to_file:
                        f.write(line)
                    stderr_summary += line
            if to_file:
                f.close()

        # save STDOUT and STDERR to class vars
        if stdout_summary:
            self.status.stdout = stdout_summary
        if stderr_summary:
            self.status.stderr = stderr_summary