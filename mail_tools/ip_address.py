#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

import netifaces  # To get the internal IP address of the machine
import socket  # To get the hostname
import re  # To work with regular expressions


class IpAddress:

    def __init__(self):
        pass

    @staticmethod
    def get_netifaces_ips(logger):
        '''
        Target:
            - gets the netifaces and their internal IP addresses of the machine
              which is running the script.
        Parameters:
            - logger: a logger to show and log messages.
        Return:
            - a list of dictionaries with the server's netifaces and their
              internal IP addresses or None in case of something being wrong.
        '''
        try:
            # Regular expression which cannot match the netiface's name
            regex = r'lo.*$'
            regex = re.compile(regex)

            # Find all interfaces and their IPs except for the "lo" ones
            netifaces_ips = []
            for netiface in netifaces.interfaces():
                if re.match(regex, netiface):
                    continue
                addrs = netifaces.ifaddresses(netiface)
                for item in addrs.get(netifaces.AF_INET, []):
                    if 'addr' in item.keys():
                        netifaces_ips.append({'netiface': netiface,
                                              'ip':       item['addr'], })
                        break
            return netifaces_ips

        except Exception as e:
            logger.debug('Error en la función "get_internal_ip": {}.'.format(
                str(e)))
            return None

    @staticmethod
    def get_hostname(logger):
        '''
        Target:
            - gets the name of the machine.
        Parameters:
            - logger: a logger to show and log some messages.
        Return:
            - a string with the name of the machine.
        '''
        try:
            hostname = socket.gethostname()
            return hostname

        except Exception as e:
            logger.debug('Error en la función "get_hostname": {}.'.format(
                str(e)))
            return None
