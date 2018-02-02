
__author__ = 'kelvin'

#test all package are installed
#quit if package cannot be found and installed
#from cafe.util.install import main
#main()

import cafe.__main__

from cafe.runner.decorators import test_suite
from cafe.runner.decorators import test_case
from cafe.core.config import get_config
from cafe.topology.topo import get_topology
from cafe.core.utils import get_test_param, Param, param_merge
from cafe.sessions.session_manager import get_session_manager
from cafe.core.db import Testable as Checkpoint
from cafe.core.db import get_test_db
from cafe.core.db import teststep
from cafe.core.utils import set_argv
from cafe.util.helper import load_ts_config
from cafe.util.helper import get_cfs
from cafe.util.helper import literal_eval
from cafe.util.formmap import FormMap
import cafe.runner.parameters.options

from cafe.runner.tctools import register_test_case
from cafe.runner.tctools import get_test_cases

from cafe.runner.tctools import run_test_cases
from cafe.runner.utilities import executing_in_runner
from cafe.runner.parameters.options import load_config_file
from cafe.report.report_runner import ReportRunner

from cafe.runner.utilities import print_console
from cafe.runner.utilities import print_log
from cafe.runner.utilities import print_report

from cafe.app import App
from cafe.util.generators.generator import CafeGeneratorAccessor as Generator
from cafe.util import patches

#from cafe.app import cafebot

#import cafe.__main__