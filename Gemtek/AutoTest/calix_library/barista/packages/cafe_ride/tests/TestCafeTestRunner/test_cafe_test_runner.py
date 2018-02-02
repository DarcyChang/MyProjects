import random
import string
import unittest

from cafe_ride.tests import FakeApplication
from cafe_ride.plugins.CafeTestRunner.cafe_test_runner import CafeTestRunner

DEFAULT_PROFILE_NUM = 3
DEFAULT_PROFILE_CHOICE_NUM = 4
MAX_PROFILE_NAME_LEN = 50
PROFILE_LIST = []


class TestCafeTestRunner(unittest.TestCase):
    def setUp(self):
        self.cafe_test_runner = CafeTestRunner(FakeApplication())
        self.cafe_test_runner.enable()

    def _profile_name_generator(self):
        return ''.join(random.choice(string.ascii_letters+string.digits+'_'+' ') for _ in range(MAX_PROFILE_NAME_LEN))

    def _set_custom_profile(self):
        profile = self._profile_name_generator()
        self.cafe_test_runner._add_custom_profile(profile)
        self.cafe_test_runner.save_setting("profile", profile)
        self.cafe_test_runner.SetProfile(self.cafe_test_runner.profile)
        return profile

    def test_add_new_profile(self):
        for _ in range(random.randint(1, 10)):
            profile_name = self._set_custom_profile()

            # check the profile name in setting file
            self.assertEqual(getattr(self.cafe_test_runner, 'profile'), profile_name)
            self.assertIn(profile_name, getattr(self.cafe_test_runner, 'custom_profiles'))

            # check the profile name in choice panel
            self.assertEqual(self.cafe_test_runner.choice.GetStringSelection(), profile_name)

            # check the profile name in test runner instance
            self.assertIn(profile_name, self.cafe_test_runner._test_runner.get_profile_names())

            PROFILE_LIST.append(profile_name)

    def test_del_custom_profile(self):
        for profile_name in PROFILE_LIST:
            self.cafe_test_runner.save_setting("profile", profile_name)
            self.cafe_test_runner.SetProfile(self.cafe_test_runner.profile)
            self.cafe_test_runner._del_custom_profile()

            # check if the profile was removed in setting file
            self.assertNotIn(profile_name, getattr(self.cafe_test_runner, 'custom_profiles'))

            # check if the profile was removed in choice panel
            self.assertNotIn(profile_name, self.cafe_test_runner.choice.GetStrings())

            # check if the profile was removed in test runner instance
            self.assertNotIn(profile_name, self.cafe_test_runner._test_runner.get_profile_names())

        # check if the custom profiles were empty in the plugin.
        self.assertEqual(self.cafe_test_runner.choice.GetCount(), DEFAULT_PROFILE_CHOICE_NUM)
        self.assertEqual(len(self.cafe_test_runner._test_runner.get_profile_names()), DEFAULT_PROFILE_NUM)
        self.assertEqual(len(getattr(self.cafe_test_runner, 'custom_profiles')), 0)
