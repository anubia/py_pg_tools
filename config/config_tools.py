#!/usr/bin/env python3
# -*- encoding: utf-8 -*-


# ************************* CARGA DE LIBRERÍAS *************************

# Importar la función logger_fatal de la librería personalizada logger.logger
# (para utilizar un logger que proporcione información al usuario)
from logger.logger import logger_fatal, logger_colored
# Importar la librería configparser (para obtener datos de un archivo .cfg)
import configparser
import re  # Importar la librería re (para trabajar con expresiones regulares)


# ************************* DEFINICIÓN DE FUNCIONES *************************

def check_regex(logger, regex):
    '''
Objetivo:
    - comprobar que una expresión regular sea correcta.
Parámetros:
    - regex: la expresión regular a analizar.
Devolución:
    - el resultado de la comprobación.
'''
    valid = True  # Inicializar regex como correcta
    try:  # Probar si hay excepciones en...
        re.compile(regex)  # Compilar regex
    except re.error as e:  # Si salta la excepción re.error...
        logger.debug('Error en la función "check_regex": {}.'.format(str(e)))
        valid = False  # Marcar regex como incorrecta
    return valid  # Devolver resultado de la comprobación


def cast_bool(boolean):
    '''
Objetivo:
    - convierte una cadena en un booleano, si la cadena es correcta.
Parámetros:
    - boolean: la cadena que se convierte a booleano.
Devolución:
    - una variable de tipo booleano, "None" si la cadena era incorrecta.
'''
    if boolean.lower() == 'true':  # Si en el .cfg se escribió True bien...
        return True
    elif boolean.lower() == 'false':  # Si en el .cfg se escribió False bien...
        return False
    else:  # Si la cadena no se puede convertir a booleano...
        return None


def str_to_list(string):
    '''
Objetivo:
    - convierte una cadena en una lista de elementos, que vendrán delimitados
    por comas. Se emplea para cargar las variables del archivo de configuración
    que deben ser tratadas como listas.
Parámetros:
    - string: la cadena que se quiere convertir en una lista.
Devolución:
    - la lista resultante de dividir la cadena por sus comas.
'''
    # Partir la cadena por sus comas y generar una lista con los fragmentos
    str_list = string.split(',')
    for i in range(len(str_list)):  # Recorrer cada elemento de la lista
        # Eliminar caracteres de espaciado a cada elemento de la lista
        str_list[i] = str_list[i].strip()
    return str_list  # Devolver una lista de elementos sin espaciados


def warn(logger, param):
    message = 'El parámetro "{}" no es válido: revise el archivo de ' \
              'configuración del programa.'.format(param)
    logger_colored(logger, 'warning', message, 'yellow', effect='bold')


def check_cfg_vars(logger, in_regex='', ex_regex='', in_forbidden=False,
                   in_priority=False, ex_templates=True, vacuum=True,
                   server_alias=None, bkp_path=None, obs_days=365, min_bkps=1):
    '''
Objetivo:
    - comprobar la validez de las expresiones regulares y las banderas del
    archivo de configuración.
Parámetros:
    - logger: el logger que se empleará para mostrar y registrar el mensaje.
    - in_regex: la expresión regular de inclusión a comprobar.
    - ex_regex: la expresión regular de exclusión a comprobar.
    - in_forbidden: bandera de inclusión de bases de datos sin permisos de
    conexión a comprobar.
    - ex_templates: bandera de exclusión de plantillas a comprobar.
    - vacuum: bandera de realización de vacuum previo a dump a comprobar.
'''
    try:  # Comprobar si algunos parámetros del .cfg son correctos
        if not check_regex(logger, in_regex):  # Si no es una regex...
            warn(logger, 'in_regex')
            raise Exception()
        if not check_regex(logger, ex_regex):  # Si no es una regex...
            warn(logger, 'ex_regex')
            raise Exception()
        if in_forbidden is None:  # Si no se pudo convertir...
            warn(logger, 'in_forbidden')
            raise Exception()
        if in_priority is None:  # Si no se pudo convertir...
            warn(logger, 'in_priority')
            raise Exception()
        if ex_templates is None:  # Si no se pudo convertir...
            warn(logger, 'ex_templates')
            raise Exception()
        if vacuum is None:  # Si no se pudo convertir...
            warn(logger, 'vacuum')
            raise Exception()
        if server_alias is '':
            warn(logger, 'server_alias')
            raise Exception()
        if bkp_path is '':
            warn(logger, 'bkp_path')
            raise Exception()
        if obs_days < 0:
            warn(logger, 'obs_days')
            raise Exception()
        if min_bkps < 0:
            warn(logger, 'min_bkps')
            raise Exception()
    # Si el programa falla al analizar las variables del .cfg...
    except Exception as e:
        logger.debug('Error en la función "check_cfg_vars": {}.'.format(
            str(e)))
        logger_fatal(logger, 'El archivo de configuración tiene parámetros '
                             'con valores incorrectos.')


