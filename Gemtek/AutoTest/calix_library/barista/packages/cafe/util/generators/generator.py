#!/usr/bin/env python
# -*- coding: utf-8 -*-
from abc import ABCMeta, abstractproperty, abstractmethod

from cafe.util.generators.exceptions import InvalidGeneratorExpression, InvalidGeneratorParameter, \
    InvalidGeneratorPoolExpression

__author__ = 'David Qian'

"""
Created on 08/09/2016
@author: David Qian

"""


ELLIPSIS_FLAG = '...'


class GeneratorBuilder(object):
    def __init__(self, item_list):
        self._item_list = item_list
        self._generator = self.__build()

    def __build(self):
        generators = (EnumerationGenerator, LimitedGenerator, InfiniteGenerator)
        for gen in generators:
            try:
                return gen(self._item_list)
            except InvalidGeneratorExpression:
                pass

        raise InvalidGeneratorExpression("cannot build generator by expression '%s'" % (self._item_list,), True)

    def get_generator(self):
        return self._generator


class CafeGeneratorAccessor(object):
    def __init__(self, pool, mode):
        generators = self.__get_generators(pool)
        from cafe.util.generators.accessor import SequenceAccessor
        from cafe.util.generators.accessor import RandomAccessor
        from cafe.util.generators.accessor import RandomUniqueAccessor
        _accessor_selector = {
            'sequence': SequenceAccessor,
            'random': RandomAccessor,
            'random_unique': RandomUniqueAccessor,
        }

        self._accessor = _accessor_selector[mode.lower()](generators)

    @property
    def next(self):
        return self._accessor.next()

    def __setstate__(self, state):
        self.__init__(state['pool'], state['mode'])

    def __get_generators(self, pool):
        if all(map(lambda x: isinstance(x, list), pool)):
            # nested list, contain one or more than one generator
            return map(lambda x: self.__build_generator(x), pool)
        elif all(map(lambda x: not isinstance(x, list), pool)):
            # not nested list, contain just one generator
            return [self.__build_generator(pool)]
        else:
            raise InvalidGeneratorPoolExpression()

    def __build_generator(self, item_list):
        return GeneratorBuilder(item_list).get_generator()


class GeneratorBase(object):
    __metaclass__ = ABCMeta

    def __init__(self, expression):
        self._expression = expression
        self._cur_index = -1

    def has_next(self):
        return self._cur_index < self.length - 1

    def reset(self):
        self._cur_index = -1

    @abstractproperty
    def length(self):
        pass

    @abstractmethod
    def get(self, index):
        pass

    def __iter__(self):
        return self

    def next(self):
        if self.has_next():
            self._cur_index += 1
            return self.get(self._cur_index)

        raise StopIteration()

    @abstractmethod
    def build(self, input):
        pass


class EnumerationGenerator(GeneratorBase):
    def __init__(self, item_list):
        super(EnumerationGenerator, self).__init__(item_list)
        self._item_list = self.build(item_list)

    @property
    def length(self):
        return len(self._item_list)

    def get(self, index):
        return self._item_list[index]

    def build(self, input_list):
        if ELLIPSIS_FLAG in input_list:
            raise InvalidGeneratorExpression("Enumeration generator expression '%s' cannot contains '%s'" %
                                             (input_list, ELLIPSIS_FLAG))

        return input_list


class SequenceGenerator(GeneratorBase):
    def __init__(self, input_list):
        super(SequenceGenerator, self).__init__(input_list)
        self._start, self._step, self._end = self.build(input_list)
        self._verify()

    @property
    def length(self):
        return int((self._end - self._start) / self._step) + 1

    def get(self, index):
        return self._start + index * self._step

    def _verify(self):
        if self._step == 0:
            raise InvalidGeneratorParameter("Generator step cannot be 0, expression is '%s'" % (self._expression,))

        if self._end is not None and (self._end - self._start) / self._step <= 0:
            raise InvalidGeneratorParameter("Generator should be linear increase/decrease, expression is '%s'" %
                                            (self._expression,))


class LimitedGenerator(SequenceGenerator):
    """Limited generator.
    Format:
    [<first_elem>, <second_elem>, ..., <last_elem>]
    e.g.:
    [1, 3, ..., 10]
    """
    def build(self, input_list):
        if len(input_list) != 4:
            raise InvalidGeneratorExpression('Limited generator expression length should be 4')

        x = input_list
        if x[2] != ELLIPSIS_FLAG:
            raise InvalidGeneratorExpression("Limited generator expression 3rd elem should be '%s'" % ELLIPSIS_FLAG)

        if any(map(lambda item: not isinstance(item, (int, float)), [x[i] for i in (0, 1, 3)])):
            raise InvalidGeneratorExpression('Limited generator expression error')

        return x[0], x[1] - x[0], x[3]


class InfiniteGenerator(SequenceGenerator):
    """Infinite generator.
    Format:
    [<first_elem>, <second_elem>, ...]
    e.g.:
    [1, 3, ...]
    """
    MAX_LENGTH = 65535

    @property
    def length(self):
        return self.MAX_LENGTH

    def build(self, input_list):
        if len(input_list) != 3:
            raise InvalidGeneratorExpression('Infinite generator expression length should be 3')

        x = input_list
        if x[2] != ELLIPSIS_FLAG:
            raise InvalidGeneratorExpression("Limited generator expression 3rd elem should be '%s'" % ELLIPSIS_FLAG)

        if any(map(lambda item: not isinstance(item, (int, float)), [x[i] for i in (0, 1)])):
            raise InvalidGeneratorExpression('Limited generator expression error')

        return x[0], x[1] - x[0], None

