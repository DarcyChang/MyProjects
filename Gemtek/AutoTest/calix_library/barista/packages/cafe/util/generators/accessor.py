#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random
from abc import ABCMeta, abstractmethod

from cafe.core.logger import CLogger

__author__ = 'David Qian'

"""
Created on 08/09/2016
@author: David Qian

"""


_module_logger = CLogger(__name__)
debug = _module_logger.debug
info = _module_logger.info
warn = _module_logger.warning
exception = _module_logger.exception
error = _module_logger.error


class AccessorBase(object):
    __metaclass__ = ABCMeta

    def __init__(self, generators):
        self._generators = generators

    @abstractmethod
    def next(self):
        pass

    def reset_generators_status(self):
        map(lambda x: x.reset(), self._generators)


class SequenceAccessor(AccessorBase):
    def __init__(self, generators):
        super(SequenceAccessor, self).__init__(generators)
        self._cur_index = 0

    def next(self):
        try:
            return self.cur_generator.next()
        except StopIteration:
            self.next_generator()
            return self.cur_generator.next()

    @property
    def cur_generator(self):
        return self._generators[self._cur_index]

    def next_generator(self):
        self._cur_index += 1
        if self._cur_index == len(self._generators):
            self._cur_index = 0
            self.reset_generators_status()


class RandomAccessor(AccessorBase):
    def __init__(self, generators):
        super(RandomAccessor, self).__init__(generators)
        self._total_len = sum(map(lambda x: x.length, self._generators))

    def next(self):
        index = random.randint(0, self._total_len - 1)
        gen, index = self._calc_index(index)
        return gen.get(index)

    def _calc_index(self, index):
        for gen in self._generators:
            if index >= gen.length:
                index -= gen.length
                continue

            return gen, index

        raise RuntimeError('Invalid index')


class RandomUniqueAccessor(RandomAccessor):
    def __init__(self, generators):
        super(RandomUniqueAccessor, self).__init__(generators)
        self._reset()

    def _reset(self):
        self._available_len = sum(map(lambda x: x.length, self._generators))
        self._range_pool = [(0, self._available_len - 1)]

    def __get_real_index(self, index):
        for idx, range_pair in enumerate(self._range_pool):
            range_len = range_pair[1] - range_pair[0] + 1
            if index >= range_len:
                index -= range_len
                continue

            return self.__update_range_pool(idx, index)

    def __update_range_pool(self, idx0, idx1):
        original_pair = self._range_pool[idx0]
        index_range = self._range_pool[idx0][1] - self._range_pool[idx0][0]
        if index_range == 0:
            self._range_pool.pop(idx0)
        else:
            if idx1 == 0:
                self._range_pool[idx0] = (original_pair[0] + 1, original_pair[1])
            elif idx1 == index_range:
                self._range_pool[idx0] = (original_pair[0], original_pair[1] - 1)
            else:
                pair_0 = (original_pair[0], original_pair[0] + idx1 - 1)
                pair_1 = (original_pair[0] + idx1 + 1, original_pair[1])
                self._range_pool[idx0] = pair_0
                self._range_pool.insert(idx0 + 1, pair_1)

        self._available_len -= 1

        return original_pair[0] + idx1

    def next(self):
        if self._available_len == 0:
            self._reset()

        rand_index = random.randint(0, self._available_len - 1)
        gen, index = self._calc_index(self.__get_real_index(rand_index))
        return gen.get(index)
