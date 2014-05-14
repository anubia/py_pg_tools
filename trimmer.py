#!/usr/bin/env python3
# -*- encoding: utf-8 -*-


# ************************* CARGA DE LIBRERÍAS *************************

# Importar la funciones create_logger de la librería personalizada
# logger.logger (para utilizar un logger que muestre información al usuario)
from logger.logger import Logger
# Importar las funciones create_dir, default_bkps_path, default_cfg_path de la
# librería personalizada dir_tools.dir_tools (para crear directorios de forma
# automática y localizar archivos creados por defecto)
from dir_tools.dir_tools import Dir
from messenger.messenger import Messenger
from messenger.messenger import Default
import os  # Importar la librería os (para trabajar con directorios y archivos)
import re  # Importar la librería glob (para buscar archivos en directorios)
import time  # Importar la librería time (para calcular intervalos de tiempo)
from math import ceil
from casting.casting import Casting
from checker.checker import Checker


# ************************* DEFINICIÓN DE FUNCIONES *************************

class Trimmer:

    bkp_path = ''
    prefix = ''
    in_dbs = []
    in_regex = ''
    in_priority = False
    ex_dbs = []
    ex_regex = ''
    min_n_bkps = None
    exp_days = None
    max_size = None
    pg_warnings = True
    connecter = None
    logger = None

    def __init__(self, bkp_path='', prefix='', in_dbs=[], in_regex='',
                 in_priority=False, ex_dbs=[], ex_regex='', min_n_bkps=1,
                 exp_days=365, max_size='10000MB', pg_warnings=True,
                 connecter=None, logger=None):

        if logger:
            self.logger = logger
        else:
            self.logger = Logger()

        if bkp_path and os.path.isdir(bkp_path):
            self.bkp_path = bkp_path
        else:
            self.logger.stop_exe(Messenger.DIR_DOES_NOT_EXIST)

        if prefix is None:
            self.prefix = Default.PREFIX
        else:
            self.prefix = prefix

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

        if min_n_bkps is None:
            self.min_n_bkps = Default.MIN_N_BKPS
        elif isinstance(min_n_bkps, int):
            self.min_n_bkps = min_n_bkps
        elif Checker.str_is_int(min_n_bkps):
            self.min_n_bkps = Casting.str_to_int(min_n_bkps)
        else:
            self.logger.stop_exe(Messenger.INVALID_MIN_BKPS)

        if exp_days is None:
            self.exp_days = Default.EXP_DAYS
        elif isinstance(exp_days, int) and exp_days >= -1:
            self.exp_days = exp_days
        elif Checker.str_is_valid_exp_days(exp_days):
            self.exp_days = Casting.str_to_int(exp_days)
        else:
            self.logger.stop_exe(Messenger.INVALID_OBS_DAYS)
        if max_size is None:
            self.max_size = Default.MAX_SIZE
        elif Checker.str_is_valid_max_size(max_size):
            self.max_size = max_size
        else:
            self.logger.stop_exe(Messenger.INVALID_MAX_TSIZE)

        if isinstance(pg_warnings, bool):
            self.pg_warnings = pg_warnings
        elif Checker.str_is_bool(pg_warnings):
            self.pg_warnings = Casting.str_to_bool(pg_warnings)
        else:
            self.logger.stop_exe(Messenger.INVALID_PG_WARNINGS)

        if self.pg_warnings:
            if connecter:
                self.connecter = connecter
            else:
                self.logger.stop_exe(Messenger.NO_CONNECTION_PARAMS)

    def trim_db(self, dbname, db_bkps_list):
        '''
    Objetivo:
        - elimina los archivos de copias de seguridad de bases de datos,
        teniendo en cuenta los parámetros de configuración del programa y su
        prioridad (mínimo número de copias > copias obsoletas > tamaño máximo
        del conjunto de copias).
    Parámetros:
        - dbname: el nombre de la base de datos de la que se hará una limpieza.
        - db_bkps_list: lista de archivos de copias de seguridad de una base de
        datos concreta.
    '''
        # Almacenar momento del tiempo en segundos a partir del cual una copia
        # de base de datos queda obsoleta
        if self.exp_days == -1:
            x_days_ago = None
        else:
            x_days_ago = time.time() - (60 * 60 * 24 * self.exp_days)
        # Almacenar el máximo tamaño permitido de las copias en Bytes
        max_size = Casting.str_to_max_size(self.max_size)

        if max_size['unit'] == 'MB':
            equivalence = 10 ** 6
        elif max_size['unit'] == 'GB':
            equivalence = 10 ** 9
        elif max_size['unit'] == 'TB':
            equivalence = 10 ** 12
        elif max_size['unit'] == 'PB':
            equivalence = 10 ** 15

        self.max_size = max_size['size'] * equivalence

        # Almacenar número actual de copias que tiene una base de datos
        num_bkps = len(db_bkps_list)
        # Realizar una copia de la lista de copias de seguridad para poderla
        # manipular sin problemas en mitad de un bucle
        db_bkps_lt = db_bkps_list[:]

        unlinked = False

        message = Messenger.BEGINNING_DB_TRIMMER.format(dbname=dbname)
        self.logger.highlight('info', message, 'white')

        for f in db_bkps_list:  # Para cada copia de seguridad de esta BD...
            # Si hay menos copias de las deseadas...
            if num_bkps <= self.min_n_bkps:
                break
            # Almacenar información del archivo
            file_info = os.stat(f)
            # Si está obsoleta...
            if x_days_ago and file_info.st_ctime < x_days_ago:
                self.logger.info(Messenger.DELETING_OBSOLETE_BACKUP % f)
                os.unlink(f)  # Eliminar copia de seguridad
                unlinked = True
                # Reducir la variable que indica el número de copias de esta BD
                # almacenadas en el directorio
                num_bkps -= 1
                db_bkps_lt.remove(f)  # Actualizar lista de copias de seguridad

        tsize = Dir.get_files_tsize(db_bkps_lt)
        tsize_unit = ceil(tsize / equivalence)

        ## DESCOMENTAR ESTA SECCIÓN PARA PROCEDER CON LA ELIMINACIÓN DE COPIAS
        ## SI EL TAMAÑO DEL TOTAL DE ÉSTAS SUPERA EL TAMAÑO MÁXIMO ESPECIFICADO
        #db_bkps_list = db_bkps_lt[:]

        #for f in db_bkps_list:
            ## Si hay menos copias de las deseadas...
            #if num_bkps <= self.min_n_bkps:
                #break
            #if tsize <= self.max_size:
                #break
            #else:
                ## Almacenar información del archivo
                #file_info = os.stat(f)
                #logger.info('Tamaño de copias de seguridad en disco mayor que'
                            #' {} {}: eliminando el archivo {}...' %
                            #(max_size['size'], max_size['unit'], f))
                #os.unlink(f)  # Eliminar copia de seguridad
                #unlinked = True
                ## Reducir la variable que indica el número de copias de esta
                ## BD almacenadas en el directorio
                #num_bkps -= 1
                ## db_bkps_lt.remove(f)
                #tsize -= file_info.st_size  # Actualizar el tamaño total

        if not unlinked:
            self.logger.info(Messenger.NO_DB_BACKUP_DELETED.format(
                dbname=dbname))

        if tsize > self.max_size:
            message = Messenger.DB_BKPS_SIZE_EXCEEDED.format(
                dbname=dbname, tsize_unit=tsize_unit, size=max_size['size'],
                unit=max_size['unit'])
            self.logger.highlight('warning', message, 'yellow', effect='bold')

        self.logger.highlight('info', Messenger.DB_TRIMMER_DONE.format(
            dbname=dbname), 'green')

    def trim_dbs(self, bkps_list, dbs_to_clean):

        # Declarar la expresión regular que detecta si el nombre del archivo
        # de backup se corresponde con una copia generada por el programa
        # dump.py
        if self.prefix:
            regex = r'(' + self.prefix + ')db_(.+)_(\d{8}_\d{6}_.+)\.' \
                    '(?:dump|bz2|gz|zip)$'
        else:
            regex = r'(.*)?db_(.+)_(\d{8}_\d{6}_.+)\.(?:dump|bz2|gz|zip)$'
        regex = re.compile(regex)  # Validar la expresión regular

        # Para cada BD de la que se desea limpiar sus copias...
        for dbname in dbs_to_clean:

            # Inicializar lista de backups de una DB concreta
            db_bkps_list = []

            for file in bkps_list:  # Para cada archivo del directorio...

                filename = os.path.basename(file)

                # Si es un backup (su nombre sigue el patrón de dump.py)...
                if re.match(regex, filename):

                    # Extraer las partes del nombre ([prefix], dbname, date)
                    parts = regex.search(filename).groups()
                    # Almacenar el nombre de la BD a la que pertenece ese
                    # backup
                    fdbname = parts[1]

                    # Si es un backup de una BD de la que se desea realizar una
                    # limpieza de backups...
                    if dbname == fdbname:
                        # Añadir a la lista de backups de esta BD
                        db_bkps_list.append(file)
                    # Si el archivo es un backup pero no se desea eliminar...
                    else:
                        continue
                else:  # Si el archivo no es un backup...
                    continue

            # Eliminar (si procede) las copias de seguridad de esta BD
            self.trim_db(dbname, db_bkps_list)

        Dir.remove_empty_dirs(self.bkp_path)


