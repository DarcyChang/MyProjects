__author__ = 'akhanov'

from cafe.report.report import Report
from cafe.core import db
from cafe.core.utils import create_folder
import tarfile
import os
from lxml import etree


class JIRAXMLReport(Report):
    """Module for generating a JIRA XML Report
    """
    def generate(self):
        """Generate the JIRA XML Report based on results in the DB
        Creates JIRA XML files in path specified by runner settings
        By default, archives them into a .tar.gz file
        And, by default, deletes the generated XML files after
        creating the archive
        """
        # Get the config
        conf = self._config

        # Keep track of filenames for archiving
        filenames = []

        # Each XML file will containe one test suite
        with self._db.get_session() as s:
            test_suites = s.query(db.TestSuite)

            for ts in test_suites:
                # Figure out the filename & Open it for writing
                filename = conf.path + os.path.sep + ("%s.jira.xml" % ts.name)
                create_folder(filename)
                f = open(filename, "w")

                # Create root element & Populate
                root = etree.Element("testsuite")
                root.attrib["error"] = "0"
                root.attrib["failures"] = "0"
                root.attrib["name"] = ts.name
                root.attrib["tests"] = "0"
                root.attrib["time"] = "0"

                total_execution = 0.0
                failures = 0
                errors = 0 #Fix for CAFE-1220
                tests = 0

                for tc in ts.test_cases:
                    # Create test case node & Populate it
                    project = conf.jira_project
                    tc_node = etree.SubElement(root, "testcase")
                    tc_node.attrib["assignee"] = tc.assignee
                    tc_node.attrib["bugatts"] = "jirap:%s;comment:false;lbs:manual_run,%s" % (project, ts.name)
                    tc_node.attrib["build"] = "unspecified"
                    tc_node.attrib["createbug"] = "false"
                    tc_node.attrib["name"] = "/%s." % tc.global_id
                    tc_node.attrib["release"] = "latest_release()"
                    tc_node.attrib["run_state"] = "SCORE"
                    tc_node.attrib["time"] = str(round(tc.elapsed_time, 3))

                    # Keep track of statistics
                    total_execution = total_execution + tc.elapsed_time
                    tests += 1

                    # Get failures & add them to the testcase
                    for tc_step in tc.test_steps:
                        if tc_step.status == db.FAIL:
                            step_node = etree.SubElement(tc_node, "failure")
                            step_node.attrib["message"] = tc_step.msg
                            failures += 1
                        elif tc_step.status == db.ERROR:#Fix for CAFE-1220
                            step_node = etree.SubElement(tc_node, "error")
                            step_node.attrib["message"] = tc_step.msg
                            errors += 1

                # Update suite statistics after all test cases are loaded
                root.attrib["tests"] = str(tests)
                root.attrib["failures"] = str(failures)
                root.attrib["error"] = str(errors) #Fix for CAFE-1220
                root.attrib["time"] = str(round(total_execution, 3))

                # Write the resulting XML to the file
                f.write(etree.tostring(root, pretty_print=True, xml_declaration=True, encoding="UTF-8"))
                filenames.append(filename)
                f.close()

        self.__create_tarball(conf, filenames)


    def __create_tarball(self, conf, filenames):
        """
        Method for generating a tarball file and deleting the xml file
        if the tarball has been flagged for cleanup in the configuration.ini file

        Args:
            conf: Configuration file data
            filenames: List of file names that will be created

        Returns: None

        """
        if conf.create_tarball:
            # Create the tarball
            tgzfname = conf.tarball_name
            create_folder(tgzfname)
            tgz = tarfile.open(tgzfname, "w:gz")

            # Add each created file to the tarball
            for fname in filenames:
                tgz.add(fname, os.path.basename(fname))
            tgz.close()

            if conf.tarball_cleanup:
                # Delete the created XML files
                for fname in filenames:
                    os.unlink(fname)