#!/usr/bin/env python3
# -*- encoding: utf-8 -*-


# ************************* CARGA DE LIBRERÍAS *************************

from logger.logger import logger_colored
import re  # Importar la librería re (para trabajar con expresiones regulares)


# ************************* DEFINICIÓN DE FUNCIONES *************************

def db_filter_include(logger, dbs_list, in_dbs=[], in_regex=''):
    '''
Objetivo:
    - filtrar una lista de bases de datos para obtener sólo las especificadas
    en el apartado de inclusión del archivo de configuración.
Parámetros:
    - logger: el logger que se empleará para mostrar y registrar el mensaje.
    - dbs_list: lista con las bases de datos a filtrar.
    - in_dbs: lista con las bases de datos a incluir.
    - in_regex: expresión regular que indica las bases de datos a incluir.
Devolución:
    - una lista que contiene un subconjunto de la lista "dbs_list", resultado
    de la adición de las condiciones de inclusión determinadas por "in_dbs" y
    "in_regex".
'''
    dbs_filtered = []  # Inicializar a vacía la lista filtrada de BDs
    if '*' in in_dbs:  # Si se especifica que se incluyan todas...
        return dbs_list  # Devolver directamente la lista entera

    if in_regex:  # Si se especificó una expresión regular de inclusión...
        for db in dbs_list:  # Para cada base de datos de la lista a analizar..
            dbname = db['name']  # Almacenar el nombre de la BD por claridad
            # Si el nombre está en la lista de inclusión o cumple la expresión
            # regular de inclusión...
            if dbname in in_dbs or re.match(in_regex, dbname):
                dbs_filtered.append(db)  # Añadir base de datos a la lista
                logger.debug('Base de datos incluida: {}'.format(dbname))
    else:  # Si no se especificó una expresión regular de inclusión...
        for db in dbs_list:  # Para cada base de datos de la lista a analizar..
            dbname = db['name']  # Almacenar el nombre de la BD por claridad
            # Si el nombre de la base de datos está en la lista de inclusión...
            if dbname in in_dbs:
                dbs_filtered.append(db)  # Añadir base de datos a la lista
                logger.debug('Base de datos incluida: {}'.format(dbname))

    # Devolver una lista con las bases de datos incluidas de la lista recibida
    return dbs_filtered


def db_filter_exclude(logger, dbs_list, ex_dbs=[], ex_regex=''):
    '''
Objetivo:
    - filtrar una lista de bases de datos para excluir sólo las especificadas
    en el apartado de exclusión del archivo de configuración.
Parámetros:
    - logger: el logger que se empleará para mostrar y registrar el mensaje.
    - dbs_list: lista con las bases de datos a filtrar.
    - ex_dbs: lista con las bases de datos a excluir.
    - ex_regex: expresión regular que indica las bases de datos a excluir.
Devolución:
    - una lista que contiene un subconjunto de la lista "dbs_list", resultado
    de la adición de las condiciones de exclusión determinadas por "ex_dbs" y
    "ex_regex".
'''
    dbs_filtered = dbs_list[:]  # Realizar una copia del listado a filtrar
    if '*' in ex_dbs:  # Si se especifica que se excluyan todas...
        return []  # Devolver directamente una lista vacía

    if ex_regex:  # Si se especificó una expresión regular de exclusión...
        for db in dbs_list:  # Para cada base de datos de la lista a analizar..
            dbname = db['name']  # Almacenar el nombre de la BD por claridad
            # Si el nombre está en la lista de exclusión o cumple la expresión
            # regular de exclusión...
            if dbname in ex_dbs or re.match(ex_regex, dbname):
                dbs_filtered.remove(db)  # Eliminar base de datos de la lista
                logger.debug('Base de datos excluida: {}'.format(dbname))
    else:  # Si no se especificó una expresión regular de exclusión...
        for db in dbs_list:  # Para cada base de datos de la lista a analizar..
            dbname = db['name']  # Almacenar el nombre de la BD por claridad
            # Si el nombre de la base de datos está en la lista de exclusión...
            if dbname in ex_dbs:
                dbs_filtered.remove(db)  # Eliminar base de datos de la lista
                logger.debug('Base de datos excluida: {}'.format(dbname))

    # Devolver una copia de la lista recibida sin las bases de datos excluidas
    return dbs_filtered


