#!/usr/bin/env python3
# -*- encoding: utf-8 -*-


# ************************* CARGA DE LIBRERÍAS *************************

from const.const import Messenger
from logger.logger import Logger
import re  # Importar la librería re (para trabajar con expresiones regulares)


# ************************* DEFINICIÓN DE FUNCIONES *************************

class DbSelector:

    def __init__(self):
        pass

    @staticmethod
    def db_filter_include(dbs_list, in_dbs=[], in_regex='', logger=None):
        '''
    Objetivo:
        - filtrar una lista de bases de datos para obtener sólo las
        especificadas en el apartado de inclusión del archivo de configuración.
    Parámetros:
        - logger: el logger que se empleará para mostrar y registrar el
        mensaje.
        - dbs_list: lista con las bases de datos a filtrar.
        - in_dbs: lista con las bases de datos a incluir.
        - in_regex: expresión regular que indica las bases de datos a incluir.
    Devolución:
        - una lista que contiene un subconjunto de la lista "dbs_list",
        resultado de la adición de las condiciones de inclusión determinadas
        por "in_dbs" y "in_regex".
    '''
        if not logger:
            logger = Logger()
        dbs_filtered = []  # Inicializar a vacía la lista filtrada de BDs
        if '*' in in_dbs:  # Si se especifica que se incluyan todas...
            return dbs_list  # Devolver directamente la lista entera

        if in_regex:  # Si se especificó una expresión regular de inclusión...
            # Para cada base de datos de la lista a analizar...
            for db in dbs_list:
                # Almacenar el nombre de la BD por claridad
                dbname = db['name']
                # Si el nombre está en la lista de inclusión o cumple la
                # expresión regular de inclusión...
                if dbname in in_dbs or re.match(in_regex, dbname):
                    dbs_filtered.append(db)  # Añadir base de datos a la lista
                    logger.debug('Base de datos incluida: {}'.format(dbname))
        else:  # Si no se especificó una expresión regular de inclusión...
            # Para cada base de datos de la lista a analizar...
            for db in dbs_list:
                # Almacenar el nombre de la BD por claridad
                dbname = db['name']
                # Si el nombre de la base de datos está en la lista de
                # inclusión...
                if dbname in in_dbs:
                    dbs_filtered.append(db)  # Añadir base de datos a la lista
                    logger.debug('Base de datos incluida: {}'.format(dbname))

        # Devolver una lista con las bases de datos incluidas de la lista
        # recibida
        return dbs_filtered

    @staticmethod
    def db_filter_exclude(dbs_list, ex_dbs=[], ex_regex='', logger=None):
        '''
    Objetivo:
        - filtrar una lista de bases de datos para excluir sólo las
        especificadas en el apartado de exclusión del archivo de configuración.
    Parámetros:
        - logger: el logger que se empleará para mostrar y registrar el
        mensaje.
        - dbs_list: lista con las bases de datos a filtrar.
        - ex_dbs: lista con las bases de datos a excluir.
        - ex_regex: expresión regular que indica las bases de datos a excluir.
    Devolución:
        - una lista que contiene un subconjunto de la lista "dbs_list",
        resultado de la adición de las condiciones de exclusión determinadas
        por "ex_dbs" y "ex_regex".
    '''
        if not logger:
            logger = Logger()
        dbs_filtered = dbs_list[:]  # Realizar una copia del listado a filtrar
        if '*' in ex_dbs:  # Si se especifica que se excluyan todas...
            return []  # Devolver directamente una lista vacía

        if ex_regex:  # Si se especificó una expresión regular de exclusión...
            # Para cada base de datos de la lista a analizar..
            for db in dbs_list:
                # Almacenar el nombre de la BD por claridad
                dbname = db['name']
                # Si el nombre está en la lista de exclusión o cumple la
                # expresión regular de exclusión...
                if dbname in ex_dbs or re.match(ex_regex, dbname):
                    # Eliminar base de datos de la lista
                    dbs_filtered.remove(db)
                    logger.debug('Base de datos excluida: {}'.format(dbname))
        else:  # Si no se especificó una expresión regular de exclusión...
            # Para cada base de datos de la lista a analizar...
            for db in dbs_list:
                # Almacenar el nombre de la BD por claridad
                dbname = db['name']
                # Si el nombre de la base de datos está en la lista de
                # exclusión...
                if dbname in ex_dbs:
                    # Eliminar base de datos de la lista
                    dbs_filtered.remove(db)
                    logger.debug('Base de datos excluida: {}'.format(dbname))

        # Devolver una copia de la lista recibida sin las bases de datos
        # excluidas
        return dbs_filtered

    @staticmethod
    def get_filtered_dbs(dbs_all, in_dbs=[], ex_dbs=[], in_regex='',
                         ex_regex='', in_priority=False, logger=None):
        '''
    Objetivo:
        - crear un listado de las bases de datos de las que se desea realizar
        una copia de seguridad, basándose en los parámetros cargados del
        archivo de configuración.
    Parámetros:
        - logger: el logger que se empleará para mostrar y registrar el
        mensaje.
        - dbs_all: una lista con todos los nombres de las bases de datos que
        están almacenadas en el PostgreSQL del servidor local.
        - bkp_vars: diccionario con los parámetros especificados en el archivo
        .cfg
    Devolución:
        - una lista con las bases de datos de las que se desea hacer una copia.
    '''
        if not logger:
            logger = Logger()
        bkp_list = []  # Inicializar la lista a vacía
        if in_priority:  # Si inclusión predomina sobre exclusión...
            # Primero excluir y luego incluir las bases de datos
            bkp_list = DbSelector.db_filter_exclude(dbs_all, ex_dbs, ex_regex,
                                                    logger)
            bkp_list = DbSelector.db_filter_include(bkp_list, in_dbs, in_regex,
                                                    logger)
        # Si las condiciones de exclusión predominan sobre la inclusión...
        else:
            # Primero incluir y luego excluir las bases de datos
            bkp_list = DbSelector.db_filter_include(dbs_all, in_dbs, in_regex,
                                                    logger)
            bkp_list = DbSelector.db_filter_exclude(bkp_list, ex_dbs, ex_regex,
                                                    logger)

        logger.highlight('info', Messenger.SEARCHING_SELECTED_DBS, 'white')

        if bkp_list == []:
            logger.highlight('warning', Messenger.EMPTY_DB_LIST, 'yellow',
                             effect='bold')
        else:
            for db in bkp_list:
                logger.info(Messenger.SELECTED_DB.format(dbname=db['name']))
        return bkp_list

    @staticmethod
    def dbname_filter_include(dbs_list, in_dbs=[], in_regex='', logger=None):
        '''
    Objetivo:
        - filtrar una lista de bases de datos para obtener sólo las
        especificadas en el apartado de inclusión del archivo de configuración.
    Parámetros:
        - logger: el logger que se empleará para mostrar y registrar el
        mensaje.
        - dbs_list: lista con las bases de datos a filtrar.
        - in_dbs: lista con las bases de datos a incluir.
        - in_regex: expresión regular que indica las bases de datos a incluir.
    Devolución:
        - una lista que contiene un subconjunto de la lista "dbs_list",
        resultado de la adición de las condiciones de inclusión determinadas
        por "in_dbs" y "in_regex".
    '''
        if not logger:
            logger = Logger()
        dbs_filtered = []  # Inicializar a vacía la lista filtrada de BDs
        if '*' in in_dbs:  # Si se especifica que se incluyan todas...
            return dbs_list  # Devolver directamente la lista entera

        if in_regex:  # Si se especificó una expresión regular de inclusión...
            # Para cada base de datos de la lista a analizar...
            for dbname in dbs_list:
                # Si el nombre está en la lista de inclusión o cumple la
                # expresión regular de inclusión...
                if dbname in in_dbs or re.match(in_regex, dbname):
                    # Añadir base de datos a la lista
                    dbs_filtered.append(dbname)
                    logger.debug('Base de datos incluida: {}'.format(dbname))
        else:  # Si no se especificó una expresión regular de inclusión...
            # Para cada base de datos de la lista a analizar...
            for dbname in dbs_list:
                # Si el nombre de la base de datos está en la lista de
                # inclusión...
                if dbname in in_dbs:
                    # Añadir base de datos a la lista
                    dbs_filtered.append(dbname)
                    logger.debug('Base de datos incluida: {}'.format(dbname))

        # Devolver una lista con las bases de datos incluidas de la lista
        # recibida
        return dbs_filtered

    @staticmethod
    def dbname_filter_exclude(dbs_list, ex_dbs=[], ex_regex='', logger=None):
        '''
    Objetivo:
        - filtrar una lista de bases de datos para excluir sólo las
        especificadas en el apartado de exclusión del archivo de configuración.
    Parámetros:
        - logger: el logger que se empleará para mostrar y registrar el
        mensaje.
        - dbs_list: lista con las bases de datos a filtrar.
        - ex_dbs: lista con las bases de datos a excluir.
        - ex_regex: expresión regular que indica las bases de datos a excluir.
    Devolución:
        - una lista que contiene un subconjunto de la lista "dbs_list",
        resultado de la adición de las condiciones de exclusión determinadas
        por "ex_dbs" y "ex_regex".
    '''
        if not logger:
            logger = Logger()
        dbs_filtered = dbs_list[:]  # Realizar una copia del listado a filtrar
        if '*' in ex_dbs:  # Si se especifica que se excluyan todas...
            return []  # Devolver directamente una lista vacía

        if ex_regex:  # Si se especificó una expresión regular de exclusión...
            # Para cada base de datos de la lista a analizar..
            for dbname in dbs_list:
                # Si el nombre está en la lista de exclusión o cumple la
                # expresión regular de exclusión...
                if dbname in ex_dbs or re.match(ex_regex, dbname):
                    # Eliminar base de datos de la lista
                    dbs_filtered.remove(dbname)
                    logger.debug('Base de datos excluida: {}'.format(dbname))
        else:  # Si no se especificó una expresión regular de exclusión...
            # Para cada base de datos de la lista a analizar...
            for dbname in dbs_list:
                # Si el nombre de la base de datos está en la lista de
                # exclusión...
                if dbname in ex_dbs:
                    # Eliminar base de datos de la lista
                    dbs_filtered.remove(dbname)
                    logger.debug('Base de datos excluida: {}'.format(dbname))

        # Devolver una copia de la lista recibida sin las bases de datos
        # excluidas
        return dbs_filtered

    @staticmethod
    def get_filtered_dbnames(dbs_all, in_dbs=[], ex_dbs=[], in_regex='',
                             ex_regex='', in_priority=False, logger=None):
        '''
    Objetivo:
        - crear un listado de las bases de datos de las que se desea realizar
        una copia de seguridad, basándose en los parámetros cargados del
        archivo de configuración.
    Parámetros:
        - logger: el logger que se empleará para mostrar y registrar el
        mensaje.
        - dbs_all: una lista con todos los nombres de las bases de datos que
        están almacenadas en el PostgreSQL del servidor local.
        - bkp_vars: diccionario con los parámetros especificados en el archivo
        .cfg
    Devolución:
        - una lista con las bases de datos de las que se desea hacer una copia.
    '''
        if not logger:
            logger = Logger()
        bkp_list = []  # Inicializar la lista a vacía
        if in_priority:  # Si inclusión predomina sobre exclusión...
            # Primero excluir y luego incluir las bases de datos
            bkp_list = DbSelector.dbname_filter_exclude(dbs_all, ex_dbs,
                                                        ex_regex, logger)
            bkp_list = DbSelector.dbname_filter_include(bkp_list, in_dbs,
                                                        in_regex, logger)
        # Si las condiciones de exclusión predominan sobre la inclusión...
        else:
            # Primero incluir y luego excluir las bases de datos
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
        dbs_all = []  # Inicializar lista de nombres de las bases de datos
        for record in cursor:  # Para cada registro de la consulta...
            dictionary = {  # Crear diccionario con...
                'name': record['datname'],  # Nombre de la base de datos
                # Permiso de conexión
                'allow_connection': record['datallowconn'],
                'owner': record['owner'],  # Propietario de la base de datos
            }
            dbs_all.append(dictionary)  # Añadir diccionario a la lista de BDs
        return dbs_all

    @staticmethod
    def list_pg_dbnames(cursor):
        dbs_all = []  # Inicializar lista de nombres de las bases de datos
        for record in cursor:  # Para cada registro de la consulta...
            dbs_all.append(record['datname'])
        return dbs_all
