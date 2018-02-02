#!/opt/ActivePython-2.7/bin/python2

#This script is alias of the ~/caferobot/cafebot.py
#It serves the purpose of backward compatibility
from caferobot.cafebot import CafebotExecFactory
if __name__ == "__main__":
    CafebotExecFactory.create().run()
