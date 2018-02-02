"""
Cafe intermediate database (idb) module
"""
__author__ = 'kelvin'
import inspect
import os
import re
import threading
import time
from contextlib import contextmanager
from threading import RLock

import sqlalchemy
from prettytable import PrettyTable
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy import ForeignKey
from sqlalchemy import Sequence
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm.exc import NoResultFound

from cafe.core.config import get_config
from decorators import SingletonClass
from logger import CLogger as Logger
from signals import *
from utils import Param

pattern = [r".cli(", ]

Base = declarative_base()

logger = Logger().get_child("testdb")
logger.debug("importing module %s" % __name__)

debug = logger.debug
error = logger.error
warn = logger.warn

PASS = "pass"
FAIL = "fail"
INDETERMINATE = "indeterminate"
INFO = "info"
WARN = "warn"
ERROR = "error"
UNKNOWN = "unknown"


class TestSuite(Base):
    """DB Test Suite Table/Object definition
    """
    __tablename__ = "testsuites"

    test_suite_id = Column(Integer, Sequence("ts_id_seq"), primary_key=True)
    name = Column(String, default="default testsuite", unique=True)
    status = Column(String, default="indeterminate")
    start_time = Column(Float, default=0.0)
    elapsed_time = Column(Float, default=0.0)

    test_cases = relationship("TestCase", back_populates="test_suite")


class TestCase(Base):
    """DB Test Case Table/Object Definition

    """
    __tablename__ = "testcases"

    test_case_id = Column(Integer, Sequence("tc_id_seq"), primary_key=True)
    name = Column(String, default="default testcase")
    assignee = Column(String, default="")
    group = Column(String, default="")
    test_suite_id = Column(Integer, ForeignKey('testsuites.test_suite_id'))
    global_id = Column(String, default="000001")
    start_time = Column(Float, default=0.0)
    elapsed_time = Column(Float, default=0.0)
    status = Column(String, default="indeterminate")

    test_suite = relationship("TestSuite", back_populates="test_cases")
    test_steps = relationship("TestStep", back_populates="test_case")


class TestStep(Base):
    """DB Test Step Table/Object Definition

    """
    __tablename__ = "teststeps"

    test_step_id = Column(Integer, Sequence("tc_step_id_seq"), primary_key=True)
    test_case_id = Column(Integer, ForeignKey('testcases.test_case_id'))
    index = Column(String, default="")
    sid = Column(String, default="")
    action = Column(String, default="")
    target = Column(String, default="")
    cmd = Column(String, default="")
    response = Column(String, default="")
    status = Column(String, default="indeterminate")
    title = Column(String, default="")
    test = Column(String, default="")
    msg = Column(String, default="")
    filename = Column(String, default="")
    line = Column(Integer, default="")
    start_time = Column(Float, default=0.0)
    elapsed_time = Column(Float, default=0.0)

    test_case = relationship("TestCase", back_populates="test_steps")


