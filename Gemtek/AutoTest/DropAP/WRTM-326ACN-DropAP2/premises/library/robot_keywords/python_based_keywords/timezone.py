import time
import pytz
import datetime
from datetime import timedelta
from TZDST_LIB import TZ_DST_Dict


__author__ = 'xlzhang'

class timezone(object):

    def __init__(self):
        pass

    @staticmethod
    def checkTZgood (ontTime, ontTZ):
            ontTime = datetime.datetime.strptime(ontTime, '%A, %b %d, %Y, %I:%M %p')
            #ontTime = "Thursday, Jul 14, 2016, 8:00 PM"
            #Tuesday, Jul 19, 2016, 0:10 AM
            print "ontTime:", ontTime
            #2016-07-14 20:00:00
            TimeZoneDict = {'UTC-12:00': 'Etc/GMT+12',
                            'UTC-11:00': 'Etc/GMT+11',
                            'UTC-10:00': 'Etc/GMT+10',
                            'UTC-09:00': 'Etc/GMT+9',
                            'UTC-08:00': 'Etc/GMT+8',
                            'UTC-07:00': 'Etc/GMT+7',
                            'UTC-06:00': 'Etc/GMT+6',
                            'UTC-05:00': 'Etc/GMT+5',
                            'UTC-04:30': 'America/Caracas',
                            'UTC-04:00': 'Etc/GMT+4',
                            'UTC-03:00': 'Etc/GMT+3',
                            'UTC-02:00': 'Etc/GMT+2',
                            'UTC-01:00': 'Etc/GMT+1',
                            'UTC': 'Etc/GMT',
                            'UTC\\+01:00': 'Etc/GMT-1',
                            'UTC\\+02:00': 'Etc/GMT-2',
                            'UTC\\+03:00': 'Etc/GMT-3',
                            'UTC\\+04:00': 'Etc/GMT-4',
                            'UTC\\+05:00': 'Etc/GMT-5',
                            'UTC\\+06:00': 'Etc/GMT-6',
                            'UTC\\+07:00': 'Etc/GMT-7',
                            'UTC\\+08:00': 'Etc/GMT-8',
                            'UTC\\+09:00': 'Etc/GMT-9',
                            'UTC\\+10:00': 'Etc/GMT-10',
                            'UTC\\+11:00': 'Etc/GMT-11',
                            'UTC\\+12:00': 'Etc/GMT-12',
                            'UTC\\+13:00': 'Etc/GMT-13',
                            'UTC\\+04:30': 'Asia/Kabul',
                            'UTC\\+05:30': 'Asia/Kolkata',
                            'UTC\\+05:45': 'Asia/Kathmandu',
                            'UTC\\+06:30': 'Asia/Rangoon',
                            'UTC\\+09:30': 'Australia/Darwin'}
            # print all_timezones
            tz = pytz.timezone(TimeZoneDict[ontTZ])
            currentTime = datetime.datetime.now(tz)
            print "currentTime:", currentTime

            # currentTimeStamp = time.mktime(currentTime.astimezone(pytz.utc).timetuple())
            # ontTime = tz.localize(ontTime)
            # ontTimeStamp = time.mktime(ontTime.astimezone(pytz.utc).timetuple())
            # use relative time to calculate the stamp so there is no absolute error.
            # current time and any other time parameters will be transfer to local time(local TZ and DST)
            # and then use that local time to calculate stamp.
            currentTimeStamp = time.mktime(currentTime.timetuple())
            ontTimeStamp = time.mktime(ontTime.timetuple())

            print 'ontTimeStamp', ontTimeStamp
            print 'currentTimeStamp:', currentTimeStamp
            # set absolute error to 600s
            if abs(currentTimeStamp-ontTimeStamp) > 600:
                return 0
            else:
                return 1

    @staticmethod
    def checkDSTgood (ontTime, ontTZlabel):
            ontTime = datetime.datetime.strptime(ontTime, '%A, %b %d, %Y, %I:%M %p')
            #ontTime = "Thursday, Jul 14, 2016, 8:00 PM"
            print "ontTime:", ontTime
            #2016-07-14 20:00:00
            tz = pytz.timezone( TZ_DST_Dict[ontTZlabel])
            currentTime = datetime.datetime.now(tz)
            print "currentTime:", currentTime
            currentTimeStamp = time.mktime(currentTime.astimezone(pytz.utc).timetuple())
            ontTime = tz.localize(ontTime)
            ontTimeStamp = time.mktime(ontTime.astimezone(pytz.utc).timetuple())

            print 'ontTimeStamp', ontTimeStamp
            print 'currentTimeStamp:', currentTimeStamp


            if abs(currentTimeStamp-ontTimeStamp) > 600:
                return 0
            else:
                return 1

    @staticmethod
    def checkDefaultTimegood (ontTime, ontTZ= 'UTC-08:00'):
            if timezone.checkTZgood (ontTime, ontTZ):
                return 1
            else:
                return 0

    @staticmethod
    def checkDTDSTgood (ontTime, ontTZlabel):
            ontTime = datetime.datetime.strptime(ontTime, '%A, %b %d, %Y, %I:%M %p')
            #ontTime = "Thursday, Jul 14, 2016, 8:00 PM"
            print "ontTime:", ontTime
            #2016-07-14 20:00:00
            TimeZoneDict = {'Tehran': 'Asia/Tehran',
                            'UTC-03:30': 'Canada/Newfoundland',
                            'UTC+09:30': 'Australia/Darwin'}
            # print all_timezones
            #
            tz = pytz.timezone(TimeZoneDict[ontTZlabel])
            now = pytz.utc.localize(datetime.datetime.utcnow())
            #currentTime = datetime.datetime.now(tz)
            #currentTime = now.astimezone(tz)
            #Check target zone DST info
            if now.astimezone(tz).dst() != timedelta(0) :
                currentTime = now.astimezone(tz) - timedelta(minutes=60)
                currentTime = tz.normalize(currentTime)
                print "currentTime_withDSTchanged:", currentTime, currentTime.tzinfo
            else :
                currentTime = now.astimezone(tz)
                print "currentTime_noDSTchanged:", currentTime, currentTime.tzinfo

            currentTimeStamp = time.mktime(currentTime.astimezone(pytz.utc).timetuple())
            ontTime = tz.localize(ontTime)
            ontTimeStamp = time.mktime(ontTime.astimezone(pytz.utc).timetuple())

            print 'ontTimeStamp', ontTimeStamp
            print 'currentTimeStamp:', currentTimeStamp

            if abs(currentTimeStamp-ontTimeStamp) > 600:
                return 0
            else:
                return 1
