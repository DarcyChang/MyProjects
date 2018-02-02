__author__ = 'akhanov'

from cafe.report.html.html import HTMLReport as html_report
from cafe.report.jira_xml.jira_xml import JIRAXMLReport as jira_xml_report
from cafe.report.console.console import ConsoleReport as console_report
from cafe.report.junit_xml_report.junit_xml_report import JUnitReport as junit_xml_report
from cafe.report.report import Report
from cafe.core.utils import ParamAttributeError

from cafe.core.db import get_test_db
from cafe.core.logger import CLogger as Logger


class ReportRunner(object):
    """Class for running reports defined in the config
    """
    def run(self, db, config):
        """Execute the reports defined in config

        Args:
            db: The database to fetch results from
            config: The configuration tree

        """
        logger = Logger("cafe_runner")

        # try:
        #     report_list = config.cafe_runner.reports
        # except ParamAttributeError:
        #     report_list = []

        if ('cafe_runner' in config) and ('reports' in config.cafe_runner):
            report_list = config.cafe_runner.reports
        else:
            report_list = []

        globs = globals()

        for report in report_list:
            report_good = True

            try:
                report_type = config[report]['__type__']
            except:
                logger.error("Invalid report '%s'" % report)
                report_good = False

            if report_good:
                handler = globs[report_type]

                assert(issubclass(handler, Report))

                report = handler(db, config[report])
                report.generate()
