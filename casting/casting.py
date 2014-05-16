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
            string. The integer will be a size and the string a storing unit of
            measure.
        Parameters:
            - string: the string to be converted.
        Return:
            - a dictionary with the size and the unit of measure used or None
            if the conversion was impossible.
        '''
        regex = r'(\d+)(MB|GB|TB|PB)$'
        regex = re.compile(regex)  # Validar la expresión regular
        if re.match(regex, string):
            parts = regex.search(string).groups()
            max_size = {
                'size': int(parts[0]),
                'unit': parts[1],
            }
            return max_size
        else:
            return None