def check_compress_type(logger, c_type):
    '''
Objetivo:
    - comprobar la validez de los tipos de extensión para comprimir archivos.
Parámetros:
    - logger: el logger que se empleará para mostrar y registrar el mensaje.
    - c_type: el tipo de extensión a analizar.
'''
    # Listar las extensiones admitidas
    c_ext = ['.dump', '.gz', '.bz2', '.zip']
    # Comprobar si las extensiones para comprimir las copias son válidas
    if c_type not in c_ext:
        warn(logger, 'bkp_type')
        logger.debug('Error en la función "check_compress_type".')
        logger_fatal(logger, 'El archivo de configuración tiene parámetros '
                             'con valores incorrectos.')


def check_dir(logger, path):
    '''
Objetivo:
    - comprobar que exista un directorio llamado 'pg_bkp' en el directorio
    donde se encuentra este script, de no ser así, se crea.
Parámetros:
    - logger: el logger que se empleará para mostrar y registrar el mensaje.
    - path: la ruta que debe existir o generarse.
Devolución:
    - la ruta absoluta del directorio donde se almacenarán las copias de
    seguridad de PostgreSQL.
'''
    if path and path[-1:] != '/':
        warn(logger, 'bkp_path')
        logger.debug('Error en la función "check_dir".')
        logger_fatal(logger, 'El archivo de configuración tiene parámetros '
                             'con valores incorrectos.')


