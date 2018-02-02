__author__ = 'akhanov'

from abc import ABCMeta
from abc import abstractmethod
from cafe.core.db import TestSuite
from cafe.core.db import TestCase
from cafe.core.db import TestStep


class Report(object):
    __metaclass__ = ABCMeta

    def __init__(self, db, config):
        self._db = db
        self._config = config

    @abstractmethod
    def generate(self):
        pass

    # def get_test_suites(self):
    #     # s = self._db.Session()
    #     with self._db.get_session() as s:
    #         tss = s.query(TestSuite).all()

    #     return tss

    # def get_test_cases(self, ts_id):
    #     # s = self._db.Session()
    #     with self._db.get_session() as s:
    #         tcs = s.query(TestCase).filter(TestCase.ts_id == ts_id)

    #     return tcs

    # def get_test_steps(self, tc_id):
    #     # s = self._db.Session()
    #     with self._db.get_session() as s:
    #         tcss = s.query(TestStep).filter(TestStep.tc_id == tc_id)

    #     return tcss
