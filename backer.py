#!/usr/bin/env python3
# -*- encoding: utf-8 -*-


# ************************* CARGA DE LIBRERÍAS *************************

from logger.logger import Logger
from date_tools.date_tools import DateTools
from db_selector.db_selector import DbSelector
from dir_tools.dir_tools import Dir
from messenger.messenger import Messenger
from messenger.messenger import Default
from vacuumer import Vacuumer
import subprocess


# ************************** DEFINICIÓN DE FUNCIONES **************************

class Backer:

    bkp_path = ''
    server_alias = ''
    bkp_type = ''
    prefix = ''
    in_dbs = []
    in_regex = ''
    in_forbidden = False
    in_priority = False
    ex_dbs = []
    ex_regex = ''
    ex_templates = True
    vacuum = True
    db_owner = ''
    connecter = None
    logger = None

    def __init__(self, connecter=None, bkp_path='', server_alias='',
                 bkp_type='dump', prefix='', in_dbs=[], in_regex='',
                 in_forbidden=False, in_priority=False, ex_dbs=['postgres'],
                 ex_regex='', ex_templates=True, vacuum=True, db_owner='',
                 logger=None):

        if logger:
            self.logger = logger
        else:
            self.logger = Logger()

        if connecter:
            self.connecter = connecter
        else:
            self.logger.stop_exe(Messenger.NO_CONNECTION_PARAMS)

        if bkp_path:
            self.bkp_path = bkp_path
        else:
            self.bkp_path = Default.BKP_PATH
            Dir.create_dir(self.bkp_path, self.logger)
        if server_alias:
            self.server_alias = server_alias
        else:
            self.server_alias = Default.SERVER_ALIAS
        if bkp_type:
            self.bkp_type = bkp_type
        else:
            self.bkp_type = Default.BKP_TYPE
        self.prefix = prefix
        self.in_dbs = in_dbs
        self.in_regex = in_regex
        self.in_forbidden = in_forbidden
        self.in_priority = in_priority
        self.ex_dbs = ex_dbs
        self.ex_regex = ex_regex
        self.ex_templates = ex_templates
        self.vacuum = vacuum
        self.db_owner = db_owner

    def backup_db(self, dbname, bkps_dir):
        '''
    Objetivo:
        - crear una copia de seguridad de la base de datos especificada.
    Parámetros:
        - logger: el logger que se empleará para mostrar y registrar el
        mensaje.
        - bkps_dir: directorio donde se guardan las copias de seguridad.
        - bkp_type: tipo de extensión que tendrá el archivo que contiene la
        copia.
        - dbname: nombre de la base de datos de la que se quiere realizar una
        copia de seguridad.
        - conn: conexión realizada desde el script a PostgreSQL.
        - prefix: prefijo a incluir en el nombre de las copias de seguridad.
    '''
        success = True
        # Obtener fecha y hora actuales de la zona
        init_ts = DateTools.get_date()
        # Obtener el año de la fecha almacenada
        year = str(DateTools.get_year(init_ts))
        # Obtener el mes de la fecha almacenada
        month = str(DateTools.get_month(init_ts))
        bkp_dir = bkps_dir + year + '/' + month + '/'
        Dir.create_dir(bkp_dir, self.logger)
        # Establecer nombre del archivo que contiene la copia de seguridad
        file_name = self.prefix + 'db_' + dbname + '_' + init_ts + '.' + \
            self.bkp_type
        # Almacenar la instrucción a realizar en consola
        if self.bkp_type == 'gz':  # Comprimir con gzip
            command = 'pg_dump {} -Fc -U {} -h {} -p {} | gzip > {}'.format(
                dbname, self.connecter.user, self.connecter.server,
                self.connecter.port, bkp_dir + file_name)
        elif self.bkp_type == 'bz2':  # Comprimir con bzip2
            command = 'pg_dump {} -Fc -U {} -h {} -p {} | bzip2 > {}'.format(
                dbname, self.connecter.user, self.connecter.server,
                self.connecter.port, bkp_dir + file_name)
        elif self.bkp_type == 'zip':  # Comprimir con zip
            command = 'pg_dump {} -Fc -U {} -h {} -p {} | zip > {}'.format(
                dbname, self.connecter.user, self.connecter.server,
                self.connecter.port, bkp_dir + file_name)
        else:  # No comprimir la copia
            command = 'pg_dump {} -Fc -U {} -h {} -p {} > {}'.format(
                dbname, self.connecter.user, self.connecter.server,
                self.connecter.port, bkp_dir + file_name)
        try:  # Probar que la copia se realiza correctamente
            # Ejecutar la instrucción de la copia de seguridad en consola
            result = subprocess.call(command, shell=True)
            if result != 0:  # Si el comando no de resultados en consola...
                raise Exception()  # Lanzar excepción
        except Exception as e:
            self.logger.debug('Error en la función "backup_db": {}.'.format(
                str(e)))
            success = False
        return success

    def backup_dbs(self, dbs_all):
        '''
    Objetivo:
        - crear copias de seguridad de las bases de datos especificadas, las
        que están incluidas en la variable "dbs_all".
    Parámetros:
        - logger: el logger que se empleará para mostrar y registrar el
        mensaje.
        - conn: conexión realizada desde el script a PostgreSQL.
        - dbs_all: una lista con todos los nombres de las bases de datos de
        PostgreSQL de las que se desea hacer una copia de seguridad (vienen
        dadas por el archivo de configuración).
        - bkp_dir: directorio donde se guardan las copias de seguridad.
        - bkp_vars: diccionario con los parámetros especificados en el archivo
        .cfg
    '''
        message = Messenger.CHECKING_BACKUP_DIR
        bkps_dir = self.bkp_path + self.server_alias + '/db_backups/'
        Dir.create_dir(bkps_dir, self.logger)
        message += Messenger.DIR_EXISTS
        self.logger.highlight('info', message, 'white')
        self.logger.highlight('info', Messenger.PROCESSING_DUMPER, 'white')
        # Para cada base de datos de la que se quiere backup...
        for db in dbs_all:
            dbname = db['name']  # Almacenar nombre de la BD por claridad
            mod_allow_conn = False  # En principio no se modifica datallowconn
            # Si se exigen copias de bases de datos sin permisos de conexión...
            if not db['allow_connection'] and self.in_forbidden:
                self.connecter.allow_db_conn(dbname)  # Permitir conexiones
                mod_allow_conn = True  # Marcar que se modifica datallowconn
                self.logger.info(Messenger.ALLOWING_DB_CONN)
            if self.vacuum:
                self.logger.info(Messenger.PRE_VACUUMING_DB.format(
                    dbname=dbname))
                vacuumer = Vacuumer(self.connecter, self.in_dbs, self.in_regex,
                                    self.in_forbidden, self.in_priority,
                                    self.ex_dbs, self.ex_regex,
                                    self.ex_templates, self.db_owner,
                                    self.logger)
                success = vacuumer.vacuum_db(dbname)
                if success:
                    self.logger.info(Messenger.PRE_VACUUMING_DB_DONE.format(
                        dbname=dbname))
                else:
                    self.logger.warning(Messenger.PRE_VACUUMING_DB_FAIL.format(
                        dbname=dbname))
            self.logger.info(Messenger.BEGINNING_DB_BACKER.format(
                dbname=dbname))
            # Realizar copia de seguridad de la base de datos
            success = self.backup_db(dbname, bkps_dir)
            if mod_allow_conn:  # Si se modificó datallowconn...
                # Deshabilitar nuevamente las conexiones y dejarlo como estaba
                self.connecter.disallow_db_conn(dbname)
                self.logger.info(Messenger.DISALLOWING_DB_CONN)
            if success:
                message = Messenger.DB_BACKER_DONE.format(dbname=dbname)
                self.logger.highlight('info', message, 'green')
            else:
                message = Messenger.DB_BACKER_FAIL.format(dbname=dbname)
                self.logger.highlight('warning', message, 'yellow',
                                      effect='bold')
        self.logger.highlight('info', Messenger.DBS_BACKER_DONE, 'green')


