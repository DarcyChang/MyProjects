import re
import string

class StringIO(object):
    #
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'

    #
    #extend keyword/methods
    #
    _string = 'wywang'

    def __init__(self, content = ''):
        #self._string = content
        pass

    def get_string(self):
        print(self._string)
        return self._string