def parse_dump(logger, cfg):
    '''
Objetivo:
    - obtener las variables del archivo de configuración y comprobar que son
    válidas.
Parámetros:
    - logger: el logger que se empleará para mostrar y registrar el mensaje.
    - cfg_file: la ruta con el archivo de configuración a cargar.
Devolución:
    - un diccionario con las variables cargadas del archivo de configuración.
'''
    try:  # Comprobar si el programa falla al cargar las variables del .cfg
        bkp_vars = {  # Pasar los valores del archivo .cfg a un diccionario
            'server': cfg.get('postgres', 'server').strip(),  # Servidor
            # Usuario de PostgreSQL
            'user': cfg.get('postgres', 'username').strip(),
            # Contraseña del usuario de PostgreSQL
            'pwd': cfg.get('postgres', 'password').strip(),
            'port': int(cfg.get('postgres', 'port')),  # Puerto
            'bkp_path': cfg.get('dump', 'bkp_path').strip(),
            'server_alias': cfg.get('dump', 'server_alias').strip(),
            # Nombres de las bases de datos de PostgreSQL de las que sí se
            # desea hacer una copia de seguridad
            'in_dbs': str_to_list(cfg.get('dump', 'in_dbs')),
            # Nombres de las bases de datos de PostgreSQL de las que no se
            # desea hacer una copia de seguridad
            'in_regex': cfg.get('dump', 'in_regex').strip(),
            # Expresión regular que indica de qué bases de datos de PostgreSQL
            # no se desea hacer una copia de seguridad
            'in_forbidden': cfg.get('dump', 'in_forbidden').strip(),
            # Bandera que indica si las condiciones de inclusión de bases de
            # datos predominan sobre las de exclusión a la hora de hacer copias
            'in_priority': cfg.get('dump', 'in_priority').strip(),
            # En caso de que el usuario de PostgreSQL (user) elegido sea
            # administrador de éste, indica si se desea sólo copiar las BDs de
            # las cuales es propietario un usuario concreto (db_owner)
            'db_owner': cfg.get('dump', 'db_owner').strip(),
            # Bandera que indica si se deben incluir en la copia las plantillas
            # de PostgreSQL
            'ex_dbs': str_to_list(cfg.get('dump', 'ex_dbs')),
            # Expresión regular que indica de qué bases de datos de PostgreSQL
            # se desea hacer una copia de seguridad
            'ex_regex': cfg.get('dump', 'ex_regex').strip(),
            # Bandera que indica si se deben incluir en la copia aquellas
            # bases de datos de PostgreSQL que no permiten conexiones
            'ex_templates': cfg.get('dump', 'ex_templates').strip(),
            # Tipo de compresión a realizar a la copia de seguridad de la BD
            'bkp_type': cfg.get('dump', 'bkp_type').strip(),
            # Prefijo a incluir en el nombre del archivo de la copia de la BD
            'prefix': cfg.get('dump', 'prefix').strip(),
            # Bandera que indica si se desea hacer un vacuum antes de la copia
            'vacuum': cfg.get('dump', 'vacuum').strip(),
        }
        # Convertir a bool las banderas del archivo de configuración
        bkp_vars['in_forbidden'] = cast_bool(bkp_vars['in_forbidden'])
        bkp_vars['in_priority'] = cast_bool(bkp_vars['in_priority'])
        bkp_vars['ex_templates'] = cast_bool(bkp_vars['ex_templates'])
        bkp_vars['vacuum'] = cast_bool(bkp_vars['vacuum'])

        # Comprobar la validez del directorio de destino de las copias
        check_dir(logger, bkp_vars['bkp_path'])
        # Comprobar la validez de las expresiones regulares y las banderas
        check_cfg_vars(logger, bkp_vars['in_regex'], bkp_vars['ex_regex'],
                       bkp_vars['in_forbidden'], bkp_vars['in_priority'],
                       bkp_vars['ex_templates'], bkp_vars['vacuum'],
                       bkp_vars['server_alias'])
        # Comprobar la validez del tipo de compresión de las copias
        check_compress_type(logger, bkp_vars['bkp_type'])
        # Si el programa falla al cargar las variables del .cfg...
    except Exception as e:
        logger.debug('Error en la función "parse_dump": {}.'.format(
            str(e)))
        logger_fatal(logger, 'El archivo de configuración tiene parámetros '
                             'con valores incorrectos.')
    return bkp_vars


def parse_dumpall(logger, cfg):
    '''
Objetivo:
    - obtener las variables del archivo de configuración y comprobar que son
    válidas.
Parámetros:
    - logger: el logger que se empleará para mostrar y registrar el mensaje.
    - cfg_file: la ruta con el archivo de configuración a cargar.
Devolución:
    - un diccionario con las variables cargadas del archivo de configuración.
'''
    try:  # Comprobar si el programa falla al cargar las variables del .cfg
        bkp_vars = {  # Pasar los valores del archivo .cfg a un diccionario
            'server': cfg.get('postgres', 'server').strip(),  # Servidor
            # Usuario de PostgreSQL
            'user': cfg.get('postgres', 'username').strip(),
            # Contraseña del usuario de PostgreSQL
            'pwd': cfg.get('postgres', 'password').strip(),
            'port': int(cfg.get('postgres', 'port')),  # Puerto
            'bkp_path': cfg.get('dumpall', 'bkp_path').strip(),
            'server_alias': cfg.get('dumpall', 'server_alias').strip(),
            'bkp_type': cfg.get('dumpall', 'bkp_type').strip(),
            # Prefijo a incluir en el nombre del archivo de la copia de la BD
            'prefix': cfg.get('dumpall', 'prefix').strip(),
            # Bandera que indica si se desea hacer un vacuum antes de la copia
            'vacuum': cfg.get('dumpall', 'vacuum').strip(),
        }

        # Comprobar la validez del directorio de destino de las copias
        check_dir(logger, bkp_vars['bkp_path'])
        # Comprobar la validez del tipo de compresión de las copias
        check_compress_type(logger, bkp_vars['bkp_type'])
        # Comprobar las banderas
        check_cfg_vars(logger, vacuum=bkp_vars['vacuum'],
                       server_alias=bkp_vars['server_alias'])
        # Si el programa falla al cargar las variables del .cfg...
    except Exception as e:
        logger.debug('Error en la función "parse_dumpall": {}.'.format(
            str(e)))
        logger_fatal(logger, 'El archivo de configuración tiene parámetros '
                             'con valores incorrectos.')
    return bkp_vars


