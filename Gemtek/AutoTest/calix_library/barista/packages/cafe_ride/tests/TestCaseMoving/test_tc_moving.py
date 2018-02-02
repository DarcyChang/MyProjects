import random
import unittest

from cafe_ride.plugins.TestCaseMoving.test_case_moving import TestCaseMovingPulgin
from cafe_ride.tests import FakeApplication, MAX_TC_LEN, MAX_UK_LEN, MIN_TC_LEN, MIN_UK_LEN
from robotide import utils

class TestTCMoving(unittest.TestCase):
    def setUp(self):
        self.app = FakeApplication()
        self.test_case_moving = TestCaseMovingPulgin(self.app)
        self.test_case_moving.enable()
        self._tree = self.test_case_moving.tree
        self.moved_item_text = self._mock_select_item()
        print self.moved_item_text
        self.moved_item_pos = 0
        self.moved_item = self._find_node_info_by_label(self._tree._root, self.moved_item_text)
        print self.moved_item_pos
        if self.moved_item:
            print self.moved_item

    def _mock_select_item(self):
        suites = ['Sub Suite %d ' % i for i in range(3)] + ['Top Suite ']
        tc_or_uk = ['Fake Test %d ' % i for i in range(3)] + ['Fake UK %d ' % i for i in range(3)]
        select_suite = suites[random.randint(0, len(suites)-1)]
        if select_suite == 'Top Suite ':
            select_tc_or_uk = tc_or_uk[random.randint(3, len(tc_or_uk)-1)]
        else:
            select_tc_or_uk = tc_or_uk[random.randint(0, len(tc_or_uk)-1)]
        return select_suite + select_tc_or_uk

    def _find_node_info_by_label(self, node, label):
        predicate = lambda n: utils.eq(self._tree.GetItemText(n), label)
        child, cookie = self._tree.GetFirstChild(node)
        while child:
            if predicate(child):
                self.moved_item_pos = cookie - 1
                return child
            if self._tree.ItemHasChildren(child):
                result = self._find_node_info_by_label(child, label)
                if result:
                    return result
            child, cookie = self._tree.GetNextChild(node, cookie)
        return None

    def test_ctrl_pageup_shortcut(self):
        self._tree.SelectItem(self.moved_item)
        self.test_case_moving.testcase_move_up(None)
        move_up = self.moved_item_pos if self.moved_item_pos in (MIN_TC_LEN, MIN_UK_LEN) else self.moved_item_pos-1
        self._find_node_info_by_label(self._tree._root, self.moved_item_text)
        self.assertEqual(self.moved_item_pos, move_up)

    def test_ctrl_pagedown_shortcut(self):
        self._tree.SelectItem(self.moved_item)
        self.test_case_moving.testcase_move_down(None)
        move_down = self.moved_item_pos if self.moved_item_pos in (MAX_UK_LEN, MAX_TC_LEN) else self.moved_item_pos+1
        self._find_node_info_by_label(self._tree._root, self.moved_item_text)
        self.assertEqual(self.moved_item_pos, move_down)
