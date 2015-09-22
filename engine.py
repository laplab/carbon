import logging
from colorlog import ColoredFormatter

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

    def test_program(self, code, lang_config, input, output):
        """Checking source code for passing one test.

        Args:
            code (str): Source code to be tested
            lang_config (dict|Map): Config for Program (see Program's class Attributes for structure)
            input (str): Input to be passed into program STDIN
            output (str): Output expected to be got from program

        """
        if not isinstance(lang_config, Map):
            lang_config = Map(lang_config)

        program = Program(code, lang_config)

        self.logger.info('\nProgram ({lang}):\n\n{code}\n\nInput: {input}\nOutput: {output}\n'.format(
            lang=lang_config.info.lang, code=code, input=input, output=output))

        self.logger.info('Compiling...')
        try:
            program.compile()
        except Exception as e:
            self.logger.fatal(e)

        self.logger.info('Executing...')
        status = Map({'stdout': None})
        try:
            status = program.execute(input, True)
        except Exception as e:
            self.logger.fatal(e)

        self.logger.info('Comparing STDOUT and expected output... ' + str(status.stdout == output))
        self.logger.info('Finished.\n\n')


if __name__ == "__main__":
    from langs_config import cpp, py
    engine = Engine(logging.DEBUG)

    engine.test_program('a, b = [ int(i for i in input().split(" ")]\nprint(a+b, end="")', py, '4 5', '9')
