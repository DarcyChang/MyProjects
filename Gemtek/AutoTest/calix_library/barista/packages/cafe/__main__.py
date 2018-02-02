import threading

__author__ = 'akhanov'

import atexit
import sys
import signal
#from cafe.report.report_runner import ReportRunner
#from cafe.core.config import get_config
#import cafe.core.shutdown


def sigint_handler(sgnl, frame):
    """Callback which handles the SIGINT signal for (in the future) graceful shutdown

    Args:
        sgnl: The caught signal
        frame: The current execution frame

    """
    import cafe.core.shutdown
    shutdown = cafe.core.shutdown.Shutdown
    print(".......Terminating Cafe Execution.......")

    for o in shutdown.get_shutdown_list():
        print("Shutting down '%s'" % o)
        shutdown.shutdown(o)

    sys.exit()


def __exit_handler():
    from cafe.core.config import get_config
    from cafe.core.db import get_test_db
    from cafe.report.report_runner import ReportRunner
    from cafe.sessions.session_manager import SessionManager
    from cafe.core.utils import ParamAttributeError

    config = get_config()

    try:
        # FIX for CAFE-565
        # SessionManager is "Singleton" declared so it should have instance attribute.
        # If it is None, means it is already destructed
        if SessionManager.instance:
            #SessionManager()._stop_session_server()
            SessionManager().close()
            SessionManager.instance = None
    except Exception as e:
        print e

    reports = ReportRunner()

    # ParamAttributeError is raised when config is not loaded - usually because no test suites ran.
    try:
        db = get_test_db()
        reports.run(db, config)
    except ParamAttributeError as e:
        # We can print something, or we can pass
        # print("No Results")
        pass

if __name__ == "__main__":
    import cafe.runner.runner
    cafe.runner.runner.main()
else:
    # from cafe.runner.parameters.options import options
    # options.apply()
    from cafe.outputmanager.outputs import register_streams

    register_streams()
    if threading.current_thread().__class__.__name__ == '_MainThread':
        signal.signal(signal.SIGINT, sigint_handler)
    atexit.register(__exit_handler)
