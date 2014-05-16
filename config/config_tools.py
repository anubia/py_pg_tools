#!/usr/bin/env python3
# -*- encoding: utf-8 -*-


# ************************* CARGA DE LIBRERÍAS *************************

from logger.logger import Logger
# Importar la librería configparser (para obtener datos de un archivo .cfg)
import configparser
import os  # Importar la librería os (para trabajar con directorios y archivos
from const.const import Messenger


# ************************* DEFINICIÓN DE FUNCIONES *************************

class LogCfgParser:

    logger = None
    cfg = None
    log_vars = {}

    def __init__(self):
        pass

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
            if not self.logger:
                self.logger = Logger()
            self.logger.debug('Error en la función "load_cfg": {}.'.format(
                str(e)))
            self.logger.stop_exe(Messenger.INVALID_CFG_PATH)

    def parse_logger(self):
        '''
    Objetivo:
        - obtener las variables del archivo de configuración y comprobar que
        son válidas.
    Devolución:
        - un diccionario con las variables cargadas del archivo de
        configuración.
    '''
        try:  # Comprobar si el programa falla al cargar las variables del .cfg
            # Pasar los valores del archivo .cfg a un diccionario
            self.log_vars = {
                'log_dir': self.cfg.get('settings', 'log_dir').strip(),
                'level': self.cfg.get('settings', 'level').strip(),
                'mute': self.cfg.get('settings', 'mute').strip(),
            }
            # Si el programa falla al cargar las variables del .cfg...
        except Exception as e:
            if not self.logger:
                self.logger = Logger()
            self.logger.debug('Error en la función "parse_logger": '
                              '{}.'.format(str(e)))
            self.logger.stop_exe(Messenger.LOGGER_CFG_DAMAGED)


