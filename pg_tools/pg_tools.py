#!/usr/bin/env python3
# -*- encoding: utf-8 -*-


# ************************* CARGA DE LIBRERÍAS *************************

# Importar la función get_date de la librería personalizada
# date_tools.date_tools (para obtener la fecha y hora actuales de la zona en
# el formato deseado)
from date_tools.date_tools import DateTools
# Importar la funciones create_logger de la librería personalizada
# logger.logger (para utilizar un logger que muestre información al usuario)
from logger.logger import Logger
# Importar las funciones create_dir, default_bkps_path, default_cfg_path de la
# librería personalizada dir_tools.dir_tools (para crear directorios de forma
# automática y localizar archivos creados por defecto)
from dir_tools.dir_tools import Dir
# Importar la librería subprocess (para realizar consultas a las bases de datos
# de PostgreSQL)
import subprocess
import os  # Importar la librería os (para trabajar con directorios y archivos)
import re  # Importar la librería glob (para buscar archivos en directorios)
import time  # Importar la librería time (para calcular intervalos de tiempo)
from math import ceil


# ************************* DEFINICIÓN DE FUNCIONES *************************

class PgTools:

    def __init__(self):
        pass

    @staticmethod
    def vacuum_db(conn, dbname, logger=None):
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
        if not logger:
            logger = Logger()
        success = True
        # Almacenar la instrucción a realizar en consola
        command = 'vacuumdb {} -U {} -h {} -p {}'.format(
            dbname, conn.user, conn.server, conn.port)
        try:  # Probar que la copia se realiza correctamente
            # Ejecutar la instrucción de la copia de seguridad en consola
            result = subprocess.call(command, shell=True)
            if result != 0:  # Si el comando no de resultados en consola...
                raise Exception()  # Lanzar excepción
        except Exception as e:
            logger.debug('Error en la función "vacuum_db": {}.'.format(str(e)))
            success = False
        return success

    @staticmethod
    def vacuum_dbs(conn, dbs_all=[], in_forbidden=False, logger=None):
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
        if not logger:
            logger = Logger()
        message = 'Procesando bases de datos a limpiar...'
        logger.set_view('info', message, 'white')
        # Para cada base de datos de la que se quiere backup...
        for db in dbs_all:
            dbname = db['name']  # Almacenar nombre de la BD por claridad
            mod_allow_conn = False  # En principio no se modifica datallowconn
            # Si se exigen copias de bases de datos sin permisos de conexión...
            if not db['allow_connection'] and in_forbidden:
                conn.allow_db_conn(dbname)  # Permitir conexiones
                mod_allow_conn = True  # Marcar que se modifica datallowconn
                logger.info('Habilitando conexiones a la base de datos...')
            logger.info('Iniciando limpieza de la base de datos '
                        '"{}"...'.format(dbname))
            # Realizar copia de seguridad de la base de datos
            success = PgTools.vacuum_db(conn, dbname, logger)
            if mod_allow_conn:  # Si se modificó datallowconn...
                # Deshabilitar nuevamente las conexiones y dejarlo como estaba
                conn.disallow_db_conn(dbname)
                logger.info('Deshabilitando conexiones a la base de datos...')
            if success:
                message = 'Limpieza de la base de datos "{}" ' \
                          'completada.'.format(dbname)
                logger.set_view('info', message, 'green')
            else:
                message = 'La limpieza de la base de datos "{}" no se pudo ' \
                          'completar.'.format(dbname)
                logger.set_view('warning', message, 'yellow', effect='bold')
        message = 'Limpieza de bases de datos finalizada.'
        logger.set_view('info', message, 'green')

    @staticmethod
    def dump_db(conn, bkps_dir, dbname, bkp_type, prefix='', logger=None):
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
        if not logger:
            logger = Logger()
        success = True
        # Obtener fecha y hora actuales de la zona
        init_ts = DateTools.get_date()
        # Obtener el año de la fecha almacenada
        year = str(DateTools.get_year(init_ts))
        # Obtener el mes de la fecha almacenada
        month = str(DateTools.get_month(init_ts))
        bkp_dir = bkps_dir + year + '/' + month + '/'
        Dir.create_dir(bkp_dir, logger)
        # Establecer nombre del archivo que contiene la copia de seguridad
        file_name = prefix + 'db_' + dbname + '_' + init_ts + bkp_type
        # Almacenar la instrucción a realizar en consola
        if bkp_type == '.gz':  # Comprimir con gzip
            command = 'pg_dump {} -Fp -U {} -h {} -p {} | gzip > {}'.format(
                dbname, conn.user, conn.server, conn.port, bkp_dir + file_name)
        elif bkp_type == '.bz2':  # Comprimir con bzip2
            command = 'pg_dump {} -Fp -U {} -h {} -p {} | bzip2 > {}'.format(
                dbname, conn.user, conn.server, conn.port, bkp_dir + file_name)
        elif bkp_type == '.zip':  # Comprimir con zip
            command = 'pg_dump {} -Fp -U {} -h {} -p {} | zip > {}'.format(
                dbname, conn.user, conn.server, conn.port, bkp_dir + file_name)
        else:  # No comprimir la copia
            command = 'pg_dump {} -Fp -U {} -h {} -p {} > {}'.format(
                dbname, conn.user, conn.server, conn.port, bkp_dir + file_name)
        try:  # Probar que la copia se realiza correctamente
            # Ejecutar la instrucción de la copia de seguridad en consola
            result = subprocess.call(command, shell=True)
            if result != 0:  # Si el comando no de resultados en consola...
                raise Exception()  # Lanzar excepción
        except Exception as e:
            logger.debug('Error en la función "dump_db": {}.'.format(str(e)))
            success = False
        return success

    @staticmethod
    def dump_dbs(conn, bkp_dir, dbs_all, bkp_type='.dump', in_forbidden=False,
                 prefix='', server_alias='localhost', vacuum=True,
                 logger=None):
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
        if not logger:
            logger = Logger()
        message = 'Comprobando directorio de destino de las copias... '
        bkps_dir = bkp_dir + server_alias + '/dump/'
        Dir.create_dir(bkps_dir, logger)
        message += 'Directorio de destino existente.'
        logger.set_view('info', message, 'white')
        message = 'Procesando copias de seguridad a realizar...'
        logger.set_view('info', message, 'white')
        # Para cada base de datos de la que se quiere backup...
        for db in dbs_all:
            dbname = db['name']  # Almacenar nombre de la BD por claridad
            mod_allow_conn = False  # En principio no se modifica datallowconn
            # Si se exigen copias de bases de datos sin permisos de conexión...
            if not db['allow_connection'] and in_forbidden:
                conn.allow_db_conn(dbname)  # Permitir conexiones
                mod_allow_conn = True  # Marcar que se modifica datallowconn
                logger.info('Habilitando conexiones a la base de datos...')
            if vacuum:
                logger.info('Iniciando limpieza previa de la base de datos '
                            '"{}"...'.format(dbname))
                success = PgTools.vacuum_db(conn, dbname, logger)
                if success:
                    logger.info('Limpieza previa de la base de datos "{}" '
                                'completada.'.format(dbname))
                else:
                    logger.warning('La limpieza previa de la base de datos '
                                   '"{}" no se pudo completar.'.format(dbname))
            logger.info('Iniciando copia de seguridad de la base de datos '
                        '"{}"...'.format(dbname))
            # Realizar copia de seguridad de la base de datos
            success = PgTools.dump_db(conn, bkps_dir, dbname, bkp_type, prefix,
                                      logger)
            if mod_allow_conn:  # Si se modificó datallowconn...
                # Deshabilitar nuevamente las conexiones y dejarlo como estaba
                conn.disallow_db_conn(dbname)
                logger.info('Deshabilitando conexiones a la base de datos...')
            if success:
                message = 'Copia de seguridad de la base de datos "{}" ' \
                          'completada.'.format(dbname)
                logger.set_view('info', message, 'green')
            else:
                message = 'La copia de seguridad de la base de datos "{}" ' \
                          'no se pudo completar.'.format(dbname)
                logger.set_view('warning', message, 'yellow', effect='bold')
        message = 'Copias de seguridad finalizadas.'
        logger.set_view('info', message, 'green')

    @staticmethod
    def dump_all(conn, bkps_dir, bkp_type='.dump', prefix='', logger=None):
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
        if not logger:
            logger = Logger()
        success = True
        # Obtener fecha y hora actuales de la zona
        init_ts = DateTools.get_date()
        # Obtener el año de la fecha almacenada
        year = str(DateTools.get_year(init_ts))
        # Obtener el mes de la fecha almacenada
        month = str(DateTools.get_month(init_ts))
        bkp_dir = bkps_dir + year + '/' + month + '/'
        Dir.create_dir(bkp_dir, logger)
        # Establecer nombre del archivo que contiene la copia de seguridad
        file_name = prefix + 'ht_' + conn.server + '_cluster_' + init_ts + \
            bkp_type
        # Almacenar la instrucción a realizar en consola
        if bkp_type == '.gz':  # Comprimir con gzip
            command = 'pg_dumpall -U {} -h {} -p {} | gzip > {}'.format(
                conn.user, conn.server, conn.port, bkp_dir + file_name)
        elif bkp_type == '.bz2':  # Comprimir con bzip2
            command = 'pg_dumpall -U {} -h {} -p {} | bzip2 > {}'.format(
                conn.user, conn.server, conn.port, bkp_dir + file_name)
        elif bkp_type == '.zip':  # Comprimir con zip
            command = 'pg_dumpall -U {} -h {} -p {} | zip > {}'.format(
                conn.user, conn.server, conn.port, bkp_dir + file_name)
        else:  # No comprimir la copia
            command = 'pg_dumpall -U {} -h {} -p {} > {}'.format(
                conn.user, conn.server, conn.port, bkp_dir + file_name)
        try:  # Probar que la copia se realiza correctamente
            # Ejecutar la instrucción de la copia de seguridad en consola
            result = subprocess.call(command, shell=True)
            if result != 0:  # Si el comando no de resultados en consola...
                raise Exception()  # Lanzar excepción
        except Exception as e:
            logger.debug('Error en la función "dump_cluster": {}.'.format(
                str(e)))
            success = False
        return success

    @staticmethod
    def dump_cluster(conn, bkps_dir, bkp_type='.dump', prefix='',
                     server_alias='localhost', logger=None):
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
        if not logger:
            logger = Logger()
        message = 'Comprobando directorio de destino de las copias... '
        bkp_dir = bkps_dir + server_alias + '/dumpall/'
        Dir.create_dir(bkps_dir, logger)
        message += 'Directorio de destino existente.'
        logger.set_view('info', message, 'white')

        message = 'Iniciando copia de seguridad de del clúster de bases de ' \
                  'datos...'
        logger.set_view('info', message, 'white')

        success = PgTools.dump_all(conn, bkp_dir, bkp_type, prefix, logger)
        if success:
            message = 'Copia de seguridad del clúster de bases de datos ' \
                      'completada.'
            logger.set_view('info', message, 'green')
        else:
            message = 'La copia de seguridad del clúster de bases de datos ' \
                      'no se pudo completar.'
            logger.set_view('warning', message, 'yellow', effect='bold')

    @staticmethod
    def clean_db(path, dbname, db_bkps_list=[], max_tsize=5000, min_bkps=1,
                 obs_days=1, logger=None):
        '''
    Objetivo:
        - elimina los archivos de copias de seguridad de bases de datos,
        teniendo en cuenta los parámetros de configuración del programa y su
        prioridad (mínimo número de copias > copias obsoletas > tamaño máximo
        del conjunto de copias).
    Parámetros:
        - logger: el logger que se empleará para mostrar y registrar el
        mensaje.
        - dbname: el nombre de la base de datos de la que se hará una limpieza.
        - db_bkps_list: lista de archivos de copias de seguridad de una base de
        datos concreta.
        - path: la ruta de la carpeta donde están almacenados los backups de la
        BD.
        - min_bkps: número mínimo de archivos de copias de seguridad que se
        deben conservar de una base de datos concreta.
        - obs_days: número de días que deben haber pasado desde la última
        modificación para considerar obsoleto el archivo de una base de datos.
        - max_tsize: tamaño máximo en Bytes que debe tener el conjunto de
        archivos de copias de seguridad de una base de datos concreta.
    '''
        if not logger:
            logger = Logger()
        # Almacenar momento del tiempo en segundos a partir del cual una copia
        # de base de datos queda obsoleta
        x_days_ago = time.time() - (60 * 60 * 24 * obs_days)
        # Almacenar el máximo tamaño permitido de las copias en Bytes
        max_tsize_mb = max_tsize
        max_tsize *= 10 ** 6
        # Almacenar número actual de copias que tiene una base de datos
        num_bkps = len(db_bkps_list)
        # Realizar una copia de la lista de copias de seguridad para poderla
        # manipular sin problemas en mitad de un bucle
        db_bkps_lt = db_bkps_list[:]

        unlinked = False

        message = 'Iniciando limpieza de copias de seguridad de la base ' \
                  'de datos "{}"...'.format(dbname)
        logger.set_view('info', message, 'white')

        for f in db_bkps_list:  # Para cada copia de seguridad de esta BD...
            if num_bkps <= min_bkps:  # Si hay menos copias de las deseadas...
                break
            file_info = os.stat(path + f)  # Almacenar información del archivo
            if file_info.st_ctime < x_days_ago:  # Si está obsoleta...
                logger.info('Copia de seguridad obsoleta: eliminando el '
                            'archivo %s...' % f)
                os.unlink(path + f)  # Eliminar copia de seguridad
                unlinked = True
                # Reducir la variable que indica el número de copias de esta BD
                # almacenadas en el directorio
                num_bkps -= 1
                db_bkps_lt.remove(f)  # Actualizar lista de copias de seguridad

        tsize = Dir.get_files_tsize(path, db_bkps_lt)
        tsize_mb = ceil(tsize / 10 ** 6)

        ## DESCOMENTAR ESTA SECCIÓN PARA PROCEDER CON LA ELIMINACIÓN DE COPIAS
        ## SI EL TAMAÑO DEL TOTAL DE ÉSTAS SUPERA EL TAMAÑO MÁXIMO ESPECIFICADO
        #db_bkps_list = db_bkps_lt[:]

        #for f in db_bkps_list:
            #if num_bkps <= min_bkps:  # Si hay menos copias de las deseadas...
                #break
            #if tsize <= max_tsize:
                #break
            #else:
                ## Almacenar información del archivo
                #file_info = os.stat(path + f)
                #logger.info('Tamaño de copias de seguridad en disco mayor que'
                            #' {} Bytes: eliminando el archivo {}...' %
                            #(max_tsize_mb, path + f))
                #os.unlink(path + f)  # Eliminar copia de seguridad
                #unlinked = True
                ## Reducir la variable que indica el número de copias de esta
                ## BD almacenadas en el directorio
                #num_bkps -= 1
                ## db_bkps_lt.remove(f)
                #tsize -= file_info.st_size  # Actualizar el tamaño total

        if not unlinked:
            logger.info('No se ha eliminado ninguna copia de la base de '
                        'datos "{}".'.format(dbname))

        if tsize > max_tsize:
            message = 'El tamaño del total de copias de seguridad en disco ' \
                      'de la base de datos {} es de {} MB, que es mayor que ' \
                      'el máximo especificado ({} MB).'.format(
                          dbname, tsize_mb, max_tsize_mb)
            logger.set_view('warning', message, 'yellow', effect='bold')

        message = 'Limpieza de copias de seguridad de la base de datos ' \
                  '"{}" completada.'.format(dbname)
        logger.set_view('info', message, 'green')

    @staticmethod
    def clean_dbs(path, bkps_list=[], dbs_to_clean=[], max_tsize=5000,
                  min_bkps=1, obs_days=1, prefix='', logger=None):
        if not logger:
            logger = Logger()
        # Declarar la expresión regular que detecta si el nombre del archivo
        # de backup se corresponde con una copia generada por el programa
        # dump.py
        if prefix:
            regex = r'(' + prefix + ')db_(.+)_(\d{8}_\d{6}_.+)\.' \
                    '(?:dump|bz2|gz|zip)$'
        else:
            regex = r'(.*)?db_(.+)_(\d{8}_\d{6}_.+)\.(?:dump|bz2|gz|zip)$'
        regex = re.compile(regex)  # Validar la expresión regular

        # Para cada BD de la que se desea limpiar sus copias...
        for dbname in dbs_to_clean:

            # Inicializar lista de backups de una DB concreta
            db_bkps_list = []

            for f in bkps_list:  # Para cada archivo del directorio...

                # Si es un backup (su nombre sigue el patrón de dump.py)...
                if re.match(regex, f):

                    # Extraer las partes del nombre ([prefix], dbname, date)
                    parts = regex.search(f).groups()
                    # Almacenar el nombre de la BD a la que pertenece ese
                    # backup
                    fdbname = parts[1]

                    # Si es un backup de una BD de la que se desea realizar una
                    # limpieza de backups...
                    if dbname == fdbname:
                        # Añadir a la lista de backups de esta BD
                        db_bkps_list.append(f)
                    # Si el archivo es un backup pero no se desea eliminar...
                    else:
                        continue
                else:  # Si el archivo no es un backup...
                    continue

            # Eliminar (si procede) las copias de seguridad de esta BD
            PgTools.clean_db(path, dbname, db_bkps_list, max_tsize, min_bkps,
                             obs_days, logger)

    @staticmethod
    def del_cluster_bkps(path, ht_bkps_list=[], max_tsize=10000, min_bkps=1,
                         obs_days=1, logger=None):
        '''
    Objetivo:
        - elimina los archivos de copias de seguridad de bases de datos,
        teniendo en cuenta los parámetros de configuración del programa y su
        prioridad (mínimo número de copias > copias obsoletas > tamaño máximo
        del conjunto de copias).
    Parámetros:
        - logger: el logger que se empleará para mostrar y registrar el
        mensaje.
        - dbname: el nombre de la base de datos de la que se hará una limpieza.
        - db_bkps_list: lista de archivos de copias de seguridad de una base de
        datos concreta.
        - path: la ruta de la carpeta donde están almacenados los backups de la
        BD.
        - min_bkps: número mínimo de archivos de copias de seguridad que se
        deben conservar de una base de datos concreta.
        - obs_days: número de días que deben haber pasado desde la última
        modificación para considerar obsoleto el archivo de una base de datos.
        - max_tsize: tamaño máximo en Bytes que debe tener el conjunto de
        archivos de copias de seguridad de una base de datos concreta.
    '''
        if not logger:
            logger = Logger()
        # Almacenar momento del tiempo en segundos a partir del cual una copia
        # de base de datos queda obsoleta
        x_days_ago = time.time() - (60 * 60 * 24 * obs_days)
        # Almacenar el máximo tamaño permitido de las copias en Bytes
        max_tsize_mb = max_tsize
        max_tsize *= 10 ** 6
        # Almacenar número actual de copias que tiene una base de datos
        num_bkps = len(ht_bkps_list)
        # Realizar una copia de la lista de copias de seguridad para poderla
        # manipular sin problemas en mitad de un bucle
        ht_bkps_lt = ht_bkps_list[:]

        unlinked = False

        message = 'Iniciando limpieza de copias de seguridad del clúster de ' \
                  'PostgreSQL del servidor.'
        logger.set_view('info', message, 'white')

        for f in ht_bkps_list:  # Para cada copia de seguridad del clúster...
            if num_bkps <= min_bkps:  # Si hay menos copias de las deseadas...
                break
            file_info = os.stat(path + f)  # Almacenar información del archivo
            if file_info.st_ctime < x_days_ago:  # Si está obsoleta...
                logger.info('Copia de seguridad obsoleta: eliminando el '
                            'archivo %s...' % f)
                os.unlink(path + f)  # Eliminar copia de seguridad
                unlinked = True
                # Reducir la variable que indica el número de copias de este
                # clúster almacenadas en el directorio
                num_bkps -= 1
                ht_bkps_lt.remove(f)  # Actualizar lista de copias de seguridad

        tsize = Dir.get_files_tsize(path, ht_bkps_lt)
        tsize_mb = ceil(tsize / 10 ** 6)

        ## DESCOMENTAR ESTA SECCIÓN PARA PROCEDER CON LA ELIMINACIÓN DE COPIAS
        ## SI EL TAMAÑO DEL TOTAL DE ÉSTAS SUPERA EL TAMAÑO MÁXIMO ESPECIFICADO
        #ht_bkps_list = ht_bkps_lt[:]

        #for f in ht_bkps_list:
            #if num_bkps <= min_bkps:  # Si hay menos copias de las deseadas...
                #break
            #if tsize <= max_tsize:
                #break
            #else:
                ## Almacenar información del archivo
                #file_info = os.stat(path + f)
                #logger.info('Tamaño de copias de seguridad en disco mayor que'
                            #' {} Bytes: eliminando el archivo {}...' %
                            #(max_tsize_mb, path + f))
                #os.unlink(path + f)  # Eliminar copia de seguridad
                #unlinked = True
                ## Reducir la variable que indica el número de copias de esta
                ## BD almacenadas en el directorio
                #num_bkps -= 1
                ## ht_bkps_lt.remove(f)
                #tsize -= file_info.st_size  # Actualizar el tamaño total

        if not unlinked:
            logger.info('No se ha eliminado ninguna copia del clúster del '
                        'servidor.')

        if tsize > max_tsize:
            message = 'El tamaño del total de copias de seguridad en disco ' \
                      'del clúster es de {} MB, que es mayor que el máximo ' \
                      'especificado ({} MB).'.format(tsize_mb, max_tsize_mb)
            logger.set_view('warning', message, 'yellow', effect='bold')

        message = 'Limpieza de copias de seguridad del clúster del servidor ' \
                  'completada.'
        logger.set_view('info', message, 'green')

    @staticmethod
    def clean_cluster(path, bkps_list=[], max_tsize=10000, min_bkps=1,
                      obs_days=1, prefix='', logger=None):
        if not logger:
            logger = Logger()
        # Declarar la expresión regular que detecta si el nombre del archivo
        # de backup se corresponde con una copia generada por el programa
        # dump.py
        if prefix:
            regex = r'(' + prefix + ')ht_(.+_cluster)_(\d{8}_\d{6}_.+)\.' \
                    '(?:dump|bz2|gz|zip)$'
        else:
            regex = r'(.*)?ht_(.+_cluster)_(\d{8}_\d{6}_.+)\.' \
                    '(?:dump|bz2|gz|zip)$'
        regex = re.compile(regex)  # Validar la expresión regular

        ht_bkps_list = []

        for f in bkps_list:  # Para cada archivo del directorio...

            # Si es un backup (su nombre sigue el patrón de dump.py)...
            if re.match(regex, f):

                # Si es un backup de una BD de la que se desea realizar una
                # limpieza de backups...
                ht_bkps_list.append(f)
                # Si el archivo es un backup pero no se desea eliminar...

            else:  # Si el archivo no es un backup...
                continue

        if ht_bkps_list:
            # Eliminar (si procede) las copias de seguridad de esta BD
            PgTools.del_cluster_bkps(path, ht_bkps_list, max_tsize, min_bkps,
                                     obs_days, logger)
        else:
            message = 'El directorio especificado en el archivo de ' \
                      'configuración no contiene copias de seguridad cuyos ' \
                      'nombres sigan el patrón del programa.'
            logger.set_view('warning', message, 'yellow', effect='bold')
