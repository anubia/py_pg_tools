#!/usr/bin/env python3
# -*- encoding: utf-8 -*-


# ************************* CARGA DE LIBRERÍAS *************************

from logger.logger import Logger
# Importar la librería configparser (para obtener datos de un archivo .cfg)
import configparser
import os  # Importar la librería os (para trabajar con directorios y archivos
import re  # Importar la librería re (para trabajar con expresiones regulares)


# ************************* DEFINICIÓN DE FUNCIONES *************************

class Checker:

    def __init__(self):
        pass

    @staticmethod
    def __warn(param, logger=None):
        if not logger:
            logger = Logger()
        message = 'El parámetro "{}" no es válido: revise el archivo de ' \
                  'configuración del programa.'.format(param)
        logger.highlight('warning', message, 'yellow', effect='bold')

    @staticmethod
    def check_regex(regex, logger=None):
        '''
    Objetivo:
        - comprobar que una expresión regular sea correcta.
    Parámetros:
        - regex: la expresión regular a analizar.
    Devolución:
        - el resultado de la comprobación.
    '''
        if not logger:
            logger = Logger()
        valid = True  # Inicializar regex como correcta
        try:  # Probar si hay excepciones en...
            re.compile(regex)  # Compilar regex
        except re.error as e:  # Si salta la excepción re.error...
            logger.debug('Error en la función "check_regex": {}.'.format(
                str(e)))
            valid = False  # Marcar regex como incorrecta
        return valid  # Devolver resultado de la comprobación

    @staticmethod
    def check_cfg_vars(in_regex='', ex_regex='', in_forbidden=False,
                       in_priority=False, ex_templates=True, vacuum=True,
                       server_alias=None, bkp_path=None, obs_days=365,
                       min_bkps=1, pg_warnings=True, logger=None):
        '''
    Objetivo:
        - comprobar la validez de las expresiones regulares y las banderas del
        archivo de configuración.
    Parámetros:
        - logger: el logger que se empleará para mostrar y registrar el
        mensaje.
        - in_regex: la expresión regular de inclusión a comprobar.
        - ex_regex: la expresión regular de exclusión a comprobar.
        - in_forbidden: bandera de inclusión de bases de datos sin permisos de
        conexión a comprobar.
        - ex_templates: bandera de exclusión de plantillas a comprobar.
        - vacuum: bandera de realización de vacuum previo a dump a comprobar.
    '''
        if not logger:
            logger = Logger()
        try:  # Comprobar si algunos parámetros del .cfg son correctos
            # Si no es una regex...
            if not Checker.check_regex(in_regex, logger):
                Checker.__warn('in_regex', logger)
                raise Exception()
            # Si no es una regex...
            if not Checker.check_regex(ex_regex, logger):
                Checker.__warn('ex_regex', logger)
                raise Exception()
            if in_forbidden is None:  # Si no se pudo convertir...
                Checker.__warn('in_forbidden', logger)
                raise Exception()
            if in_priority is None:  # Si no se pudo convertir...
                Checker.__warn('in_priority', logger)
                raise Exception()
            if ex_templates is None:  # Si no se pudo convertir...
                Checker.__warn('ex_templates', logger)
                raise Exception()
            if vacuum is None:  # Si no se pudo convertir...
                Checker.__warn('vacuum', logger)
                raise Exception()
            if server_alias == '':
                Checker.__warn('server_alias', logger)
                raise Exception()
            if bkp_path == '':
                Checker.__warn('bkp_path', logger)
                raise Exception()
            if obs_days < 0:
                Checker.__warn('obs_days', logger)
                raise Exception()
            if min_bkps < 0:
                Checker.__warn('min_bkps', logger)
                raise Exception()
            if pg_warnings is None:  # Si no se pudo convertir...
                Checker.__warn('pg_warnings', logger)
                raise Exception()
        # Si el programa falla al analizar las variables del .cfg...
        except Exception as e:
            logger.debug('Error en la función "check_cfg_vars": {}.'.format(
                str(e)))
            logger.stop_exe('El archivo de configuración tiene parámetros con '
                            'valores incorrectos.')

    @staticmethod
    def check_compress_type(c_type, logger=None):
        '''
    Objetivo:
        - comprobar la validez de los tipos de extensión para comprimir
        archivos.
    Parámetros:
        - logger: el logger que se empleará para mostrar y registrar el
        mensaje.
        - c_type: el tipo de extensión a analizar.
    '''
        if not logger:
            logger = Logger()
        # Listar las extensiones admitidas
        c_ext = ['.dump', '.gz', '.bz2', '.zip']
        # Comprobar si las extensiones para comprimir las copias son válidas
        if c_type not in c_ext:
            Checker.__warn('bkp_type', logger)
            logger.debug('Error en la función "check_compress_type".')
            logger.stop_exe('El archivo de configuración tiene parámetros con '
                            'valores incorrectos.')

    @staticmethod
    def check_dir(path, logger=None):
        '''
    Objetivo:
        - comprobar que exista un directorio llamado 'pg_bkp' en el directorio
        donde se encuentra este script, de no ser así, se crea.
    Parámetros:
        - logger: el logger que se empleará para mostrar y registrar el
        mensaje.
        - path: la ruta que debe existir o generarse.
    Devolución:
        - la ruta absoluta del directorio donde se almacenarán las copias de
        seguridad de PostgreSQL.
    '''
        if not logger:
            logger = Logger()
        if path and path[-1:] != '/':
            Checker.__warn(logger, 'bkp_path')
            logger.debug('Error en la función "check_dir".')
            logger.stop_exe('El archivo de configuración tiene parámetros con '
                            'valores incorrectos.')