class _TestDB(object):
    __uid = 0
    def __init__(self, db_uri="sqlite:///my_sqlite.db", echo=False, logger=None):
        """constructor

        Args:
            db_uri (string): data url string. default ("sqlite:///my_sqlite.db")
            echo (bool): True - to turn on the sqlachemy debug log print; False otherwise
            logger (object): Cafe CLogger object

        Returns:
            None

        """
        self.state = "disconnect"
        self.db_uri = db_uri

        self.db_lock = RLock()
        self.thread_state = threading.local()
        self.thread_state.current_testsuite_id = None
        self.thread_state.current_testcase_id = None
        self.thread_state.current_teststep_id = None
        self.thread_state.previous_testcase_id = None
        self.thread_state.in_transaction = False

        self.logger = Logger(__name__) if logger is None else logger

        try:
            _TestDB.create_path_from_uri(db_uri)
            engine = self.db_engine = sqlalchemy.create_engine(db_uri, echo=echo)
            Base.metadata.create_all(engine)
            self.__session = scoped_session(sqlalchemy.orm.sessionmaker(bind=engine))
        except Exception as e:
            self.logger.error(" - db_uri=%s: %s" % (str(db_uri), e.message))
        else:
            self.state = "connected"
            self.logger.debug("db (%s) create success" % str(db_uri))

    @property
    def uid(self):
        self.__uid += 1
        return self.__uid

    @contextmanager
    def get_session(self):
        """ Context manager which gives the user a SQLAlchemy session for this database.

        If you are already inside another session, that session is returned instead.

        The session blocks the database until the context is exited, due to SQLite not supporting simultaneous writes.

        Examples:
            >>> from cafe.core.db import get_test_db, TestSuite
            >>>
            >>> with get_test_db().get_session() as s:
            >>>     test_suites = s.query(TestSuite).filter(TestSuite.name.like("test_%")).all()

        Yields:
            A SQLAlchemy session object

        """
        try:
            transaction_starter = not self.thread_state.in_transaction
        except AttributeError:
            transaction_starter = True

        if transaction_starter:
            self.thread_state.in_transaction = True

        with self.db_lock:
            yield self.__session()

        if transaction_starter:
            self.__session.remove()
            self.thread_state.in_transaction = False

    @staticmethod
    def return_db_uri(db_type, abs_db_path):
        """static method to return a sqlalchemy uri with timestamp

        Args:
            db_type: (string) - database type. eg sqlite.
            abs_db_path: absolute pathname of the database file or uri

        Returns:
            string - db uri

        """
        t = time.localtime()
        t1 = time.strftime("%Y%m%d", t)
        t2 = time.strftime("%Y%m%d%H%M%S", t)
        s = "sqlite:///%s/%s/%s.idb" % (abs_db_path, t1, t2)
        # note:
        # problem to run in memory database with multithread
        # should consider linux RAM disk solution
        # s = "sqlite:///:memory:"
        return s

    @staticmethod
    def get_db_uri_from_file(db_type, db_file):
        """static method to return a sqlalchemy uri form a file

        Args:
            db_type (string): database type. eg sqlite.
            abs_db_path: absolute pathname of the database file or uri

        Returns:
            string: db uri

        """
        s = "sqlite:///%s" % (db_file)
        return s

    @staticmethod
    def get_path_from_uri(uri):
        """static method to return db file pathname from uri

        Args:
            uri (string): string of sqlachemy db uri

        Returns:
            string: db file pathname

        """
        return uri.split("///")[1]

    @staticmethod
    def create_path_from_uri(uri):
        """static method to to create file folder path uri

        Args:
            uri (string): string of sqlachemy db uri

        Returns:
            None

        """
        p = TestDB.get_path_from_uri(uri)
        try:
            os.makedirs(os.path.dirname(p))
        except (OSError, BaseException):
            pass
        return os.path.isdir(os.path.dirname(p))

    def get_db_uri(self):
        """static method to return db uri

        Returns:
            string: db uri

        """
        return self.db_uri

    # TODO: Need a message for these exceptions
    class CafeDBException(Exception):
        pass

    class CafeNoCurrentTestCase(Exception):
        pass

    class CafeNoPreviousTestCase(Exception):
        pass

    class CafeNoCurrentTestSuite(Exception):
        pass

    class CafeNoCurrentTestStep(Exception):
        pass

    def unset_current_testcase_id(self):
        """ Unsets the current testcase id. The current teststep id is thread-local.
        """
        self.thread_state.current_testcase_id = None

    def unset_current_testsuite_id(self):
        """ Unsets the current testsuite id. The current teststep id is thread-local.
        """
        self.thread_state.current_testsuite_id = None

    def unset_current_teststep_id(self):
        """ Unsets the current teststep id. The current teststep id is thread-local.
        """
        self.thread_state.current_teststep_id = None

    def set_current_testcase_id(self, test_case_id):
        """ Sets the current testcase id. The current testcase id is thread-local.
        """
        self.thread_state.current_testcase_id = test_case_id

    def set_current_testsuite_id(self, test_suite_id):
        """ Sets the current testsuite id. The current testcase id is thread-local.
        """
        self.thread_state.current_testsuite_id = test_suite_id

    def set_current_teststep_id(self, test_step_id):
        """ Sets the current teststep id. The current testcase id is thread-local.
        """
        self.thread_state.current_teststep_id = test_step_id

    def get_previous_testcase_id(self):
        """ Returns the current testcase id. The current testcase id is thread-local.

        Raises:
            TestDB.CafeNoCurrentTestCase if there is no current testcase
        """
        try:
            ret = self.thread_state.previous_testcase_id
        except AttributeError:
            ret = self.thread_state.previous_testcase_id = None

        if ret is None:
            raise self.CafeNoPreviousTestCase()
        else:
            return ret

    def get_current_testcase_id(self):
        """ Returns the current testcase id. The current testcase id is thread-local.

        Raises:
            TestDB.CafeNoCurrentTestCase if there is no current testcase
        """
        try:
            ret = self.thread_state.current_testcase_id
        except AttributeError:
            ret = self.thread_state.current_testcase_id = None

        if ret is None:
            raise self.CafeNoCurrentTestCase()
        else:
            return ret

    def get_current_testsuite_id(self):
        """ Returns the current testsuite id. The current testsuite id is thread-local.

        Raises:
            TestDB.CafeNoCurrentTestCase if there is no current testsuite
        """
        try:
            ret = self.thread_state.current_testsuite_id
        except AttributeError:
            ret = self.thread_state.current_testsuite_id = None

        if ret is None:
            raise self.CafeNoCurrentTestSuite()
        else:
            return ret

    def get_current_teststep_id(self):
        try:
            ret = self.thread_state.current_teststep_id
        except AttributeError:
            ret = self.thread_state.current_teststep_id = None

        if ret is None:
            raise self.CafeNoCurrentTestStep()
        else:
            return ret

    def create_teststep(self, title="", index="", sid="", action="", target="",
                        cmd="", response="", status="indeterminate", test="unknown",
                        msg="", filename="", line=-1, start_time=time.time(), elapsed_time=0.0):
        if self.state is "disconnect":
            raise self.CafeDBException("Lost connection to DB!")

        # If there is no current test case (Keyword is used as an API call, for example), allow a pass
        ret = None

        try:
            test_case_id = self.get_current_testcase_id()
            step = self._create_teststep(test_case_id, title, index, sid, action, target, cmd,
                                         response, status, test, msg, filename, line,
                                         start_time, elapsed_time)

            self.set_current_teststep_id(step.test_step_id)

            ret = step
        except self.CafeNoCurrentTestCase:
            ret = None

        return ret

    def _create_teststep(self, test_case_id, title="", index="", sid="", action="", target="",
                         cmd="", response="", status="indeterminate", test="unknown", msg="", filename="",
                         line=-1, start_time=time.time(), elapsed_time=0.0):

        with self.get_session() as session:
            session.expire_on_commit = False

            step = TestStep(test_case_id=test_case_id, title=title, index=index, sid=sid,
                            action=action, target=target, cmd=cmd,
                            response=response, status=status,
                            test=test, msg=msg, filename=filename,
                            line=line, start_time=start_time,
                            elapsed_time=elapsed_time)

            session.add(step)
            session.commit()

            if status == "pass" and step.test_case.status == "indeterminate":
                step.test_case.status = "pass"
            elif status == "fail" or status == "error":
                step.test_case.status = "fail"

            session.commit()
            # step_id = step.test_step_id

        return step

    def create_testcase(self, group="", name="default", global_id="000001", assignee="default", start_time=None):
        if self.state is "disconnect":
            raise self.CafeDBException("Lost connection to DB!")

        if start_time is None:
            start_time = time.time()

        test_suite_id = None

        # If there is no current test suite, create a default test suite
        try:
            test_suite_id = self.get_current_testsuite_id()
        except self.CafeNoCurrentTestSuite:
            test_suite_id = self.create_testsuite()
        finally:
            tc_id = self._create_testcase(group, name, global_id, assignee, test_suite_id, start_time)
            self.set_current_testcase_id(tc_id)

        return tc_id

    def _create_testcase(self, group="", name="default_testcase", global_id="000001", assignee="default",
                         test_suite_id=-1,
                         start_time=time.time()):

        tc = TestCase(group=group, name=name, global_id=global_id, assignee=assignee, test_suite_id=test_suite_id,
                      start_time=start_time)
        tc_id = None

        with self.get_session() as session:
            session.add(tc)
            session.commit()
            tc_id = tc.test_case_id

        return tc_id

    def create_testsuite(self, name=None, start_time=None, elapsed_time=0.0):
        if self.state == "disconnect":
            raise self.CafeDBException("Lost connection to DB!")

        if start_time is None:
            start_time = time.time()

        ts = TestSuite(name=name, start_time=start_time, elapsed_time=elapsed_time)
        ts_id = None

        with self.get_session() as session:
            session.add(ts)
            session.commit()
            ts_id = ts.test_suite_id

        self.set_current_testsuite_id(ts_id)

        return ts_id

    def close_current_testcase(self):
        with self.get_session() as session:
            tc = session.query(TestCase).filter(TestCase.test_case_id == self.get_current_testcase_id()).one()
            tc.elapsed_time = time.time() - tc.start_time

            ts_status = tc.test_suite.status

            if tc.status == "pass" and ts_status == "indeterminate":
                tc.test_suite.status = "pass"
            elif tc.status == "fail":
                tc.test_suite.status = "fail"

            session.commit()

        self.thread_state.previous_testcase_id = self.get_current_testcase_id()
        self.unset_current_testcase_id()

    def close_current_testsuite(self):
        with self.get_session() as session:
            ts = session.query(TestSuite).filter(TestSuite.test_suite_id == self.get_current_testsuite_id()).one()
            ts.elapsed_time = time.time() - ts.start_time
            session.commit()

        self.unset_current_testsuite_id()

    def get_current_testcase(self):
        with self.get_session() as session:
            tc = session.query(TestCase).filter(TestCase.test_case_id == self.get_current_testcase_id()).one()
            session.expunge(tc)

        return tc

    def get_summary_report_text(self):
        # TODO: Should these be moved to their own module and class
        """
        get summary report of test execution
        :return: string of summary report
        """
        self.logger.debug("get summary report text")

        with self.get_session() as db_session:
            testsuites = db_session.query(TestSuite).all()

            x = PrettyTable(["name", "status", "tc_num", "pass", "fail", "indeterminate", "start_time", "elapsed_time"])

            x.align["name"] = "l"
            x.padding_width = 1  # One space between column edges and contents (default)
            for ts in testsuites:
                vals = [ts.name, ts.status]

                vals.append(len(ts.test_cases))
                vals.append(len([i for i in ts.test_cases if i.status == "pass"]))
                vals.append(len([i for i in ts.test_cases if i.status == "fail"]))
                vals.append(len([i for i in ts.test_cases if i.status == "indeterminate"]))

                vals.extend([ts.start_time, ts.elapsed_time])

                x.add_row(vals)

            ret = "*** summary report ***\n" + str(x)
        return ret

    def get_testsuite_report_text(self, ts):
        # TODO: Should these be moved to their own module and class
        """
        get test suite report
        :param ts: name or id of test suite
        :return: string of test suite report
        """
        if isinstance(ts, str):
            ts_id = self.get_testsuite(ts).test_suite_id
        elif isinstance(ts, int):
            ts_id = int(ts)
        else:
            ts_id = -1

        if ts_id == -1:
            self.logger.error(msg=" - ts (%s)" % str(ts),
                              signal=DB_TESTSUITE_GET_ID_FAILED)
            return

        self.logger.debug("get testsuite report text (%s)" % str(ts))

        with self.get_session() as session:
            testcases = session.query(TestCase).filter(TestCase.test_suite_id == ts_id)

            x = PrettyTable(["name", "global_id", "status", "assignee", "teststep_cnt", "pass",
                             "fail", "info", "warn", "error", "start_time", "elapsed_time"])
            x.align["name"] = "l"
            x.align["start_time"] = "l"
            x.align["elapsed_time"] = "l"
            x.padding_width = 1  # One space between column edges and contents (default)

            for tc in testcases:
                # print (tc)
                vals = [tc.name, tc.global_id, tc.status, tc.assignee, len(tc.test_steps)]
                vals.append(len([i for i in tc.test_steps if i.status == "pass"]))
                vals.append(len([i for i in tc.test_steps if i.status == "fail"]))
                vals.append(len([i for i in tc.test_steps if i.status == "info"]))
                vals.append(len([i for i in tc.test_steps if i.status == "warn"]))
                vals.append(len([i for i in tc.test_steps if i.status == "error"]))
                vals.extend([tc.start_time, tc.elapsed_time])

                x.add_row(vals)

        # self.Session.remove()
        ret = "*** test suite report (%s) ***\n" % str(ts) + str(x)
        return ret

    def get_testcase_report_text(self, ts, tc_name, global_id):
        """
        get test case report
        :param global_id:
        :param ts: test suite name or id
        :param tc_name: test case name
        :return: string of test case report
        """
        if isinstance(ts, str):
            ts_id = self.get_testsuite(ts).test_suite_id

        elif isinstance(ts, int):
            ts_id = int(ts)
        else:
            ts_id = -1

        if ts_id == -1:
            logger.error(msg=" - ts (%s)" % str(ts),
                         signal=DB_TESTSUITE_GET_ID_FAILED) #FIXED CAFE-1598
            return

        tc_id = self.get_testcase(tc_name, global_id, ts_id).test_case_id

        if tc_id == -1:
            logger.error(msg=" - tc (%s)" % tc_name,
                         signal=DB_TESTCASE_GET_ID_FAILED)
            return

        self.logger.debug("get testcase report text (%s %s)" % (ts, tc_name))
        with self.get_session() as db_session:
            teststeps = db_session.query(TestStep).filter(TestStep.test_case_id == tc_id)

            x = PrettyTable(["status", "index", "sid", "title", "test", "msg", "action", "target",
                             "cmd", "response", "filename", "line", "start_time", "elapsed_time"])
            x.align["id"] = "l"
            x.padding_width = 1  # One space between column edges and contents (default)
            for s in teststeps:
                val = [s.status, s.index, s.sid, s.title, s.test, s.msg, s.action, s.target, s.cmd]
                val.extend([s.response, s.filename, s.line, s.start_time, s.elapsed_time])
                x.add_row(val)
            ret = "*** test case report (%s - %s) ***\n" % (ts, tc_name) + str(x)
        return ret

    def get_testsuite(self, name):
        with self.get_session() as session:
            try:
                q = session.query(TestSuite).filter(TestSuite.name == name).one()
            except NoResultFound:
                # TODO: should a exception be raises or some value other than none be returned?
                q = None

        return q

    def get_testcase(self, name, global_id, test_suite_id):
        with self.get_session() as session:
            try:
                q = session.query(TestCase).filter(
                    TestCase.name == name,
                    TestCase.global_id == global_id,
                    TestCase.test_suite_id == test_suite_id).one()
            except NoResultFound:
                # TODO: should a exception be raises or some value other than none be returned?
                q = None

        return q


