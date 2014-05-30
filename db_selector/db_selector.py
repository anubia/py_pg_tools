#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

import re

from const.const import Messenger
from logger.logger import Logger


class DbSelector:

    def __init__(self):
        pass

    @staticmethod
    def db_filter_include(dbs_list, in_dbs=[], in_regex='', logger=None):
        '''
        Target:
            - filter a list of databases to get only the specified ones, taking
              into account the received parameters.
        Parameters:
            - dbs_list: list to filter.
            - in_dbs: list with the databases' names to include.
            - in_regex: regular expression which indicates the databases' names
              to include.
            - logger: a logger to show and log some messages.
        Return:
            - a filtered list (subset of "dbs_list"), value from the addition
              of the include conditions "in_dbs" y "in_regex".
        '''
        if not logger:
            logger = Logger()

        dbs_filtered = []

        if '*' in in_dbs:  # If include all...
            return dbs_list  # Return the whole list

        if in_regex:
            for db in dbs_list:
                dbname = db['name']
                # If database's name is in the inclusion list or matches the
                # regular expression...
                if dbname in in_dbs or re.match(in_regex, dbname):
                    dbs_filtered.append(db)  # Add database to the list
                    logger.debug('Base de datos incluida: {}'.format(dbname))
        else:
            for db in dbs_list:
                dbname = db['name']
                # If database's name is in the inclusion list...
                if dbname in in_dbs:
                    dbs_filtered.append(db)  # Add database to the list
                    logger.debug('Base de datos incluida: {}'.format(dbname))

        return dbs_filtered

    @staticmethod
    def db_filter_exclude(dbs_list, ex_dbs=[], ex_regex='', logger=None):
        '''
        Target:
            - filter a list of databases to remove only the specified ones,
              taking into account the received parameters.
        Parameters:
            - dbs_list: list to filter.
            - ex_dbs: list with the databases' names to exclude.
            - ex_regex: regular expression which indicates the databases' names
              to exclude.
            - logger: a logger to show and log some messages.
        Return:
            - a filtered list (subset of "dbs_list"), value from the addition
              of the exclude conditions "ex_dbs" y "ex_regex".
        '''
        if not logger:
            logger = Logger()

        # Copy the list to remove remove positions without conflict errors
        dbs_filtered = dbs_list[:]

        if '*' in ex_dbs:  # If exclude all...
            return []  # Return an empty list

        if ex_regex:
            for db in dbs_list:
                dbname = db['name']
                # If database's name is in the exclusion list or matches the
                # regular expression...
                if dbname in ex_dbs or re.match(ex_regex, dbname):
                    # Remove database from the list
                    dbs_filtered.remove(db)
                    logger.debug('Base de datos excluida: {}'.format(dbname))
        else:
            for db in dbs_list:
                dbname = db['name']
                # If database's name is in the exclusion list...
                if dbname in ex_dbs:
                    # Remove database from the list
                    dbs_filtered.remove(db)
                    logger.debug('Base de datos excluida: {}'.format(dbname))

        return dbs_filtered

    @staticmethod
    def get_filtered_dbs(dbs_all, in_dbs=[], ex_dbs=[], in_regex='',
                         ex_regex='', in_priority=False, logger=None):
        '''
        Target:
            - filter a database's list taking into account inclusion and
              exclusion parameters and their priority.
        Parameters:
            - dbs_all: list to filter.
            - in_dbs: list with the databases' names to include.
            - ex_dbs: list with the databases' names to exclude.
            - in_regex: regular expression which indicates the databases' names
              to include.
            - ex_regex: regular expression which indicates the databases' names
              to exclude.
            - in_priority: a flag which determinates if the inclusion
              parameters must predominate over the exclusion ones.
            - logger: a logger to show and log some messages.
        Return:
            - a filtered list (subset of "dbs_all").
        '''
        if not logger:
            logger = Logger()

        bkp_list = []

        if in_priority:  # If inclusion is over exclusion
            # Apply exclusion first and then inclusion
            bkp_list = DbSelector.db_filter_exclude(dbs_all, ex_dbs, ex_regex,
                                                    logger)
            bkp_list = DbSelector.db_filter_include(bkp_list, in_dbs, in_regex,
                                                    logger)
        else:  # If exclusion is over inclusion
            # Apply inclusion first and then exclusion
            bkp_list = DbSelector.db_filter_include(dbs_all, in_dbs, in_regex,
                                                    logger)
            bkp_list = DbSelector.db_filter_exclude(bkp_list, ex_dbs, ex_regex,
                                                    logger)

        logger.highlight('info', Messenger.SEARCHING_SELECTED_DBS, 'white')

        if bkp_list == []:
            logger.highlight('warning', Messenger.EMPTY_DB_LIST, 'yellow')
        else:
            for db in bkp_list:
                logger.info(Messenger.SELECTED_DB.format(dbname=db['name']))

        return bkp_list

    @staticmethod
    def dbname_filter_include(dbs_list, in_dbs=[], in_regex='', logger=None):
        '''
        Target:
            - filter a list of databases' names to get only the specified ones,
              taking into account the received parameters.
        Parameters:
            - dbs_list: list to filter.
            - in_dbs: list with the databases' names to include.
            - in_regex: regular expression which indicates the databases' names
              to include.
            - logger: a logger to show and log some messages.
        Return:
            - a filtered list (subset of "dbs_list"), value from the addition
              of the include conditions "in_dbs" y "in_regex".
        '''
        if not logger:
            logger = Logger()

        dbs_filtered = []

        if '*' in in_dbs:  # If include all...
            return dbs_list  # Return the whole list

        if in_regex:
            for dbname in dbs_list:
                # If database's name is in the inclusion list or matches the
                # regular expression...
                if dbname in in_dbs or re.match(in_regex, dbname):
                    dbs_filtered.append(dbname)  # Add database to the list
                    logger.debug('Base de datos incluida: {}'.format(dbname))
        else:
            for dbname in dbs_list:
                # If database's name is in the inclusion list...
                if dbname in in_dbs:
                    dbs_filtered.append(dbname)  # Add database to the list
                    logger.debug('Base de datos incluida: {}'.format(dbname))

        return dbs_filtered

    @staticmethod
    def dbname_filter_exclude(dbs_list, ex_dbs=[], ex_regex='', logger=None):
        '''
        Target:
            - filter a list of databases' names to remove only the specified
              ones, taking into account the received parameters.
        Parameters:
            - dbs_list: list to filter.
            - ex_dbs: list with the databases' names to exclude.
            - ex_regex: regular expression which indicates the databases' names
              to exclude.
            - logger: a logger to show and log some messages.
        Return:
            - a filtered list (subset of "dbs_list"), value from the addition
              of the exclude conditions "ex_dbs" y "ex_regex".
        '''
        if not logger:
            logger = Logger()

        # Copy the list to remove remove positions without conflict errors
        dbs_filtered = dbs_list[:]

        if '*' in ex_dbs:  # If exclude all...
            return []  # Return an empty list

        if ex_regex:
            for dbname in dbs_list:
                # If database's name is in the exclusion list or matches the
                # regular expression...
                if dbname in ex_dbs or re.match(ex_regex, dbname):
                    # Remove database from the list
                    dbs_filtered.remove(dbname)
                    logger.debug('Base de datos excluida: {}'.format(dbname))
        else:
            for dbname in dbs_list:
                # If database's name is in the exclusion list...
                if dbname in ex_dbs:
                    # Remove database from the list
                    dbs_filtered.remove(dbname)
                    logger.debug('Base de datos excluida: {}'.format(dbname))

        return dbs_filtered

    @staticmethod
    def get_filtered_dbnames(dbs_all, in_dbs=[], ex_dbs=[], in_regex='',
                             ex_regex='', in_priority=False, logger=None):
        '''
        Target:
            - filter a list of databases' names taking into account inclusion
              and exclusion parameters and their priority.
        Parameters:
            - dbs_all: list to filter.
            - in_dbs: list with the databases' names to include.
            - ex_dbs: list with the databases' names to exclude.
            - in_regex: regular expression which indicates the databases' names
              to include.
            - ex_regex: regular expression which indicates the databases' names
              to exclude.
            - in_priority: a flag which determinates if the inclusion
              parameters must predominate over the exclusion ones.
            - logger: a logger to show and log some messages.
        Return:
            - a filtered list (subset of "dbs_all").
        '''
        if not logger:
            logger = Logger()

        bkp_list = []

        if in_priority:  # If inclusion is over exclusion
            # Apply exclusion first and then inclusion
            bkp_list = DbSelector.dbname_filter_exclude(dbs_all, ex_dbs,
                                                        ex_regex, logger)
            bkp_list = DbSelector.dbname_filter_include(bkp_list, in_dbs,
                                                        in_regex, logger)
        else:
            # Apply inclusion first and then exclusion
            bkp_list = DbSelector.dbname_filter_include(dbs_all, in_dbs,
                                                        in_regex, logger)
            bkp_list = DbSelector.dbname_filter_exclude(bkp_list, ex_dbs,
                                                        ex_regex, logger)

        logger.highlight('info', Messenger.SEARCHING_SELECTED_DBS, 'white')

        if bkp_list == []:
            logger.highlight('warning', Messenger.EMPTY_DBNAME_LIST, 'yellow',
                             effect='bold')
        else:
            for dbname in bkp_list:
                logger.info(Messenger.SELECTED_DB.format(dbname=dbname))
        return bkp_list

    @staticmethod
    def list_pg_dbs(cursor):
        '''
        Target:
            - turns a cursor's data into a list.
        Parameters:
            - cursor: a connection cursor with data stored.
        Return:
            - a list with dictionaries which have databases' name, connection
              permissions and their owner stored.
        '''
        dbs_all = []

        for record in cursor:
            dictionary = {
                'name': record['datname'],
                'allow_connection': record['datallowconn'],
                'owner': record['owner'],
            }
            dbs_all.append(dictionary)  # Add database info to list

        return dbs_all

    @staticmethod
    def list_pg_dbnames(cursor):
        '''
        Target:
            - turns a cursor's data into a list.
        Parameters:
            - cursor: a connection cursor with data stored.
        Return:
            - a list with databases' name.
        '''
        dbs_all = []

        for record in cursor:
            dbs_all.append(record['datname'])  # Add database's name to list

        return dbs_all