class TrimmerCluster:

    bkp_path = ''
    prefix = ''
    min_n_bkps = None
    exp_days = None
    max_size = None

    def __init__(self, bkp_path='', prefix='', min_n_bkps=1, exp_days=365,
                 max_size=5000, logger=None):

        if logger:
            self.logger = logger
        else:
            self.logger = Logger()

        if bkp_path and os.path.isdir(bkp_path):
            self.bkp_path = bkp_path
        else:
            self.logger.stop_exe(Messenger.DIR_DOES_NOT_EXIST)

        if prefix is None:
            self.prefix = Default.PREFIX
        else:
            self.prefix = prefix

        if min_n_bkps is None:
            self.min_n_bkps = Default.MIN_N_BKPS
        elif isinstance(min_n_bkps, int):
            self.min_n_bkps = min_n_bkps
        elif Checker.str_is_int(min_n_bkps):
            self.min_n_bkps = Casting.str_to_int(min_n_bkps)
        else:
            self.logger.stop_exe(Messenger.INVALID_MIN_BKPS)

        if exp_days is None:
            self.exp_days = Default.EXP_DAYS
        elif isinstance(exp_days, int) and exp_days >= -1:
            self.exp_days = exp_days
        elif Checker.str_is_valid_exp_days(exp_days):
            self.exp_days = Casting.str_to_int(exp_days)
        else:
            self.logger.stop_exe(Messenger.INVALID_OBS_DAYS)

        if max_size is None:
            self.max_size = Default.MAX_SIZE
        elif Checker.str_is_valid_max_size(max_size):
            self.max_size = max_size
        else:
            self.logger.stop_exe(Messenger.INVALID_MAX_TSIZE)

    def trim_cluster(self, ht_bkps_list):
        '''
    Objetivo:
        - elimina los archivos de copias de seguridad de bases de datos,
        teniendo en cuenta los parámetros de configuración del programa y su
        prioridad (mínimo número de copias > copias obsoletas > tamaño máximo
        del conjunto de copias).
    Parámetros:
        - ht_bkps_list: lista de archivos de copias de seguridad de un host
        concreto.
    '''
        # Almacenar momento del tiempo en segundos a partir del cual una copia
        # de base de datos queda obsoleta
        if self.exp_days == -1:
            x_days_ago = None
        else:
            x_days_ago = time.time() - (60 * 60 * 24 * self.exp_days)
        # Almacenar el máximo tamaño permitido de las copias en Bytes
        max_size = Casting.str_to_max_size(self.max_size)

        if max_size['unit'] == 'MB':
            equivalence = 10 ** 6
        elif max_size['unit'] == 'GB':
            equivalence = 10 ** 9
        elif max_size['unit'] == 'TB':
            equivalence = 10 ** 12
        elif max_size['unit'] == 'PB':
            equivalence = 10 ** 15

        self.max_size = max_size['size'] * equivalence

        # Almacenar número actual de copias que tiene una base de datos
        num_bkps = len(ht_bkps_list)
        # Realizar una copia de la lista de copias de seguridad para poderla
        # manipular sin problemas en mitad de un bucle
        ht_bkps_lt = ht_bkps_list[:]

        unlinked = False

        self.logger.highlight('info', Messenger.BEGINNING_CL_TRIMMER, 'white')

        for f in ht_bkps_list:  # Para cada copia de seguridad del clúster...
            # Si hay menos copias de las deseadas...
            if num_bkps <= self.min_n_bkps:
                break
            # Almacenar información del archivo
            file_info = os.stat(f)
            # Si está obsoleta...
            if x_days_ago and file_info.st_ctime < x_days_ago:
                self.logger.info(Messenger.DELETING_OBSOLETE_BACKUP % f)
                os.unlink(f)  # Eliminar copia de seguridad
                unlinked = True
                # Reducir la variable que indica el número de copias de este
                # clúster almacenadas en el directorio
                num_bkps -= 1
                ht_bkps_lt.remove(f)  # Actualizar lista de copias de seguridad

        tsize = Dir.get_files_tsize(ht_bkps_lt)
        tsize_unit = ceil(tsize / equivalence)

        ## DESCOMENTAR ESTA SECCIÓN PARA PROCEDER CON LA ELIMINACIÓN DE COPIAS
        ## SI EL TAMAÑO DEL TOTAL DE ÉSTAS SUPERA EL TAMAÑO MÁXIMO ESPECIFICADO
        #ht_bkps_list = ht_bkps_lt[:]

        #for f in ht_bkps_list:
            ## Si hay menos copias de las deseadas...
            #if num_bkps <= self.min_n_bkps:
                #break
            #if tsize <= self.max_size:
                #break
            #else:
                ## Almacenar información del archivo
                #file_info = os.stat(f)
                #logger.info('Tamaño de copias de seguridad en disco mayor que'
                            #' {} {}: eliminando el archivo {}...' %
                            #(max_size['size'], max_size['unit'], f))
                #os.unlink(f)  # Eliminar copia de seguridad
                #unlinked = True
                ## Reducir la variable que indica el número de copias de esta
                ## BD almacenadas en el directorio
                #num_bkps -= 1
                ## ht_bkps_lt.remove(f)
                #tsize -= file_info.st_size  # Actualizar el tamaño total

        if not unlinked:
            self.logger.info(Messenger.NO_CL_BACKUP_DELETED)

        if tsize > self.max_size:
            message = Messenger.CL_BKPS_SIZE_EXCEEDED.format(
                tsize_unit=tsize_unit, size=max_size['size'],
                unit=max_size['unit'])
            self.logger.highlight('warning', message, 'yellow', effect='bold')

        self.logger.highlight('info', Messenger.CL_TRIMMER_DONE, 'green')

    def trim_clusters(self, bkps_list):

        # Declarar la expresión regular que detecta si el nombre del archivo
        # de backup se corresponde con una copia generada por el programa
        # dump.py
        if self.prefix:
            regex = r'(' + self.prefix + ')ht_(.+_cluster)_' \
                    '(\d{8}_\d{6}_.+)\.(?:dump|bz2|gz|zip)$'
        else:
            regex = r'(.*)?ht_(.+_cluster)_(\d{8}_\d{6}_.+)\.' \
                    '(?:dump|bz2|gz|zip)$'
        regex = re.compile(regex)  # Validar la expresión regular

        ht_bkps_list = []

        for file in bkps_list:  # Para cada archivo del directorio...

            filename = os.path.basename(file)
            # Si es un backup (su nombre sigue el patrón de dump.py)...
            if re.match(regex, filename):

                # Si es un backup de una BD de la que se desea realizar una
                # limpieza de backups...
                ht_bkps_list.append(file)
                # Si el archivo es un backup pero no se desea eliminar...

            else:  # Si el archivo no es un backup...
                continue

        if ht_bkps_list:
            # Eliminar (si procede) las copias de seguridad de esta BD
            self.trim_cluster(ht_bkps_list)
            Dir.remove_empty_dirs(self.bkp_path)
        else:
            self.logger.highlight('warning', Messenger.NO_BACKUP_IN_DIR,
                                  'yellow', effect='bold')