def get_dbs_to_bkp(logger, dbs_all, bkp_vars):
    '''
Objetivo:
    - crear un listado de las bases de datos de las que se desea realizar una
    copia de seguridad, basándose en los parámetros cargados del archivo de
    configuración.
Parámetros:
    - logger: el logger que se empleará para mostrar y registrar el mensaje.
    - dbs_all: una lista con todos los nombres de las bases de datos que
    están almacenadas en el PostgreSQL del servidor local.
    - bkp_vars: diccionario con los parámetros especificados en el archivo .cfg
Devolución:
    - una lista con las bases de datos de las que se desea hacer una copia.
'''
    bkp_list = []  # Inicializar la lista a vacía
    if bkp_vars['in_priority']:  # Si inclusión predomina sobre exclusión...
        # Primero excluir y luego incluir las bases de datos
        bkp_list = db_filter_exclude(
            logger, dbs_all, bkp_vars['ex_dbs'], bkp_vars['ex_regex'])
        bkp_list = db_filter_include(
            logger, bkp_list, bkp_vars['in_dbs'], bkp_vars['in_regex'])
    else:  # Si las condiciones de exclusión predominan sobre la inclusión...
        # Primero incluir y luego excluir las bases de datos
        bkp_list = db_filter_include(
            logger, dbs_all, bkp_vars['in_dbs'], bkp_vars['in_regex'])
        bkp_list = db_filter_exclude(
            logger, bkp_list, bkp_vars['ex_dbs'], bkp_vars['ex_regex'])
    if bkp_list == []:
        logger.warning('Ninguna base de datos cumple los parámetros '
                       'especificados en el archivo de configuración: no se '
                       'realizará ninguna copia de seguridad.')
    else:
        message = 'Se realizará la acción sobre las siguientes bases de ' \
                  'datos: '
        for db in bkp_list:
            if db is bkp_list[-1]:
                message += '"{}".'.format(db['name'])
                break
            message += '"{}", '.format(db['name'])
        logger_colored(logger, 'info', message, 'white')
    return bkp_list


def dbname_filter_include(logger, dbs_list, in_dbs=[], in_regex=''):
    '''
Objetivo:
    - filtrar una lista de bases de datos para obtener sólo las especificadas
    en el apartado de inclusión del archivo de configuración.
Parámetros:
    - logger: el logger que se empleará para mostrar y registrar el mensaje.
    - dbs_list: lista con las bases de datos a filtrar.
    - in_dbs: lista con las bases de datos a incluir.
    - in_regex: expresión regular que indica las bases de datos a incluir.
Devolución:
    - una lista que contiene un subconjunto de la lista "dbs_list", resultado
    de la adición de las condiciones de inclusión determinadas por "in_dbs" y
    "in_regex".
'''
    dbs_filtered = []  # Inicializar a vacía la lista filtrada de BDs
    if '*' in in_dbs:  # Si se especifica que se incluyan todas...
        return dbs_list  # Devolver directamente la lista entera

    if in_regex:  # Si se especificó una expresión regular de inclusión...
        # Para cada base de datos de la lista a analizar...
        for dbname in dbs_list:
            # Si el nombre está en la lista de inclusión o cumple la expresión
            # regular de inclusión...
            if dbname in in_dbs or re.match(in_regex, dbname):
                dbs_filtered.append(dbname)  # Añadir base de datos a la lista
                logger.debug('Base de datos incluida: {}'.format(dbname))
    else:  # Si no se especificó una expresión regular de inclusión...
        # Para cada base de datos de la lista a analizar...
        for dbname in dbs_list:
            # Si el nombre de la base de datos está en la lista de inclusión...
            if dbname in in_dbs:
                dbs_filtered.append(dbname)  # Añadir base de datos a la lista
                logger.debug('Base de datos incluida: {}'.format(dbname))

    # Devolver una lista con las bases de datos incluidas de la lista recibida
    return dbs_filtered