def parse_vacuum(logger, cfg):
    '''
Objetivo:
    - obtener las variables del archivo de configuración y comprobar que son
    válidas.
Parámetros:
    - logger: el logger que se empleará para mostrar y registrar el mensaje.
    - cfg_file: la ruta con el archivo de configuración a cargar.
Devolución:
    - un diccionario con las variables cargadas del archivo de configuración.
'''
    try:  # Comprobar si el programa falla al cargar las variables del .cfg
        bkp_vars = {  # Pasar los valores del archivo .cfg a un diccionario
            'server': cfg.get('postgres', 'server').strip(),  # Servidor
            # Usuario de PostgreSQL
            'user': cfg.get('postgres', 'username').strip(),
            # Contraseña del usuario de PostgreSQL
            'pwd': cfg.get('postgres', 'password').strip(),
            'port': int(cfg.get('postgres', 'port')),  # Puerto
            'in_dbs': str_to_list(cfg.get('vacuum', 'in_dbs')),
            # Nombres de las bases de datos de PostgreSQL de las que no se
            # desea hacer una copia de seguridad
            'in_regex': cfg.get('vacuum', 'in_regex').strip(),
            # Expresión regular que indica de qué bases de datos de PostgreSQL
            # no se desea hacer una copia de seguridad
            'in_forbidden': cfg.get('vacuum', 'in_forbidden').strip(),
            # Bandera que indica si las condiciones de inclusión de bases de
            # datos predominan sobre las de exclusión a la hora de hacer copias
            'in_priority': cfg.get('vacuum', 'in_priority').strip(),
            # En caso de que el usuario de PostgreSQL (user) elegido sea
            # administrador de éste, indica si se desea sólo copiar las BDs de
            # las cuales es propietario un usuario concreto (db_owner)
            'db_owner': cfg.get('vacuum', 'db_owner').strip(),
            # Bandera que indica si se deben incluir en la copia las plantillas
            # de PostgreSQL
            'ex_dbs': str_to_list(cfg.get('vacuum', 'ex_dbs')),
            # Expresión regular que indica de qué bases de datos de PostgreSQL
            # se desea hacer una copia de seguridad
            'ex_regex': cfg.get('vacuum', 'ex_regex').strip(),
            # Bandera que indica si se deben incluir en la copia aquellas
            # bases de datos de PostgreSQL que no permiten conexiones
            'ex_templates': cfg.get('vacuum', 'ex_templates').strip(),
        }

        # Comprobar la validez de las expresiones regulares y las banderas
        check_cfg_vars(logger, bkp_vars['in_regex'], bkp_vars['ex_regex'],
                       bkp_vars['in_forbidden'], bkp_vars['in_priority'],
                       bkp_vars['ex_templates'])
        # Si el programa falla al cargar las variables del .cfg...
    except Exception as e:
        logger.debug('Error en la función "parse_vacuum": {}.'.format(
            str(e)))
        logger_fatal(logger, 'El archivo de configuración tiene parámetros '
                             'con valores incorrectos.')
    return bkp_vars