TestDB = _TestDB


@SingletonClass
class CTestDB(TestDB): pass


def get_test_db():
    if CTestDB.instance:
        ret = CTestDB()
    else:
        config = get_config()
        path = TestDB.return_db_uri(config.cafe_runner.db_type, config.cafe_runner.db_path)
        TestDB.create_path_from_uri(path)
        ret = CTestDB(db_uri=path, echo=config.cafe_runner.db_echo, logger=None)

    return ret


from functools import wraps


def teststep(title=""):
    def wrapper(func):
        @wraps(func)
        def inner(*args, **kwargs):
            start_time = time.time()
            db = get_test_db()

            try:
                _is_match = False
                for f in inspect.stack():
                    filename = f[1]
                    line = int(f[2])
                    caller = f[3]
                    test = str(f[4][0]).strip()
                    if any(x in test for x in pattern):
                        _is_match = True
                        break
                if _is_match is False:
                    f = inspect.stack()[1]
                    filename = f[1]
                    line = int(f[2])
                    caller = f[3]
                    test = str(f[4][0]).strip()

            except (IOError, OSError, BaseException):
                filename = "-"
                line = -1
                test = func.__name__ + "%s, %s" % (str(args), str(kwargs))

            t = "test step: " + title + ": " + test
            test = ""
            msg = "%s, %s" % (str(args), str(kwargs))

            rs = get_config().runner_state
            rs.callbacks.start_test_step(title)
            r = func(*args, **kwargs)

            step = db.create_teststep(status=INFO, title=t, test=test, msg=msg, filename=filename,
                                      response=str(r), line=line, start_time=start_time)

            rs.callbacks.end_test_step(title, step)

            if func.__name__ == "__init__":
                return
            x = Param()
            if isinstance(r, (dict, Param)):
                for i, j in r.items():
                    x.set(i, j)
            else:
                x.set("value", r)
            return x

        return inner

    return wrapper