def dbname_filter_exclude(logger, dbs_list, ex_dbs=[], ex_regex=''):
    '''
Objetivo:
    - filtrar una lista de bases de datos para excluir sólo las especificadas
    en el apartado de exclusión del archivo de configuración.
Parámetros:
    - logger: el logger que se empleará para mostrar y registrar el mensaje.
    - dbs_list: lista con las bases de datos a filtrar.
    - ex_dbs: lista con las bases de datos a excluir.
    - ex_regex: expresión regular que indica las bases de datos a excluir.
Devolución:
    - una lista que contiene un subconjunto de la lista "dbs_list", resultado
    de la adición de las condiciones de exclusión determinadas por "ex_dbs" y
    "ex_regex".
'''
    dbs_filtered = dbs_list[:]  # Realizar una copia del listado a filtrar
    if '*' in ex_dbs:  # Si se especifica que se excluyan todas...
        return []  # Devolver directamente una lista vacía

    if ex_regex:  # Si se especificó una expresión regular de exclusión...
        # Para cada base de datos de la lista a analizar..
        for dbname in dbs_list:
            # Si el nombre está en la lista de exclusión o cumple la expresión
            # regular de exclusión...
            if dbname in ex_dbs or re.match(ex_regex, dbname):
                # Eliminar base de datos de la lista
                dbs_filtered.remove(dbname)
                logger.debug('Base de datos excluida: {}'.format(dbname))
    else:  # Si no se especificó una expresión regular de exclusión...
        # Para cada base de datos de la lista a analizar...
        for dbname in dbs_list:
            # Si el nombre de la base de datos está en la lista de exclusión...
            if dbname in ex_dbs:
                # Eliminar base de datos de la lista
                dbs_filtered.remove(dbname)
                logger.debug('Base de datos excluida: {}'.format(dbname))

    # Devolver una copia de la lista recibida sin las bases de datos excluidas
    return dbs_filtered


def get_dbnames_to_bkp(logger, dbs_all, bkp_vars):
    '''
Objetivo:
    - crear un listado de las bases de datos de las que se desea realizar una
    copia de seguridad, basándose en los parámetros cargados del archivo de
    configuración.
Parámetros:
    - logger: el logger que se empleará para mostrar y registrar el mensaje.
    - dbs_all: una lista con todos los nombres de las bases de datos que
    están almacenadas en el PostgreSQL del servidor local.
    - bkp_vars: diccionario con los parámetros especificados en el archivo .cfg
Devolución:
    - una lista con las bases de datos de las que se desea hacer una copia.
'''
    bkp_list = []  # Inicializar la lista a vacía
    if bkp_vars['in_priority']:  # Si inclusión predomina sobre exclusión...
        # Primero excluir y luego incluir las bases de datos
        bkp_list = dbname_filter_exclude(
            logger, dbs_all, bkp_vars['ex_dbs'], bkp_vars['ex_regex'])
        bkp_list = dbname_filter_include(
            logger, bkp_list, bkp_vars['in_dbs'], bkp_vars['in_regex'])
    else:  # Si las condiciones de exclusión predominan sobre la inclusión...
        # Primero incluir y luego excluir las bases de datos
        bkp_list = dbname_filter_include(
            logger, dbs_all, bkp_vars['in_dbs'], bkp_vars['in_regex'])
        bkp_list = dbname_filter_exclude(
            logger, bkp_list, bkp_vars['ex_dbs'], bkp_vars['ex_regex'])
    if bkp_list == []:
        logger.warning('Ninguna base de datos cumple los parámetros '
                       'especificados en el archivo de configuración: no se '
                       'realizará ninguna limpieza de copias de seguridad.')
    else:
        message = 'Se realizará una limpieza de las siguientes bases de ' \
                  'datos: '
        for dbname in bkp_list:
            if dbname is bkp_list[-1]:
                message += '"{}".'.format(dbname)
                break
            message += '"{}", '.format(dbname)
        logger_colored(logger, 'info', message, 'white')
    return bkp_list