def parse_cleaner(logger, cfg):
    '''
Objetivo:
    - obtener las variables del archivo de configuración y comprobar que son
    válidas.
Parámetros:
    - logger: el logger que se empleará para mostrar y registrar el mensaje.
    - cfg_file: la ruta con el archivo de configuración a cargar.
Devolución:
    - un diccionario con las variables cargadas del archivo de configuración.
'''
    try:  # Comprobar si el programa falla al cargar las variables del .cfg
        bkp_vars = {  # Pasar los valores del archivo .cfg a un diccionario
            'server': cfg.get('postgres', 'server').strip(),  # Servidor
            # Usuario de PostgreSQL
            'user': cfg.get('postgres', 'username').strip(),
            # Contraseña del usuario de PostgreSQL
            'pwd': cfg.get('postgres', 'password').strip(),
            'port': int(cfg.get('postgres', 'port')),  # Puerto
            'bkp_path': cfg.get('cleaner', 'bkp_path').strip(),
            'in_dbs': str_to_list(cfg.get('cleaner', 'in_dbs')),
            # Nombres de las bases de datos de PostgreSQL de las que no se
            # desea hacer una copia de seguridad
            'in_regex': cfg.get('cleaner', 'in_regex').strip(),
            # Bandera que indica si las condiciones de inclusión de bases de
            # datos predominan sobre las de exclusión a la hora de hacer copias
            'in_priority': cfg.get('cleaner', 'in_priority').strip(),
            # Expresión regular que indica de qué bases de datos de PostgreSQL
            # no se desea hacer una copia de seguridad
            'ex_dbs': str_to_list(cfg.get('cleaner', 'ex_dbs')),
            # Expresión regular que indica de qué bases de datos de PostgreSQL
            # se desea hacer una copia de seguridad
            'ex_regex': cfg.get('cleaner', 'ex_regex').strip(),
            # Prefijo a incluir en el nombre del archivo de la copia de la BD
            'prefix': cfg.get('cleaner', 'prefix').strip(),
            'obs_days': int(cfg.get('cleaner', 'obs_days').strip()),
            'min_bkps': int(cfg.get('cleaner', 'min_bkps').strip()),
            'max_tsize': int(cfg.get('cleaner', 'max_tsize').strip()),
        }

        # Comprobar la validez de las expresiones regulares y las banderas
        check_cfg_vars(logger, bkp_vars['in_regex'], bkp_vars['ex_regex'],
                       in_priority=bkp_vars['in_priority'],
                       bkp_path=bkp_vars['bkp_path'],
                       obs_days=bkp_vars['obs_days'],
                       min_bkps=bkp_vars['min_bkps'])
        # Si el programa falla al cargar las variables del .cfg...
    except Exception as e:
        logger.debug('Error en la función "parse_cleaner": {}.'.format(
            str(e)))
        logger_fatal(logger, 'El archivo de configuración tiene parámetros '
                             'con valores incorrectos.')
    return bkp_vars


def parse_cleanerall(logger, cfg):
    '''
Objetivo:
    - obtener las variables del archivo de configuración y comprobar que son
    válidas.
Parámetros:
    - logger: el logger que se empleará para mostrar y registrar el mensaje.
    - cfg_file: la ruta con el archivo de configuración a cargar.
Devolución:
    - un diccionario con las variables cargadas del archivo de configuración.
'''
    try:  # Comprobar si el programa falla al cargar las variables del .cfg
        bkp_vars = {  # Pasar los valores del archivo .cfg a un diccionario
            'server': cfg.get('postgres', 'server').strip(),  # Servidor
            # Usuario de PostgreSQL
            'user': cfg.get('postgres', 'username').strip(),
            # Contraseña del usuario de PostgreSQL
            'pwd': cfg.get('postgres', 'password').strip(),
            'port': int(cfg.get('postgres', 'port')),  # Puerto
            'bkp_path': cfg.get('cleanerall', 'bkp_path').strip(),
            # Prefijo a incluir en el nombre del archivo de la copia de la BD
            'prefix': cfg.get('cleanerall', 'prefix').strip(),
            'obs_days': int(cfg.get('cleanerall', 'obs_days').strip()),
            'min_bkps': int(cfg.get('cleanerall', 'min_bkps').strip()),
            'max_tsize': int(cfg.get('cleanerall', 'max_tsize').strip()),
        }

        # Comprobar la validez de las expresiones regulares y las banderas
        check_cfg_vars(logger, bkp_path=bkp_vars['bkp_path'],
                       obs_days=bkp_vars['obs_days'],
                       min_bkps=bkp_vars['min_bkps'])
        # Si el programa falla al cargar las variables del .cfg...
    except Exception as e:
        logger.debug('Error en la función "parse_cleaner": {}.'.format(
            str(e)))
        logger_fatal(logger, 'El archivo de configuración tiene parámetros '
                             'con valores incorrectos.')
    return bkp_vars


def load_dump(logger, cfg_file):
    '''
Objetivo:
    - cargar el archivo de configuración con todas sus variables.
Parámetros:
    - logger: el logger que se empleará para mostrar y registrar el mensaje.
    - cfg_file: la ruta con el archivo de configuración a cargar.
Devolución:
    - un diccionario con las variables cargadas del archivo de configuración.
'''
    try:  # Probar si hay excepciones en...
        cfg = configparser.ConfigParser()  # Crear un Parser
        cfg.read(cfg_file)  # Parsear el archivo .cfg
    except Exception as e:  # Si salta una excepción...
        logger.debug('Error en la función "load_dump": {}.'.format(str(e)))
        logger_fatal(logger, 'La ruta del archivo de configuración es '
                             'incorrecta.')
    bkp_vars = parse_dump(logger, cfg)  # Obtener variables del .cfg
    return bkp_vars  # Devolver el diccionario con el resultado de la operación


