__author__ = 'Shawn Wang'


class CafeExceptionMetaClass(type):

    _cafe_exceptions = {}

    def __new__(cls, name, base, attr):

        if 'code' not in attr or attr['code'] is None:
            raise TypeError('Cafe Exception must contain an error code')

        if 'description' not in attr:
            raise TypeError('Cafe Exception must contain a description')

        if attr['code'] in CafeExceptionMetaClass._cafe_exceptions:
            print CafeExceptionMetaClass._cafe_exceptions
            raise NameError('Code %s is already registered to %s' %
                            (attr['code'],
                             CafeExceptionMetaClass._cafe_exceptions[attr['code']]))

        CafeExceptionMetaClass._cafe_exceptions[attr['code']] = attr['description']

        return super(CafeExceptionMetaClass,
                     cls).__new__(cls, name, base, attr)


class CafeException(Exception):

    __metaclass__ = CafeExceptionMetaClass

    def __init__(self):
        self._code = None
        self._description = None

    @property
    def code(self):
        return self._code

    @code.setter
    def code(self, error_code):
        self._code = error_code

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, error_description):
        self._description = error_description

    def __str__(self):
        return "Cafe Error Code:  %s\tError:  %s" % (self.code, self.description)
