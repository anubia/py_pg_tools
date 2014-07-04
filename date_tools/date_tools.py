#!/usr/bin/env python3
# -*- encoding: utf-8 -*-


import datetime  # to manipulate dates
import time  # to manipulate dates

from dateutil.tz import tzlocal  # to manipulate dates


class DateTools:

    def __init__(self):
        pass

    @staticmethod
    def get_date(fmt='%Y%m%d_%H%M%S_%Z'):
        '''
        Target:
            - get the current date of the zone in the specified format.
        Parameters:
            - fmt: the date format used.
        Return:
            - the current date of the zone in the specified format.
        '''
        # Get date and time of the zone
        init_time = datetime.datetime.now(tzlocal())
        init_ts = init_time.strftime(fmt)  # Change date's format

        return init_ts

    @staticmethod
    def get_year(date_str, fmt='%Y%m%d_%H%M%S_%Z'):
        '''
        Target:
            - extract the year of a date stored in a string.
        Parameters:
            - date_str: the string with the date.
            - fmt: the date format used.
        Return:
            - the year of the received date.
        '''
        # Turn string into a date object
        init_ts = time.strptime(date_str, fmt)
        yy = init_ts.tm_year  # Get the year
        # Add some zeros on the left in case of years having less than 4 digits
        year = str(yy).rjust(4, '0')

        return year

    @staticmethod
    def get_month(date_str, fmt='%Y%m%d_%H%M%S_%Z'):
        '''
        Target:
            - extract the month of a date stored in a string.
        Parameters:
            - date_str: the string with the date.
            - fmt: the date format used.
        Return:
            - the month of the received date.
        '''
        # Turn string into a date object
        init_ts = time.strptime(date_str, fmt)
        mm = init_ts.tm_mon  # Get the month
        # Add a zero on the left in case of months having less than 2 digits
        month = str(mm).rjust(2, '0')

        return month

    @staticmethod
    def get_current_datetime():
        '''
        Target:
            - get the current date and time in timestamp format.
        Return:
            - a timestamp with the current moment.
        '''
        now = datetime.datetime.now()

        return now

    @staticmethod
    def get_diff_datetimes(start_time, end_time):
        '''
        Target:
            - extract the month of a date stored in a string.
        Parameters:
            - date_str: the string with the date.
            - fmt: the date format used.
        Return:
            - the month of the received date.
        '''
        diff = end_time - start_time

        return diff
