#!/usr/bin/env python3
# -*- encoding: utf-8 -*-


# ************************* CARGA DE LIBRERÍAS *************************

# Importar la funciones create_logger de la librería personalizada
# logger.logger (para utilizar un logger que muestre información al usuario)
from logger.logger import Logger
from casting.casting import Casting
from checker.checker import Checker
from const.const import Messenger
from const.const import Default
import subprocess


# ************************* DEFINICIÓN DE FUNCIONES *************************

class Vacuumer:

    in_dbs = []
    in_regex = ''
    in_priority = False
    ex_dbs = []
    ex_regex = ''
    ex_templates = True
    db_owner = ''
    connecter = None
    logger = None

    def __init__(self, connecter=None, in_dbs=[], in_regex='',
                 in_priority=False, ex_dbs=['postgres'], ex_regex='',
                 ex_templates=True, db_owner='', logger=None):

        if logger:
            self.logger = logger
        else:
            self.logger = Logger()

        if connecter:
            self.connecter = connecter
        else:
            self.logger.stop_exe(Messenger.NO_CONNECTION_PARAMS)

        if isinstance(in_dbs, list):
            self.in_dbs = in_dbs
        else:
            self.in_dbs = Casting.str_to_list(in_dbs)

        if Checker.check_regex(in_regex):
            self.in_regex = in_regex
        else:
            self.logger.stop_exe(Messenger.INVALID_IN_REGEX)

        if isinstance(in_priority, bool):
            self.in_priority = in_priority
        elif Checker.str_is_bool(in_priority):
            self.in_priority = Casting.str_to_bool(in_priority)
        else:
            self.logger.stop_exe(Messenger.INVALID_IN_PRIORITY)

        if isinstance(ex_dbs, list):
            self.ex_dbs = ex_dbs
        else:
            self.ex_dbs = Casting.str_to_list(ex_dbs)

        if Checker.check_regex(ex_regex):
            self.ex_regex = ex_regex
        else:
            self.logger.stop_exe(Messenger.INVALID_EX_REGEX)

        if isinstance(ex_templates, bool):
            self.ex_templates = ex_templates
        elif Checker.str_is_bool(ex_templates):
            self.ex_templates = Casting.str_to_bool(ex_templates)
        else:
            self.logger.stop_exe(Messenger.INVALID_EX_TEMPLATES)

        if db_owner is None:
            self.db_owner = Default.DB_OWNER
        else:
            self.db_owner = db_owner

    def vacuum_db(self, dbname):
        '''
    Objetivo:
        - crear una copia de seguridad de la base de datos especificada.
    Parámetros:
        - logger: el logger que se empleará para mostrar y registrar el
        mensaje.
        - dbname: nombre de la base de datos de la que se quiere realizar una
        copia de seguridad.
        - conn: conexión realizada desde el script a PostgreSQL
    '''
        success = True
        # Almacenar la instrucción a realizar en consola
        command = 'vacuumdb {} -U {} -h {} -p {}'.format(
            dbname, self.connecter.user, self.connecter.server,
            self.connecter.port)
        try:  # Probar que la copia se realiza correctamente
            # Ejecutar la instrucción de la copia de seguridad en consola
            result = subprocess.call(command, shell=True)
            if result != 0:  # Si el comando no de resultados en consola...
                raise Exception()  # Lanzar excepción
        except Exception as e:
            self.logger.debug('Error en la función "vacuum_db": {}.'.format(
                str(e)))
            success = False
        return success

    def vacuum_dbs(self, vacuum_list):
        '''
    Objetivo:
        - crear copias de seguridad de las bases de datos especificadas, las
        que están incluidas en la variable "dbs_all".
    Parámetros:
        - logger: el logger que se empleará para mostrar y registrar el
        mensaje.
        - conn: conexión realizada desde el script a PostgreSQL
        - dbs_all: una lista con todos los nombres de las bases de datos de
        PostgreSQL de las que se desea hacer una copia de seguridad (vienen
        dadas por el archivo de configuración).
        - bkp_vars: diccionario con los parámetros especificados en el archivo
        .cfg
    '''
        if vacuum_list:
            self.logger.highlight('info', Messenger.BEGINNING_VACUUMER,
                                  'white')
        # Para cada base de datos de la que se quiere backup...
        for db in vacuum_list:
            dbname = db['name']  # Almacenar nombre de la BD por claridad
            # Si se exigen copias de bases de datos sin permisos de conexión...
            message = Messenger.PROCESSING_DB.format(dbname=dbname)
            self.logger.highlight('info', message, 'cyan')
            if not db['allow_connection']:
                message = Messenger.FORBIDDEN_DB_CONNECTION.format(
                    dbname=dbname)
                self.logger.highlight('warning', message, 'yellow',
                                      effect='bold')
                success = False
            else:
                # Realizar copia de seguridad de la base de datos
                success = self.vacuum_db(dbname)
            if success:
                message = Messenger.DB_VACUUMER_DONE.format(dbname=dbname)
                self.logger.highlight('info', message, 'green')
            else:
                message = Messenger.DB_VACUUMER_FAIL.format(dbname=dbname)
                self.logger.highlight('warning', message, 'yellow',
                                      effect='bold')
        self.logger.highlight('info', Messenger.VACUUMER_DONE, 'green',
                              effect='bold')
