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
import os  # Importar la librería os (para trabajar con directorios y archivos)
import re  # Importar la librería glob (para buscar archivos en directorios)
import time  # Importar la librería time (para calcular intervalos de tiempo)
from math import ceil


# ************************* DEFINICIÓN DE FUNCIONES *************************

class Trimmer:

    bkp_path = ''
    prefix = ''
    in_dbs = []
    in_regex = ''
    in_priority = False
    ex_dbs = []
    ex_regex = ''
    min_bkps = None
    obs_days = None
    max_tsize = None
    pg_warnings = True
    connecter = None
    logger = None

    def __init__(self, bkp_path='', prefix='', in_dbs=[], in_regex='',
                 in_priority=False, ex_dbs=[], ex_regex='', min_bkps=1,
                 obs_days=365, max_tsize=5000, pg_warnings=True,
                 connecter=None, logger=None):

        if logger:
            self.logger = logger
        else:
            self.logger = Logger()

        if bkp_path and os.path.isdir(bkp_path):
            self.bkp_path = bkp_path
        else:
            self.logger.stop_exe(Messenger.DIR_DOES_NOT_EXIST)
        self.prefix = prefix
        self.in_dbs = in_dbs
        self.in_regex = in_regex
        self.in_priority = in_priority
        self.ex_dbs = ex_dbs
        self.ex_regex = ex_regex
        self.min_bkps = min_bkps
        self.obs_days = obs_days
        self.max_tsize = max_tsize
        self.pg_warnings = pg_warnings
        if self.pg_warnings is True:
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
        x_days_ago = time.time() - (60 * 60 * 24 * self.obs_days)
        # Almacenar el máximo tamaño permitido de las copias en Bytes
        max_tsize_mb = self.max_tsize
        self.max_tsize *= 10 ** 6
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
            if num_bkps <= self.min_bkps:
                break
            # Almacenar información del archivo
            file_info = os.stat(f)
            if file_info.st_ctime < x_days_ago:  # Si está obsoleta...
                self.logger.info(Messenger.DELETING_OBSOLETE_BACKUP % f)
                os.unlink(f)  # Eliminar copia de seguridad
                unlinked = True
                # Reducir la variable que indica el número de copias de esta BD
                # almacenadas en el directorio
                num_bkps -= 1
                db_bkps_lt.remove(f)  # Actualizar lista de copias de seguridad

        tsize = Dir.get_files_tsize(db_bkps_lt)
        tsize_mb = ceil(tsize / 10 ** 6)

        ## DESCOMENTAR ESTA SECCIÓN PARA PROCEDER CON LA ELIMINACIÓN DE COPIAS
        ## SI EL TAMAÑO DEL TOTAL DE ÉSTAS SUPERA EL TAMAÑO MÁXIMO ESPECIFICADO
        #db_bkps_list = db_bkps_lt[:]

        #for f in db_bkps_list:
            ## Si hay menos copias de las deseadas...
            #if num_bkps <= self.min_bkps:
                #break
            #if tsize <= self.max_tsize:
                #break
            #else:
                ## Almacenar información del archivo
                #file_info = os.stat(f)
                #logger.info('Tamaño de copias de seguridad en disco mayor que'
                            #' {} Bytes: eliminando el archivo {}...' %
                            #(max_tsize_mb, f))
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

        if tsize > self.max_tsize:
            message = Messenger.DB_BKPS_SIZE_EXCEEDED.format(
                dbname=dbname, tsize_mb=tsize_mb, max_tsize_mb=max_tsize_mb)
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
    min_bkps = None
    obs_days = None
    max_tsize = None

    def __init__(self, bkp_path='', prefix='', min_bkps=1, obs_days=365,
                 max_tsize=5000, logger=None):

        if logger:
            self.logger = logger
        else:
            self.logger = Logger()

        if bkp_path and os.path.isdir(bkp_path):
            self.bkp_path = bkp_path
        else:
            self.logger.stop_exe(Messenger.DIR_DOES_NOT_EXIST)

        self.prefix = prefix
        self.min_bkps = min_bkps
        self.obs_days = obs_days
        self.max_tsize = max_tsize

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
        x_days_ago = time.time() - (60 * 60 * 24 * self.obs_days)
        # Almacenar el máximo tamaño permitido de las copias en Bytes
        max_tsize_mb = self.max_tsize
        self.max_tsize *= 10 ** 6
        # Almacenar número actual de copias que tiene una base de datos
        num_bkps = len(ht_bkps_list)
        # Realizar una copia de la lista de copias de seguridad para poderla
        # manipular sin problemas en mitad de un bucle
        ht_bkps_lt = ht_bkps_list[:]

        unlinked = False

        self.logger.highlight('info', Messenger.BEGINNING_CL_TRIMMER, 'white')

        for f in ht_bkps_list:  # Para cada copia de seguridad del clúster...
            # Si hay menos copias de las deseadas...
            if num_bkps <= self.min_bkps:
                break
            # Almacenar información del archivo
            file_info = os.stat(f)
            if file_info.st_ctime < x_days_ago:  # Si está obsoleta...
                self.logger.info(Messenger.DELETING_OBSOLETE_BACKUP % f)
                os.unlink(f)  # Eliminar copia de seguridad
                unlinked = True
                # Reducir la variable que indica el número de copias de este
                # clúster almacenadas en el directorio
                num_bkps -= 1
                ht_bkps_lt.remove(f)  # Actualizar lista de copias de seguridad

        tsize = Dir.get_files_tsize(ht_bkps_lt)
        tsize_mb = ceil(tsize / 10 ** 6)

        ## DESCOMENTAR ESTA SECCIÓN PARA PROCEDER CON LA ELIMINACIÓN DE COPIAS
        ## SI EL TAMAÑO DEL TOTAL DE ÉSTAS SUPERA EL TAMAÑO MÁXIMO ESPECIFICADO
        #ht_bkps_list = ht_bkps_lt[:]

        #for f in ht_bkps_list:
            ## Si hay menos copias de las deseadas...
            #if num_bkps <= self.min_bkps:
                #break
            #if tsize <= self.max_tsize:
                #break
            #else:
                ## Almacenar información del archivo
                #file_info = os.stat(f)
                #logger.info('Tamaño de copias de seguridad en disco mayor que'
                            #' {} Bytes: eliminando el archivo {}...' %
                            #(max_tsize_mb, f))
                #os.unlink(f)  # Eliminar copia de seguridad
                #unlinked = True
                ## Reducir la variable que indica el número de copias de esta
                ## BD almacenadas en el directorio
                #num_bkps -= 1
                ## ht_bkps_lt.remove(f)
                #tsize -= file_info.st_size  # Actualizar el tamaño total

        if not unlinked:
            self.logger.info(Messenger.NO_CL_BACKUP_DELETED)

        if tsize > self.max_tsize:
            message = Messenger.CL_BKPS_SIZE_EXCEEDED.format(
                tsize_mb=tsize_mb, max_tsize_mb=max_tsize_mb)
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
