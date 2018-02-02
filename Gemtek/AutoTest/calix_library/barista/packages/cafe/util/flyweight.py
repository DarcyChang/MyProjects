#!/usr/bin/env python
# -*- coding: utf-8 -*-

import weakref
from abc import ABCMeta

from cafe.core.logger import CLogger
from caferobot.caseutil import InstanceRefSet

_module_logger = CLogger(__name__)
debug = _module_logger.debug
error = _module_logger.error
warn = _module_logger.warning
info = _module_logger.info


class FlyweightMeta(ABCMeta):
    def __new__(mcs, name, parents, dct):
        """
        :param name: class name
        :param parents: class parents
        :param dct: dict: includes class attributes, class methods,
        static methods, etc
        :return: new class
        """

        # set up instances pool
        dct['pool'] = weakref.WeakValueDictionary()

        # def get_driver(self):
        #     raise NotImplementedError()
        #
        # # Device class should implement this method
        # dct['get_driver'] = get_driver

        return super(FlyweightMeta, mcs).__new__(mcs, name, parents, dct)

    @staticmethod
    def _serialize_params(cls, *args, **kwargs):
        """Serialize input parameters to a key.
        Simple implementation is just to serialize it as a string

        """
        args_list = map(str, args)
        args_list.extend([str(kwargs), cls.__name__])
        key = ''.join(args_list)
        return key

    def __call__(cls, *args, **kwargs):
        key = FlyweightMeta._serialize_params(cls, *args, **kwargs)
        pool = getattr(cls, 'pool')

        instance = pool.get(key)
        if not instance:
            info('Create %s instance with key "%s"' % (cls.__name__, key))
            instance = super(FlyweightMeta, cls).__call__(*args, **kwargs)
            InstanceRefSet.add(instance)
            pool[key] = instance
        else:
            debug('class %s instance with key "%s" already exists' % (cls.__name__, key))
        return weakref.proxy(instance)
