#!/usr/bin/env python3
# -*- encoding: utf-8 -*-


# ************************* CARGA DE LIBRERÍAS *************************

# Importar la funciones create_logger de la librería personalizada
# logger.logger (para utilizar un logger que muestre información al usuario)
from logger.logger import Logger
import subprocess


# ************************* DEFINICIÓN DE FUNCIONES *************************

class Vacuumer:

    in_dbs = []
    in_regex = ''
    in_forbidden = False
    in_priority = False
    ex_dbs = []
    ex_regex = ''
    ex_templates = True
    db_owner = ''
    connecter = None
    logger = None

    def __init__(self, connecter=None, in_dbs=[], in_regex='',
                 in_forbidden=False, in_priority=False, ex_dbs=['postgres'],
                 ex_regex='', ex_templates=True, db_owner='', logger=None):

        if logger:
            self.logger = logger
        else:
            self.logger = Logger()

        if connecter:
            self.connecter = connecter
        else:
            message = 'No se han especificado los parámetros de conexión.'
            self.logger.stop_exe(message)

        self.in_dbs = in_dbs
        self.in_regex = in_regex
        self.in_forbidden = in_forbidden
        self.in_priority = in_priority
        self.ex_dbs = ex_dbs
        self.ex_regex = ex_regex
        self.ex_templates = ex_templates
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
        message = 'Procesando bases de datos a limpiar...'
        self.logger.highlight('info', message, 'white')
        # Para cada base de datos de la que se quiere backup...
        for db in vacuum_list:
            dbname = db['name']  # Almacenar nombre de la BD por claridad
            mod_allow_conn = False  # En principio no se modifica datallowconn
            # Si se exigen copias de bases de datos sin permisos de conexión...
            if not db['allow_connection'] and self.in_forbidden:
                self.connecter.allow_db_conn(dbname)  # Permitir conexiones
                mod_allow_conn = True  # Marcar que se modifica datallowconn
                self.logger.info('Habilitando conexiones a la base de '
                                 'datos...')
            self.logger.info('Iniciando limpieza de la base de datos '
                             '"{}"...'.format(dbname))
            # Realizar copia de seguridad de la base de datos
            success = self.vacuum_db(dbname)
            if mod_allow_conn:  # Si se modificó datallowconn...
                # Deshabilitar nuevamente las conexiones y dejarlo como estaba
                self.connecter.disallow_db_conn(dbname)
                self.logger.info('Deshabilitando conexiones a la base de '
                                 'datos...')
            if success:
                message = 'Limpieza de la base de datos "{}" ' \
                          'completada.'.format(dbname)
                self.logger.highlight('info', message, 'green')
            else:
                message = 'La limpieza de la base de datos "{}" no se pudo ' \
                          'completar.'.format(dbname)
                self.logger.highlight('warning', message, 'yellow',
                                      effect='bold')
        message = 'Limpieza de bases de datos finalizada.'
        self.logger.highlight('info', message, 'green')