def load_dumpall(logger, cfg_file):
    '''
Objetivo:
    - cargar el archivo de configuración con todas sus variables.
Parámetros:
    - logger: el logger que se empleará para mostrar y registrar el mensaje.
    - cfg_file: la ruta con el archivo de configuración a cargar.
Devolución:
    - un diccionario con las variables cargadas del archivo de configuración.
'''
    try:  # Probar si hay excepciones en...
        cfg = configparser.ConfigParser()  # Crear un Parser
        cfg.read(cfg_file)  # Parsear el archivo .cfg
    except Exception as e:  # Si salta una excepción...
        logger.debug('Error en la función "load_dumpall": {}.'.format(str(e)))
        logger_fatal(logger, 'La ruta del archivo de configuración es '
                             'incorrecta.')
    bkp_vars = parse_dumpall(logger, cfg)  # Obtener variables del .cfg
    return bkp_vars  # Devolver el diccionario con el resultado de la operación


def load_vacuum(logger, cfg_file):
    '''
Objetivo:
    - cargar el archivo de configuración con todas sus variables.
Parámetros:
    - logger: el logger que se empleará para mostrar y registrar el mensaje.
    - cfg_file: la ruta con el archivo de configuración a cargar.
Devolución:
    - un diccionario con las variables cargadas del archivo de configuración.
'''
    try:  # Probar si hay excepciones en...
        cfg = configparser.ConfigParser()  # Crear un Parser
        cfg.read(cfg_file)  # Parsear el archivo .cfg
    except Exception as e:  # Si salta una excepción...
        logger.debug('Error en la función "load_vacuum": {}.'.format(str(e)))
        logger_fatal(logger, 'La ruta del archivo de configuración es '
                             'incorrecta.')
    bkp_vars = parse_vacuum(logger, cfg)  # Obtener variables del .cfg
    return bkp_vars  # Devolver el diccionario con el resultado de la operación


def load_cleaner(logger, cfg_file):
    '''
Objetivo:
    - cargar el archivo de configuración con todas sus variables.
Parámetros:
    - logger: el logger que se empleará para mostrar y registrar el mensaje.
    - cfg_file: la ruta con el archivo de configuración a cargar.
Devolución:
    - un diccionario con las variables cargadas del archivo de configuración.
'''
    try:  # Probar si hay excepciones en...
        cfg = configparser.ConfigParser()  # Crear un Parser
        cfg.read(cfg_file)  # Parsear el archivo .cfg
    except Exception as e:  # Si salta una excepción...
        logger.debug('Error en la función "load_cleaner": {}.'.format(str(e)))
        logger_fatal(logger, 'La ruta del archivo de configuración es '
                             'incorrecta.')
    bkp_vars = parse_cleaner(logger, cfg)  # Obtener variables del .cfg
    return bkp_vars  # Devolver el diccionario con el resultado de la operación


def load_cleanerall(logger, cfg_file):
    '''
Objetivo:
    - cargar el archivo de configuración con todas sus variables.
Parámetros:
    - logger: el logger que se empleará para mostrar y registrar el mensaje.
    - cfg_file: la ruta con el archivo de configuración a cargar.
Devolución:
    - un diccionario con las variables cargadas del archivo de configuración.
'''
    try:  # Probar si hay excepciones en...
        cfg = configparser.ConfigParser()  # Crear un Parser
        cfg.read(cfg_file)  # Parsear el archivo .cfg
    except Exception as e:  # Si salta una excepción...
        logger.debug('Error en la función "load_cleanerall": {}.'.format(
            str(e)))
        logger_fatal(logger, 'La ruta del archivo de configuración es '
                             'incorrecta.')
    bkp_vars = parse_cleanerall(logger, cfg)  # Obtener variables del .cfg
    return bkp_vars  # Devolver el diccionario con el resultado de la operación
