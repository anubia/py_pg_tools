#!/usr/bin/env python3
# -*- encoding: utf-8 -*-


import re  # To work with regular expressions

from const.const import Default


class Checker:

    def __init__(self):
        pass

    @staticmethod
    def str_is_bool(boolean):
        '''
        Target:
            - check if a string could be converted into a boolean.
        Parameters:
            - boolean: the string to be checked.
        Return:
            - a boolean with the result.
        '''
        if boolean in Default.VALID_BOOLS:
            return True
        else:
            return False

    @staticmethod
    def str_is_int(integer):
        '''
        Target:
            - check if a string could be converted into a integer.
        Parameters:
            - string: the string to be checked.
        Return:
            - a boolean with the result.
        '''
        try:
            int(integer)
            return True
        except:
            return False

    @staticmethod
    def str_is_valid_exp_days(exp_days):
        '''
        Target:
            - check if a string could be converted into a valid variable of
              expiration days. It would be any positive integer, zero or -1.
        Parameters:
            - exp_days: the string to be checked.
        Return:
            - a boolean with the result.
        '''
        try:
            result = int(exp_days)
            if result >= -1:
                return True
            else:
                return False
        except:
            return False

    @staticmethod
    def str_is_valid_max_size(max_size):
        '''
        Target:
            - check if a string could be converted into a valid variable of
              maximum size. It would be any integer followed inmediately by a
              storing unit of measure, like MegaBytes, GigaBytes, TeraBytes or
              PetaBytes (MB, GB, TB, PB).
        Parameters:
            - max_size: the string to be checked.
        Return:
            - a boolean with the result.
        '''
        regex = r'(\d+)(MB|GB|TB|PB)$'
        regex = re.compile(regex)
        if re.match(regex, max_size):
            return True
        else:
            return False

    @staticmethod
    def check_regex(regex):
        '''
        Target:
            - check if a string is a valid regex.
        Parameters:
            - regex: the string to be checked.
        Return:
            - a boolean with the result.
        '''
        try:
            re.compile(regex)
            return True
        except re.error:
            return False

    @staticmethod
    def check_compress_type(c_type):
        '''
        Target:
            - check if a string is a valid compress type.
        Parameters:
            - c_type: the string to be checked.
        Return:
            - the compress type if is valid, otherwise False.
        '''
        if c_type in Default.BKP_TYPES:
            return c_type
        else:
            return False

    @staticmethod
    def str_is_valid_mail(mail):
        '''
        Target:
            - check if a string is a valid email.
        Parameters:
            - mail: the string to be checked.
        Return:
            - a boolean with the result.
        '''
        regex = r'^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*' \
                '(\.[a-z]{2,4})$'
        regex = re.compile(regex)
        if re.match(regex, mail):
            return True
        else:
            return False

    @staticmethod
    def str_is_valid_mail_info(mail_info):
        '''
        Target:
            - check if a string could be converted into a valid variable of
              mail info. It would be an optional string followed inmediately by
              another one.
        Parameters:
            - mail_info: the string to be checked.
        Return:
            - a boolean with the result.
        '''
        regex = r'(.*)(\s)?<(.+)>$'
        regex = re.compile(regex)
        if re.match(regex, mail_info):
            return True
        else:
            return False
