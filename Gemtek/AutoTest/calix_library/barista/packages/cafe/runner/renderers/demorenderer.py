__author__ = 'akhanov'

from callbacks import Renderer
from cafe.core.db import get_test_db
from cafe.runner.utilities import get_test_suite_name
from cafe.core.config import get_config
import sys

class DemoRenderer(Renderer):
    """The renderer used currently
    """
    '''
    def end_test_suite(self, func):
        db = get_test_db()
        super(DemoRenderer, self).end_test_suite(func)
        print(db._get_testsuite_report_text(get_test_suite_name(func)))
    '''

    def get_stdout_destination(self):
        """The callback which redirects stdout
        Here we return an object that writes to both a logger, and to stdout if "cafe_runner.show_print_statements" is
        True

        Returns:
            The stream object
        """
        '''
        logger = self.logger

        class logger_stream(object):
            def write(self, contents):
                logger.debug(contents)

        return logger_stream()
        '''
        stdout = sys.stdout
        logger = self.logger

        class stdout_stream(object):
            #NOTE: not to use this class for now to avoid looping of print
            def write(self, contents):
                # REVERT
                sys.stdout = stdout
                logger.info(contents)
                sys.stdout = self

                if get_config().cafe_runner.show_print_statements:
                    stdout.write(contents)

            def flush(self, *args, **kwargs):

                if get_config().cafe_runner.show_print_statements:
                    stdout.flush(*args, **kwargs)

        #return stdout_stream()
        return stdout
