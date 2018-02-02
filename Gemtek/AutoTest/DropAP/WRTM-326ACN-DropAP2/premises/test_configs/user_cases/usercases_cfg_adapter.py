__author__ = 'alu'
import os

class uc_cfg_adapter(object):
    def __init__(self):
        pass

    @staticmethod
    def build_gc_l2_ins1():
        from stp.premises.test_configs.user_cases.GC import GCL2UserCase1_Conf
        return GCL2UserCase1_Conf

    @staticmethod
    def build_gc_l2_ins2():
        from stp.premises.test_configs.user_cases.GC import GCL2UserCase2_Conf
        return GCL2UserCase2_Conf

    @staticmethod
    def build_gc_l2_ins4():
        from stp.premises.test_configs.user_cases.GC import GCL2UserCase4_Conf
        return GCL2UserCase4_Conf

    @staticmethod
    def build_gc_l2_ins5():
        from stp.premises.test_configs.user_cases.GC import GCL2UserCase5_Conf
        return GCL2UserCase5_Conf

    @staticmethod
    def build_gc_l3_ins1():
        from stp.premises.test_configs.user_cases.GC import GCL3UserCase1_Conf
        return GCL3UserCase1_Conf


    @staticmethod
    def build_gh_l2_ins1():
        from stp.premises.test_configs.user_cases.GH import GHL2UserCase1_Conf
        return GHL2UserCase1_Conf

    @staticmethod
    def build_gh_l2_ins2():
        from stp.premises.test_configs.user_cases.GH import GHL2UserCase2_Conf
        return GHL2UserCase2_Conf

    @staticmethod
    def build_gh_l2_ins4():
        from stp.premises.test_configs.user_cases.GH import GHL2UserCase4_Conf
        return GHL2UserCase4_Conf

    @staticmethod
    def build_gh_l2_ins5():
        from stp.premises.test_configs.user_cases.GH import GHL2UserCase5_Conf
        return GHL2UserCase5_Conf

    @staticmethod
    def build_gh_l3_ins1():
        from stp.premises.test_configs.user_cases.GH import GHL3UserCase1_Conf
        return GHL3UserCase1_Conf