class BackerCluster:

    bkp_path = ''
    server_alias = ''
    bkp_type = ''
    prefix = ''
    vacuum = True
    connecter = None
    logger = None

    def __init__(self, connecter=None, bkp_path='', server_alias='',
                 bkp_type='dump', prefix='', vacuum=True, logger=None):

        if logger:
            self.logger = logger
        else:
            self.logger = Logger()

        if connecter:
            self.connecter = connecter
        else:
            self.logger.stop_exe(Messenger.NO_CONNECTION_PARAMS)

        if bkp_path:
            self.bkp_path = bkp_path
        else:
            self.bkp_path = Default.BKP_PATH
            Dir.create_dir(self.bkp_path, self.logger)
        if server_alias:
            self.server_alias = server_alias
        else:
            self.server_alias = Default.SERVER_ALIAS
        if bkp_type:
            self.bkp_type = bkp_type
        else:
            self.bkp_type = Default.BKP_TYPE
        self.prefix = prefix
        self.vacuum = vacuum

    def backup_all(self, bkps_dir):
        '''
    Objetivo:
        - crear una copia de seguridad del cluster de PostgreSQL del servidor
        especificado.
    Parámetros:
        - bkp_dir: directorio donde se guardan las copias de seguridad.
        - ext: tipo de extensión que tendrá el archivo que contiene la copia.
        - conn: conexión realizada desde el script a PostgreSQL.
        - prefix: prefijo a incluir en el nombre de las copias de seguridad
    '''
        success = True
        # Obtener fecha y hora actuales de la zona
        init_ts = DateTools.get_date()
        # Obtener el año de la fecha almacenada
        year = str(DateTools.get_year(init_ts))
        # Obtener el mes de la fecha almacenada
        month = str(DateTools.get_month(init_ts))
        bkp_dir = bkps_dir + year + '/' + month + '/'
        Dir.create_dir(bkp_dir, self.logger)
        # Establecer nombre del archivo que contiene la copia de seguridad
        file_name = self.prefix + 'ht_' + self.connecter.server + \
            str(self.connecter.port) + '_cluster_' + init_ts + '.' + \
            self.bkp_type
        # Almacenar la instrucción a realizar en consola
        if self.bkp_type == 'gz':  # Comprimir con gzip
            command = 'pg_dumpall -U {} -h {} -p {} | gzip > {}'.format(
                self.connecter.user, self.connecter.server,
                self.connecter.port, bkp_dir + file_name)
        elif self.bkp_type == 'bz2':  # Comprimir con bzip2
            command = 'pg_dumpall -U {} -h {} -p {} | bzip2 > {}'.format(
                self.connecter.user, self.connecter.server,
                self.connecter.port, bkp_dir + file_name)
        elif self.bkp_type == 'zip':  # Comprimir con zip
            command = 'pg_dumpall -U {} -h {} -p {} | zip > {}'.format(
                self.connecter.user, self.connecter.server,
                self.connecter.port, bkp_dir + file_name)
        else:  # No comprimir la copia
            command = 'pg_dumpall -U {} -h {} -p {} > {}'.format(
                self.connecter.user, self.connecter.server,
                self.connecter.port, bkp_dir + file_name)
        try:  # Probar que la copia se realiza correctamente
            # Ejecutar la instrucción de la copia de seguridad en consola
            result = subprocess.call(command, shell=True)
            if result != 0:  # Si el comando no de resultados en consola...
                raise Exception()  # Lanzar excepción
        except Exception as e:
            self.logger.debug('Error en la función "backup_all": {}.'.format(
                str(e)))
            success = False
        return success

    def backup_cl(self):
        '''
    Objetivo:
        - crear copias de seguridad de las bases de datos especificadas, las
        que están incluidas en la variable "dbs_all".
    Parámetros:
        - logger: el logger que se empleará para mostrar y registrar el
        mensaje.
        - bkp_dir: directorio donde se guardan las copias de seguridad.
        - conn: conexión realizada desde el script a PostgreSQL.
        - bkp_vars: diccionario con los parámetros especificados en el archivo
        .cfg
    '''
        message = Messenger.CHECKING_BACKUP_DIR
        bkps_dir = self.bkp_path + self.server_alias + '/cluster_backups/'
        Dir.create_dir(bkps_dir, self.logger)
        message += Messenger.DIR_EXISTS
        self.logger.highlight('info', message, 'white')

        self.logger.highlight('info', Messenger.BEGINNING_CL_BACKER, 'white')

        if self.vacuum:
            vacuumer = Vacuumer(connecter=self.connecter, logger=self.logger)
            dbs_all = DbSelector.list_pg_dbs(self.connecter.cursor)
            vacuumer.vacuum_dbs(dbs_all)

        success = self.backup_all(bkps_dir)
        if success:
            self.logger.highlight('info', Messenger.CL_BACKER_DONE, 'green')
        else:
            self.logger.highlight('warning', Messenger.CL_BACKER_FAIL,
                                  'yellow', effect='bold')
