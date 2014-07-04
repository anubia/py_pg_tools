#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

import re  # To work with regular expressions


class Casting:

    def __init__(self):
        pass

    @staticmethod
    def str_to_bool(string):
        '''
        Target:
            - converts a string into a boolean.
        Parameters:
            - string: the string to be converted.
        Return:
            - a boolean or None if the conversion was impossible.
        '''
        if string.lower() == 'true':
            return True
        elif string.lower() == 'false':
            return False
        else:
            return None

    @staticmethod
    def str_to_list(string):
        '''
        Target:
            - converts a string, delimited by commas, into a list.
        Parameters:
            - string: the string to be converted.
        Return:
            - the resultant list.
        '''
        str_list = string.split(',')  # Split the string on each comma
        if str_list == ['']:
            return []
        for i in range(len(str_list)):
            str_list[i] = str_list[i].strip()  # Delete spaces of each element
        return str_list

    @staticmethod
    def str_to_int(string):
        '''
        Target:
            - converts a string into a integer.
        Parameters:
            - string: the string to be converted.
        Return:
            - the resultant integer or False if the conversion was impossible.
        '''
        try:
            result = int(string)
            return result
        except:
            return False

    @staticmethod
    def str_to_max_size(string):
        '''
        Target:
            - converts a string into a dictionary made up by an integer and a
              string. The integer will be a size and the string a storing unit
              of measure.
        Parameters:
            - string: the string to be converted.
        Return:
            - a dictionary with the size and the unit of measure used or None
              if the conversion was impossible.
        '''
        regex = r'(\d+)(MB|GB|TB|PB)$'
        regex = re.compile(regex)
        if re.match(regex, string):
            parts = regex.search(string).groups()
            max_size = {
                'size': int(parts[0]),
                'unit': parts[1],
            }
            return max_size
        else:
            return None

    @staticmethod
    def get_equivalence(unit_measure):
        '''
        Target:
            - gets the equivalence in Bytes of the specified unit of measure.
        Parameters:
            - unit_measure: the unit of measure whose equivalence is going to
            be calculated.
        Return:
            - an integer which indicates the equivalence.
        '''
        equivalence = 10 ** 6

        if unit_measure == 'MB':
            equivalence = 10 ** 6
        elif unit_measure == 'GB':
            equivalence = 10 ** 9
        elif unit_measure == 'TB':
            equivalence = 10 ** 12
        elif unit_measure == 'PB':
            equivalence = 10 ** 15

        return equivalence

    @staticmethod
    def str_to_mail_info(string):
        '''
        Target:
            - converts a string into a dictionary made up by two strings. The
              first one will be the username of the mail account and the second
              one the address.
        Parameters:
            - string: the string to be converted.
        Return:
            - a dictionary with the username and the address of a mail account
              or None if the conversion was impossible.
        '''
        regex = r'(.*)<(.+)>$'
        regex = re.compile(regex)
        if re.match(regex, string):
            parts = regex.search(string).groups()
            mail_info = {
                'name': parts[0].strip(),
                'email': parts[1].strip(),
            }
            return mail_info
        else:
            return None
