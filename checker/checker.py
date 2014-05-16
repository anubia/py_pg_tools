#!/usr/bin/env python3
# -*- encoding: utf-8 -*-


import re  # To work with regular expressions

from const.const import Default


class Checker:

    def __init__(self):
        pass

    @staticmethod
    def str_is_bool(string):
        '''
        Target:
            - check if a string could be converted into a boolean.
        Parameters:
            - string: the string to be checked.
        Return:
            - a boolean with the result.
        '''
        if string in Default.VALID_BOOLS:
            return True
        else:
            return False

    @staticmethod
    def str_is_int(string):
        '''
        Target:
            - check if a string could be converted into a integer.
        Parameters:
            - string: the string to be checked.
        Return:
            - a boolean with the result.
        '''
        try:
            int(string)
            return True
        except:
            return False

    @staticmethod
    def str_is_valid_exp_days(string):
        '''
        Target:
            - check if a string could be converted into a valid variable of
            expiration days. It would be any positive integer, zero or -1.
        Parameters:
            - string: the string to be checked.
        Return:
            - a boolean with the result.
        '''
        try:
            result = int(string)
            if result >= -1:
                return True
            else:
                return False
        except:
            return False

    @staticmethod
    def str_is_valid_max_size(string):
        '''
        Target:
            - check if a string could be converted into a valid variable of
            maximum size. It would be any integer followed inmediately by a
            storing unit of measure, like MegaBytes, GigaBytes, TeraBytes or
            PetaBytes (MB, GB, TB, PB).
        Parameters:
            - string: the string to be checked.
        Return:
            - a boolean with the result.
        '''
        regex = r'(\d+)(MB|GB|TB|PB)$'
        regex = re.compile(regex)
        if re.match(regex, string):
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