class Casting:

    def __init__(self):
        pass

    @staticmethod
    def str_to_bool(boolean):
        '''
    Objetivo:
        - convierte una cadena en un booleano, si la cadena es correcta.
    Parámetros:
        - boolean: la cadena que se convierte a booleano.
    Devolución:
        - una variable de tipo booleano, "None" si la cadena era incorrecta.
    '''
        # Si en el .cfg se escribió True bien...
        if boolean.lower() == 'true':
            return True
        # Si en el .cfg se escribió False bien...
        elif boolean.lower() == 'false':
            return False
        else:  # Si la cadena no se puede convertir a booleano...
            return None

    @staticmethod
    def str_to_list(string):
        '''
    Objetivo:
        - convierte una cadena en una lista de elementos, que vendrán
        delimitados por comas. Se emplea para cargar las variables del archivo
        de configuración que deben ser tratadas como listas.
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


class CfgParser:

    logger = None
    cfg = None
    conn_vars = {}
    bkp_vars = {}
    kill_vars = {}

    def __init__(self, logger=None):
        if logger:
            self.logger = logger
        else:
            self.logger = Logger()

    def load_cfg(self, cfg_file):
        '''
    Objetivo:
        - cargar el archivo de configuración con todas sus variables.
    Parámetros:
        - logger: el logger que se empleará para mostrar y registrar el
        mensaje.
        - cfg_file: la ruta con el archivo de configuración a cargar.
        - action: una acción que indicará las variables a cargar, ya que éstas
        son diferentes a la hora de conectarse a PostgreSQL, hacer dump,
        dumpall, vacuum, clean o cleanall.
    Devolución:
        - un diccionario con las variables cargadas del archivo de
        configuración.
    '''
        try:  # Probar si hay excepciones en...
            self.cfg = configparser.ConfigParser()  # Crear un Parser
            if os.path.exists(cfg_file):
                self.cfg.read(cfg_file)  # Parsear el archivo .cfg
            else:
                raise Exception()
        except Exception as e:  # Si salta una excepción...
            self.logger.debug('Error en la función "load_cfg": {}.'.format(
                str(e)))
            self.logger.stop_exe('La ruta de alguno de los archivos de '
                                 'configuración es incorrecta.')

    def parse_pgconn(self):

        try:  # Comprobar si el programa falla al cargar las variables del .cfg
            # Pasar los valores del archivo .cfg a un diccionario
            self.conn_vars = {
                # Servidor
                'server': self.cfg.get('postgres', 'server').strip(),
                # Usuario de PostgreSQL
                'user': self.cfg.get('postgres', 'username').strip(),
                # Contraseña del usuario de PostgreSQL
                'pwd': self.cfg.get('postgres', 'password').strip(),
                'port': int(self.cfg.get('postgres', 'port')),  # Puerto
            }
        except Exception as e:
            self.logger.debug('Error en la función "parse_pg": {}.'.format(
                str(e)))
            self.logger.stop_exe('El archivo de configuración de la conexión '
                                 'a PostgreSQL tiene parámetros con valores '
                                 'incorrectos.')

    def parse_dump(self):
        '''
    Objetivo:
        - obtener las variables del archivo de configuración y comprobar que
        son válidas.
    Parámetros:
        - logger: el logger que se empleará para mostrar y registrar el
        mensaje.
        - cfg_file: la ruta con el archivo de configuración a cargar.
    Devolución:
        - un diccionario con las variables cargadas del archivo de
        configuración.
    '''
        try:  # Comprobar si el programa falla al cargar las variables del .cfg
            # Pasar los valores del archivo .cfg a un diccionario
            self.bkp_vars = {
                'bkp_path': self.cfg.get('dir', 'bkp_path').strip(),
                'server_alias': self.cfg.get('dir', 'server_alias').strip(),
                # Tipo de compresión a realizar a la copia de seguridad de la
                # BD
                'bkp_type': self.cfg.get('file', 'bkp_type').strip(),
                # Prefijo a incluir en el nombre del archivo de la copia de la
                # BD
                'prefix': self.cfg.get('file', 'prefix').strip(),
                # Nombres de las bases de datos de PostgreSQL de las que sí se
                # desea hacer una copia de seguridad
                'in_dbs': Casting.str_to_list(
                    self.cfg.get('includes', 'in_dbs')),
                # Nombres de las bases de datos de PostgreSQL de las que no se
                # desea hacer una copia de seguridad
                'in_regex': self.cfg.get('includes', 'in_regex').strip(),
                # Expresión regular que indica de qué bases de datos de
                # PostgreSQL no se desea hacer una copia de seguridad
                'in_forbidden': self.cfg.get(
                    'includes', 'in_forbidden').strip(),
                # Bandera que indica si las condiciones de inclusión de bases
                # de datos predominan sobre las de exclusión a la hora de hacer
                # copias
                'in_priority': self.cfg.get('includes', 'in_priority').strip(),
                # Bandera que indica si se deben incluir en la copia las
                # plantillas de PostgreSQL
                'ex_dbs': Casting.str_to_list(
                    self.cfg.get('excludes', 'ex_dbs')),
                # Expresión regular que indica de qué bases de datos de
                # PostgreSQL se desea hacer una copia de seguridad
                'ex_regex': self.cfg.get('excludes', 'ex_regex').strip(),
                # Bandera que indica si se deben incluir en la copia aquellas
                # bases de datos de PostgreSQL que no permiten conexiones
                'ex_templates': self.cfg.get(
                    'excludes', 'ex_templates').strip(),
                # Bandera que indica si se desea hacer un vacuum antes de la
                # copia
                'vacuum': self.cfg.get('other', 'vacuum').strip(),
                # En caso de que el usuario de PostgreSQL (user) elegido sea
                # administrador de éste, indica si se desea sólo copiar las BDs
                # de las cuales es propietario un usuario concreto (db_owner)
                'db_owner': self.cfg.get('other', 'db_owner').strip(),
            }
            # Convertir a bool las banderas del archivo de configuración
            self.bkp_vars['in_forbidden'] = Casting.str_to_bool(
                self.bkp_vars['in_forbidden'])
            self.bkp_vars['in_priority'] = Casting.str_to_bool(
                self.bkp_vars['in_priority'])
            self.bkp_vars['ex_templates'] = Casting.str_to_bool(
                self.bkp_vars['ex_templates'])
            self.bkp_vars['vacuum'] = Casting.str_to_bool(
                self.bkp_vars['vacuum'])

            # Comprobar la validez del directorio de destino de las copias
            Checker.check_dir(self.bkp_vars['bkp_path'], self.logger)
            # Comprobar la validez de las expresiones regulares y las banderas
            Checker.check_cfg_vars(self.bkp_vars['in_regex'],
                                   self.bkp_vars['ex_regex'],
                                   self.bkp_vars['in_forbidden'],
                                   self.bkp_vars['in_priority'],
                                   self.bkp_vars['ex_templates'],
                                   self.bkp_vars['vacuum'],
                                   self.bkp_vars['server_alias'],
                                   logger=self.logger)
            # Comprobar la validez del tipo de compresión de las copias
            Checker.check_compress_type(self.bkp_vars['bkp_type'], self.logger)
            # Si el programa falla al cargar las variables del .cfg...
        except Exception as e:
            self.logger.debug('Error en la función "parse_dump": {}.'.format(
                str(e)))
            self.logger.stop_exe('El archivo de configuración con las '
                                 'condiciones de las copias de seguridad '
                                 'tiene parámetros con valores incorrectos.')

    def parse_dumpall(self):
        '''
    Objetivo:
        - obtener las variables del archivo de configuración y comprobar que
        son válidas.
    Parámetros:
        - logger: el logger que se empleará para mostrar y registrar el
        mensaje.
        - cfg_file: la ruta con el archivo de configuración a cargar.
    Devolución:
        - un diccionario con las variables cargadas del archivo de
        configuración.
    '''
        try:  # Comprobar si el programa falla al cargar las variables del .cfg
            # Pasar los valores del archivo .cfg a un diccionario
            self.bkp_vars = {
                'bkp_path': self.cfg.get('dir', 'bkp_path').strip(),
                'server_alias': self.cfg.get('dir', 'server_alias').strip(),
                'bkp_type': self.cfg.get('file', 'bkp_type').strip(),
                # Prefijo a incluir en el nombre del archivo de la copia de la
                # BD
                'prefix': self.cfg.get('file', 'prefix').strip(),
                # Bandera que indica si se desea hacer un vacuum antes de la
                # copia
                'vacuum': self.cfg.get('other', 'vacuum').strip(),
            }

            # Comprobar la validez del directorio de destino de las copias
            Checker.check_dir(self.bkp_vars['bkp_path'], self.logger)
            # Comprobar la validez del tipo de compresión de las copias
            Checker.check_compress_type(self.bkp_vars['bkp_type'], self.logger)
            # Comprobar las banderas
            Checker.check_cfg_vars(vacuum=self.bkp_vars['vacuum'],
                                   server_alias=self.bkp_vars['server_alias'],
                                   logger=self.logger)
            # Si el programa falla al cargar las variables del .cfg...
        except Exception as e:
            self.logger.debug('Error en la función "parse_dumpall": '
                              '{}.'.format(str(e)))
            self.logger.stop_exe('El archivo de configuración con las '
                                 'condiciones de las copias de seguridad '
                                 'tiene parámetros con valores incorrectos.')

    def parse_vacuum(self):
        '''
    Objetivo:
        - obtener las variables del archivo de configuración y comprobar que
        son válidas.
    Parámetros:
        - logger: el logger que se empleará para mostrar y registrar el
        mensaje.
        - cfg_file: la ruta con el archivo de configuración a cargar.
    Devolución:
        - un diccionario con las variables cargadas del archivo de
        configuración.
    '''
        try:  # Comprobar si el programa falla al cargar las variables del .cfg
            # Pasar los valores del archivo .cfg a un diccionario
            self.bkp_vars = {
                'in_dbs': Casting.str_to_list(
                    self.cfg.get('includes', 'in_dbs')),
                # Nombres de las bases de datos de PostgreSQL de las que no se
                # desea hacer una copia de seguridad
                'in_regex': self.cfg.get('includes', 'in_regex').strip(),
                # Expresión regular que indica de qué bases de datos de
                # PostgreSQL no se desea hacer una copia de seguridad
                'in_forbidden': self.cfg.get(
                    'includes', 'in_forbidden').strip(),
                # Bandera que indica si las condiciones de inclusión de bases
                # de datos predominan sobre las de exclusión a la hora de hacer
                # copias
                'in_priority': self.cfg.get('includes', 'in_priority').strip(),
                # Bandera que indica si se deben incluir en la copia las
                # plantillas de PostgreSQL
                'ex_dbs': Casting.str_to_list(
                    self.cfg.get('excludes', 'ex_dbs')),
                # Expresión regular que indica de qué bases de datos de
                # PostgreSQL se desea hacer una copia de seguridad
                'ex_regex': self.cfg.get('excludes', 'ex_regex').strip(),
                # Bandera que indica si se deben incluir en la copia aquellas
                # bases de datos de PostgreSQL que no permiten conexiones
                'ex_templates': self.cfg.get(
                    'excludes', 'ex_templates').strip(),
                # En caso de que el usuario de PostgreSQL (user) elegido sea
                # administrador de éste, indica si se desea sólo copiar las BDs
                # de las cuales es propietario un usuario concreto (db_owner)
                'db_owner': self.cfg.get('other', 'db_owner').strip(),
            }

            # Comprobar la validez de las expresiones regulares y las banderas
            Checker.check_cfg_vars(self.bkp_vars['in_regex'],
                                   self.bkp_vars['ex_regex'],
                                   self.bkp_vars['in_forbidden'],
                                   self.bkp_vars['in_priority'],
                                   self.bkp_vars['ex_templates'],
                                   logger=self.logger)
            # Si el programa falla al cargar las variables del .cfg...
        except Exception as e:
            self.logger.debug('Error en la función "parse_vacuum": {}.'.format(
                str(e)))
            self.logger.stop_exe('El archivo de configuración con las '
                                 'condiciones de la limpieza en PostgreSQL '
                                 'tiene parámetros con valores incorrectos.')

    def parse_clean(self):
        '''
    Objetivo:
        - obtener las variables del archivo de configuración y comprobar que
        son válidas.
    Parámetros:
        - logger: el logger que se empleará para mostrar y registrar el
        mensaje.
        - cfg_file: la ruta con el archivo de configuración a cargar.
    Devolución:
        - un diccionario con las variables cargadas del archivo de
        configuración.
    '''
        try:  # Comprobar si el programa falla al cargar las variables del .cfg
            # Pasar los valores del archivo .cfg a un diccionario
            self.bkp_vars = {
                'bkp_path': self.cfg.get('dir', 'bkp_path').strip(),
                # Prefijo a incluir en el nombre del archivo de la copia de la
                # BD
                'prefix': self.cfg.get('file', 'prefix').strip(),
                'in_dbs': Casting.str_to_list(
                    self.cfg.get('includes', 'in_dbs')),
                # Nombres de las bases de datos de PostgreSQL de las que no se
                # desea hacer una copia de seguridad
                'in_regex': self.cfg.get('includes', 'in_regex').strip(),
                # Bandera que indica si las condiciones de inclusión de bases
                # de datos predominan sobre las de exclusión a la hora de hacer
                # copias
                'in_priority': self.cfg.get('includes', 'in_priority').strip(),
                # Expresión regular que indica de qué bases de datos de
                # PostgreSQL no se desea hacer una copia de seguridad
                'ex_dbs': Casting.str_to_list(
                    self.cfg.get('excludes', 'ex_dbs')),
                # Expresión regular que indica de qué bases de datos de
                # PostgreSQL se desea hacer una copia de seguridad
                'ex_regex': self.cfg.get('excludes', 'ex_regex').strip(),
                'min_bkps': int(
                    self.cfg.get('conditions', 'min_bkps').strip()),
                'obs_days': int(
                    self.cfg.get('conditions', 'obs_days').strip()),
                'max_tsize': int(
                    self.cfg.get('conditions', 'max_tsize').strip()),
                # Bandera que indica si se desea hacer un vacuum antes de la
                # copia
                'pg_warnings': self.cfg.get('other', 'pg_warnings').strip(),
            }

            # Comprobar la validez de las expresiones regulares y las banderas
            Checker.check_cfg_vars(self.bkp_vars['in_regex'],
                                   self.bkp_vars['ex_regex'],
                                   in_priority=self.bkp_vars['in_priority'],
                                   bkp_path=self.bkp_vars['bkp_path'],
                                   obs_days=self.bkp_vars['obs_days'],
                                   min_bkps=self.bkp_vars['min_bkps'],
                                   pg_warnings=self.bkp_vars['pg_warnings'],
                                   logger=self.logger)
            # Si el programa falla al cargar las variables del .cfg...
        except Exception as e:
            self.logger.debug('Error en la función "parse_cleaner": '
                              '{}.'.format(str(e)))
            self.logger.stop_exe('El archivo de configuración con las '
                                 'condiciones de la limpieza de copias de '
                                 'seguridad tiene parámetros con valores '
                                 'incorrectos.')

    def parse_cleanall(self):
        '''
    Objetivo:
        - obtener las variables del archivo de configuración y comprobar que
        son válidas.
    Parámetros:
        - logger: el logger que se empleará para mostrar y registrar el
        mensaje.
        - cfg_file: la ruta con el archivo de configuración a cargar.
    Devolución:
        - un diccionario con las variables cargadas del archivo de
        configuración.
    '''
        try:  # Comprobar si el programa falla al cargar las variables del .cfg
            # Pasar los valores del archivo .cfg a un diccionario
            self.bkp_vars = {
                'bkp_path': self.cfg.get('dir', 'bkp_path').strip(),
                # Prefijo a incluir en el nombre del archivo de la copia de la
                # BD
                'prefix': self.cfg.get('file', 'prefix').strip(),
                'min_bkps': int(
                    self.cfg.get('conditions', 'min_bkps').strip()),
                'obs_days': int(
                    self.cfg.get('conditions', 'obs_days').strip()),
                'max_tsize': int(
                    self.cfg.get('conditions', 'max_tsize').strip()),
            }

            # Comprobar la validez de las expresiones regulares y las banderas
            Checker.check_cfg_vars(bkp_path=self.bkp_vars['bkp_path'],
                                   obs_days=self.bkp_vars['obs_days'],
                                   min_bkps=self.bkp_vars['min_bkps'],
                                   logger=self.logger)
            # Si el programa falla al cargar las variables del .cfg...
        except Exception as e:
            self.logger.debug('Error en la función "parse_cleaner": '
                              '{}.'.format(str(e)))
            self.logger.stop_exe('El archivo de configuración con las '
                                 'condiciones de la limpieza de copias de '
                                 'seguridad tiene parámetros con valores '
                                 'incorrectos.')

    def parse_kill(self):
        '''
    Objetivo:
        - obtener las variables del archivo de configuración y comprobar que
        son válidas.
    Parámetros:
        - logger: el logger que se empleará para mostrar y registrar el
        mensaje.
        - cfg_file: la ruta con el archivo de configuración a cargar.
    Devolución:
        - un diccionario con las variables cargadas del archivo de
        configuración.
    '''
        try:  # Comprobar si el programa falla al cargar las variables del .cfg
            # Pasar los valores del archivo .cfg a un diccionario
            self.kill_vars = {
                'kill_all': Casting.str_to_bool(
                    self.cfg.get('settings', 'kill_all').strip()),
                'kill_user': self.cfg.get('settings', 'kill_user').strip(),
                'kill_dbs': Casting.str_to_list(
                    self.cfg.get('settings', 'kill_dbs').strip()),
            }
            # Si el programa falla al cargar las variables del .cfg...
        except Exception as e:
            self.logger.debug('Error en la función "parse_kill": '
                              '{}.'.format(str(e)))
            self.logger.stop_exe('El archivo de configuración con las '
                                 'condiciones de desconexiones de PostgreSQL '
                                 'tiene parámetros con valores incorrectos.')
