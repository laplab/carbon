import os.path
import logging
from colorlog import ColoredFormatter

from errors import *
from helpers import Map
from program import Program


class Engine:
    """Base class of Carbon Engine, highest level of abstraction in module.
    In this class all components are together. Program will be compiled, executed and checked
    for the right answer here.

    """

    def __init__(self, logging_level):
        """Init method of engine.

        Args:
            logging_level (int): Minimal level for logging of events

        """
        # init logging
        handler = logging.StreamHandler()
        handler.setFormatter(
            ColoredFormatter(
                ('%(green)s%(asctime)s%(reset)s ' +
                 '%(cyan)s%(filename)s:%(lineno)d%(reset)s ' +
                 '%(log_color)s%(bold)s%(levelname)-8s%(reset)s ' +
                 '%(log_color)s%(message)s%(reset)s'),
                datefmt=None,
                reset=True,
                log_colors={
                        'DEBUG':    'cyan',
                        'INFO':     'green',
                        'WARNING':  'yellow',
                        'ERROR':    'red',
                        'CRITICAL': 'red',
                },
                secondary_log_colors={},
                style='%'
            )
        )
        self.logger = logging.getLogger('carbon_engine')
        self.logger.addHandler(handler)
        self.logger.setLevel(logging_level)

    def test_program(self, filename, lang_config, input, output, autoremove=False):
        """Checking source code for passing one test.

        Args:
            filename (str): File name of source
            lang_config (dict|Map): Config for Program (see Program's class Attributes for structure)
            input (str): Input to be passed into program STDIN
            output (str): Output expected to be got from program
            autoremove (bool[default=False]): Remove file after execution

        Raises:
            FileDoesNotExistError: File named by filename arg is not found

        """

        # check if file exists
        if not os.path.isfile(filename):
            raise FileDoesNotExistError()

        if not isinstance(lang_config, Map):
            lang_config = Map(lang_config)

        program = Program(filename, lang_config)

        self.logger.info('Compiling {0}...'.format(program.filename))
        try:
            program.compile()
        except Exception as e:
            self.logger.fatal(e)

        self.logger.info('Executing {0}...'.format(program.filename))
        status = Map({'stdout': None})
        try:
            status = program.execute(input, autoremove)
        except Exception as e:
            self.logger.fatal(e)

        self.logger.info('Comparing STDOUT and expected output... ' + str(status.stdout == output))
