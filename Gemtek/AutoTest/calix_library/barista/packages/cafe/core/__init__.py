import os
# delete decorator.pyc due to refactor from 'core/decorator.py' to 'core/decorators.py'
try:
    os.remove(os.path.join(os.path.dirname(__file__), 'decorator.pyc'))
except:
    pass

__author__ = 'kelvin'
from cafe.core import decorators
