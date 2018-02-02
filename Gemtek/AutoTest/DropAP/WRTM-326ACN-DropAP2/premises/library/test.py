__author__ = 'alu'

import re
import time
import cafe
from cafe.resp.response_map import ResponseMap
from collections import OrderedDict
from demo.alu_demo.User_Cases.test_lib import Teststeplib_e7 as e7_lib



res = "ONT        Subscriber Info                                  Status" \
      "---------- ------------------------------------------------ ---------------" \
      "205        <no subscriber ID>                               enabled" \
      "           Last Location: 2/1"
r = ResponseMap(res)
table1 = r.table_match_by_delimiter()

print"table1:",table1[-1]
print type(table1[-1])