class CfgParser:

    logger = None
    cfg = None
    conn_vars = {}
    bkp_vars = {}
    kill_vars = {}

    def __init__(self, logger):
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
            self.logger.stop_exe(Messenger.INVALID_CFG_PATH)

    def parse_connecter(self):

        try:  # Comprobar si el programa falla al cargar las variables del .cfg
            # Pasar los valores del archivo .cfg a un diccionario
            self.conn_vars = {
                # Servidor
                'server': self.cfg.get('postgres', 'server').strip(),
                # Usuario de PostgreSQL
                'user': self.cfg.get('postgres', 'username').strip(),
                # Contraseña del usuario de PostgreSQL
                #'pwd': self.cfg.get('postgres', 'password').strip(),
                'port': self.cfg.get('postgres', 'port'),  # Puerto
            }
        except Exception as e:
            self.logger.debug('Error en la función "parse_connecter": '
                              '{}.'.format(str(e)))
            self.logger.stop_exe(Messenger.CONNECTER_CFG_DAMAGED)

    def parse_backer(self):
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
                'group': self.cfg.get('dir', 'group').strip(),
                # Tipo de compresión a realizar a la copia de seguridad de la
                # BD
                'bkp_type': self.cfg.get('file', 'bkp_type').strip(),
                # Prefijo a incluir en el nombre del archivo de la copia de la
                # BD
                'prefix': self.cfg.get('file', 'prefix').strip(),
                # Nombres de las bases de datos de PostgreSQL de las que sí se
                # desea hacer una copia de seguridad
                'in_dbs': self.cfg.get('includes', 'in_dbs'),
                # Nombres de las bases de datos de PostgreSQL de las que no se
                # desea hacer una copia de seguridad
                'in_regex': self.cfg.get('includes', 'in_regex').strip(),
                # Bandera que indica si las condiciones de inclusión de bases
                # de datos predominan sobre las de exclusión a la hora de hacer
                # copias
                'in_priority': self.cfg.get('includes', 'in_priority').strip(),
                # Bandera que indica si se deben incluir en la copia las
                # plantillas de PostgreSQL
                'ex_dbs': self.cfg.get('excludes', 'ex_dbs'),
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

        except Exception as e:
            self.logger.debug('Error en la función "parse_backer": {}.'.format(
                str(e)))
            self.logger.stop_exe(Messenger.DB_BACKER_CFG_DAMAGED)

    def parse_backer_cluster(self):
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
                'group': self.cfg.get('dir', 'group').strip(),
                'bkp_type': self.cfg.get('file', 'bkp_type').strip(),
                # Prefijo a incluir en el nombre del archivo de la copia de la
                # BD
                'prefix': self.cfg.get('file', 'prefix').strip(),
                # Bandera que indica si se desea hacer un vacuum antes de la
                # copia
                'vacuum': self.cfg.get('other', 'vacuum').strip(),
            }

            # Si el programa falla al cargar las variables del .cfg...
        except Exception as e:
            self.logger.debug('Error en la función "parse_backer_cluster": '
                              '{}.'.format(str(e)))
            self.logger.stop_exe(Messenger.CL_BACKER_CFG_DAMAGED)

    def parse_vacuumer(self):
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
                'in_dbs': self.cfg.get('includes', 'in_dbs'),
                # Nombres de las bases de datos de PostgreSQL de las que no se
                # desea hacer una copia de seguridad
                'in_regex': self.cfg.get('includes', 'in_regex').strip(),
                # Bandera que indica si las condiciones de inclusión de bases
                # de datos predominan sobre las de exclusión a la hora de hacer
                # copias
                'in_priority': self.cfg.get('includes', 'in_priority').strip(),
                # Bandera que indica si se deben incluir en la copia las
                # plantillas de PostgreSQL
                'ex_dbs': self.cfg.get('excludes', 'ex_dbs'),
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

            # Si el programa falla al cargar las variables del .cfg...
        except Exception as e:
            self.logger.debug('Error en la función "parse_vacuumer": '
                              '{}.'.format(str(e)))
            self.logger.stop_exe(Messenger.VACUUMER_CFG_DAMAGED)

    def parse_trimmer(self):
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
                'in_dbs': self.cfg.get('includes', 'in_dbs'),
                # Nombres de las bases de datos de PostgreSQL de las que no se
                # desea hacer una copia de seguridad
                'in_regex': self.cfg.get('includes', 'in_regex').strip(),
                # Bandera que indica si las condiciones de inclusión de bases
                # de datos predominan sobre las de exclusión a la hora de hacer
                # copias
                'in_priority': self.cfg.get('includes', 'in_priority').strip(),
                # Expresión regular que indica de qué bases de datos de
                # PostgreSQL no se desea hacer una copia de seguridad
                'ex_dbs': self.cfg.get('excludes', 'ex_dbs'),
                # Expresión regular que indica de qué bases de datos de
                # PostgreSQL se desea hacer una copia de seguridad
                'ex_regex': self.cfg.get('excludes', 'ex_regex').strip(),
                'min_n_bkps': self.cfg.get('conditions', 'min_n_bkps').strip(),
                'exp_days': self.cfg.get('conditions', 'exp_days').strip(),
                'max_size': self.cfg.get('conditions', 'max_size').strip(),
                # Bandera que indica si se desea hacer un vacuum antes de la
                # copia
                'pg_warnings': self.cfg.get('other', 'pg_warnings').strip(),
            }

            # Si el programa falla al cargar las variables del .cfg...
        except Exception as e:
            self.logger.debug('Error en la función "parse_trimmer": '
                              '{}.'.format(str(e)))
            self.logger.stop_exe(Messenger.DB_TRIMMER_CFG_DAMAGED)

    def parse_trimmer_cluster(self):
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
                'min_n_bkps': self.cfg.get('conditions', 'min_n_bkps').strip(),
                'exp_days': self.cfg.get('conditions', 'exp_days').strip(),
                'max_size': self.cfg.get('conditions', 'max_size').strip(),
            }

            # Si el programa falla al cargar las variables del .cfg...
        except Exception as e:
            self.logger.debug('Error en la función "parse_trimmer_cluster": '
                              '{}.'.format(str(e)))
            self.logger.stop_exe(Messenger.CL_TRIMMER_CFG_DAMAGED)

    def parse_terminator(self):
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
                'kill_all': self.cfg.get('settings', 'kill_all').strip(),
                'kill_user': self.cfg.get('settings', 'kill_user').strip(),
                'kill_dbs': self.cfg.get('settings', 'kill_dbs').strip(),
            }
            # Si el programa falla al cargar las variables del .cfg...
        except Exception as e:
            self.logger.debug('Error en la función "parse_terminator": '
                              '{}.'.format(str(e)))
            self.logger.stop_exe(Messenger.TERMINATOR_CFG_DAMAGED)