class Testable(object):
    """Class to provide APIs to test step verification

    """
    EQUAL = "eq"
    NOTEQUAL = "ne"
    REGEX = "re"
    CONTAIN = "contain"
    NOTCONTAIN = "notcontain"

    msg_status = [PASS, FAIL, INFO, WARN, ERROR, UNKNOWN]

    def __init__(self, value="", encoding="ascii"):
        """Constructor

        Args:
            value: a object. if value is unicode. value will be converted to ascii

        """
        self.encoding = encoding
        if isinstance(value, unicode):
            value = value.encode(self.encoding, 'ignore')
        self.value = value

    def __iter__(self):
        return iter(self.value)

    def __repr__(self):
        return str(self.value)

    def _validate_msg_status(self, status):
        if not status.lower() in self.msg_status:
            warn("invald msg status (%s). return unknown" % status)
            return UNKNOWN
        else:
            return status.lower()

    def _pass(self, exp, title="", msg=""):
        self._msg(exp=exp, title=title, msg=msg, status=PASS)  # CAFE-1202

    def _fail(self, exp, title="", msg=""):
        self._msg(exp=exp, title=title, msg=msg, status=FAIL)  # CAFE-1202

    def _msg(self, exp, title="", msg="", status=UNKNOWN):
        f = inspect.stack()[1][3]
        filename = inspect.stack()[2][1]
        line = inspect.stack()[2][2]

        db = get_test_db()
        l = len(str(self.value))
        if l < 10:
            v = str(self.value)
        else:
            v = str(self.value)[0:9] + " ..."

        _status = self._validate_msg_status(status)

        title = title + ": " + f + " - exp:%s,value:%s" % (exp, v)

        test = ""

        get_config().runner_state.callbacks.start_test_step(title)
        step = None

        if db is not None:
            step = db.create_teststep(
                status=_status,
                title=title,
                test=test,
                msg=msg,
                filename=filename,
                line=line)

        get_config().runner_state.callbacks.end_test_step(title, step)

    def fail(self, title=""):
        # TODO: should this not match _fail(), maybe remove _fail()
        """
        create a "fail" teststep record.
        or use it to focus a Cafe Test case to fail.

        Args:
            title: fail message

        """
        self._msg("", title=title, status=FAIL)

    fail_test = fail_step = fail

    def pass_step(self, title=""):
        # TODO: should this not match _pass(), maybe remove _pass()
        """
        create a "PASS" teststep record.
        or use it to focus a Cafe Test case to fail.

        Args:
            title: fail message

        """
        self._msg("", title=title, status=PASS)

    pass_test = pass_step

    def info(self, title=""):
        """
        create a "info" teststep record.

        Args:
            title: info message

        """
        self._msg("", title=title, status=INFO)

    def verify_not_equal(self, exp="", title="", pos_msg="", neg_msg="", pos_status=PASS, neg_status=FAIL):
        """
        Verify Checkpoint "value"
        If the exp != value, pass; otherwise: fail.

        Args:
            exp: value to compare
            title: test title. default is ""
            pos_msg: if test pass, this message would be printed. default is ""
            neg_msg: if test fail, this message would be printed. default is ""
            pos_status: if test pass: the result would be log into db as status of "pos_status". default is "pass"
            neg_status: if test fail: the result would be log into db as status of "neg_status". default is "fail"

        Returns:
            bool: True for test pass; False otherwise.
        """
        exp = str(exp).encode(encoding=self.encoding, errors="ignore")
        if str(exp) != str(self.value):
            self._msg(exp, title, pos_msg, pos_status)
            return True
        else:
            self._msg(exp, title, neg_msg, neg_status)
            return False

    def verify_exact(self, exp="", title="", pos_msg="", neg_msg="", pos_status=PASS, neg_status=FAIL):
        """
        Verify Checkpoint "value"
        If the exp == value, pass; otherwise: fail.

        Args:
            exp: value to compare
            title: test title. default is ""
            pos_msg: if test pass, this message would be printed. default is ""
            neg_msg: if test fail, this message would be printed. default is ""
            pos_status: if test pass: the result would be log into db as status of "pos_status". default is "pass"
            neg_status: if test fail: the result would be log into db as status of "neg_status". default is "fail"

        Returns:
            bool: True for test pass; False otherwise.
        """
        exp = str(exp).encode(encoding=self.encoding, errors="ignore")
        if str(exp) == str(self.value):
            self._msg(exp, title, pos_msg, pos_status)
            return True
        else:
            self._msg(exp, title, neg_msg, neg_status)
            return False

    def verify_contains(self, exp="", title="", pos_msg="", neg_msg="", pos_status=PASS, neg_status=FAIL):
        """
        Verify Checkpoint "value"
        If the exp is contained in value, pass; otherwise: fail.

        Args:
            exp: value to compare
            title: test title. default is ""
            pos_msg: if test pass, this message would be printed. default is ""
            neg_msg: if test fail, this message would be printed. default is ""
            pos_status: if test pass: the result would be log into db as status of "pos_status". default is "pass"
            neg_status: if test fail: the result would be log into db as status of "neg_status". default is "fail"

        Returns:
            bool: True for test pass; False otherwise.
        """
        exp = str(exp).encode(encoding=self.encoding, errors="ignore")
        if str(exp) in str(self.value):
            self._msg(exp, title, pos_msg, pos_status)
            return True
        else:
            self._msg(exp, title, neg_msg, neg_status)
            return False

    def verify_not_contains(self, exp="", title="", pos_msg="", neg_msg="", pos_status=PASS, neg_status=FAIL):
        """
        Verify Checkpoint "value"
        If the exp is not contained in value, pass; otherwise: fail.

        Args:
            exp: value to compare
            title: test title. default is ""
            pos_msg: if test pass, this message would be printed. default is ""
            neg_msg: if test fail, this message would be printed. default is ""
            pos_status: if test pass: the result would be log into db as status of "pos_status". default is "pass"
            neg_status: if test fail: the result would be log into db as status of "neg_status". default is "fail"

        Returns:
            bool: True for test pass; False otherwise.
        """
        exp = str(exp).encode(encoding=self.encoding, errors="ignore")
        if not str(exp) in str(self.value):
            self._msg(exp, title, pos_msg, pos_status)
            return True
        else:
            self._msg(exp, title, neg_msg, neg_status)
            return False

    def verify_regex(self, exp="", title="", pos_msg="", neg_msg="", pos_status=PASS, neg_status=FAIL,
                     flags=re.MULTILINE):

        """
        Verify Checkpoint "value"
        If the regexp string "exp" is matched with value, pass; otherwise: fail.

        Args:
            exp: value to compare
            title: test title. default is ""
            pos_msg: if test pass, this message would be printed. default is ""
            neg_msg: if test fail, this message would be printed. default is ""
            pos_status: if test pass: the result would be log into db as status of "pos_status". default is "pass"
            neg_status: if test fail: the result would be log into db as status of "neg_status". default is "fail"

        Returns:
            bool: True for test pass; False otherwise.
        """
        exp = str(exp).encode(encoding=self.encoding, errors="ignore")
        m = re.search(exp, str(self.value), flags)
        if m:
            self._msg(exp, title, pos_msg, pos_status)
            return True
        else:
            self._msg(exp, title, neg_msg, neg_status)
            return False

    def verify(self, verify_type=None, exp="", title="", pos_msg="", neg_msg="",
               pos_status=PASS, neg_status=FAIL, flags=re.MULTILINE):
        if str(verify_type).lower() == self.EQUAL:
            return self.verify_exact(exp, title, pos_msg, neg_msg, pos_status, neg_status)
        elif str(verify_type).lower() == self.NOTEQUAL:
            return self.verify_not_equal(exp, title, pos_msg, neg_msg, pos_status, neg_status)
        elif str(verify_type).lower() == self.CONTAIN:
            return self.verify_contains(exp, title, pos_msg, neg_msg, pos_status, neg_status)
        elif str(verify_type).lower() == self.NOTCONTAIN:
            return self.verify_not_contains(exp, title, pos_msg, neg_msg, pos_status, neg_status)
        elif str(verify_type).lower() == self.REGEX:
            return self.verify_regex(exp, title, pos_msg, neg_msg, pos_status, neg_status, flags)
        else:
            return self.verify_exact(exp, title, pos_msg, neg_msg, pos_status, neg_status)

    # alias
    # TODO: Are these really needed?
    regex = verify_regex
    contains = verify_contains
    not_contains = verify_not_contains
    exact = verify_exact
    equal = verify_exact
