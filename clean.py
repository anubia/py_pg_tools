#!/usr/bin/env python3
# -*- encoding: utf-8 -*-


# ************************* CARGA DE LIBRERÍAS *************************

# Importar la funciones create_logger y logger_fatal de la librería
# personalizada logger.logger (para utilizar un logger que proporcione
# información al usuario)
from logger.logger import create_logger, logger_fatal, logger_colored
# Importar la funciones pg_connect y pg_disconnect de la librería
# personalizada pg_connection.pg_connection (para conectarse y desconectarse a
# PostgreSQL y poder ejecutar consultas)
from pg_connection.pg_connection import pg_connect, pg_disconnect
from db_selector.db_selector import get_dbnames_to_bkp
# Importar las funciones create_dir, default_bkps_path, default_cfg_path de la
# librería personalizada dir_tools.dir_tools (para crear directorios de forma
# automática y localizar archivos creados por defecto)
from dir_tools.dir_tools import default_cfg_path
from pg_tools.pg_tools import is_pg_superuser, get_cursor_dbs
from config.config_tools import load_cleaner
from math import ceil
import os  # Importar la librería os (para trabajar con directorios y archivos)
import re  # Importar la librería glob (para buscar archivos en directorios)
import time  # Importar la librería time (para calcular intervalos de tiempo)
# Importar la librería argparse (para trabajar con el vector argv fácilmente)
import argparse


# ************************* DEFINICIÓN DE FUNCIONES *************************

def union(list1, list2):
    '''
Objetivo:
    - devuelve una lista que consiste en la unión de dos listas.
Parámetros:
    - list1: una de las listas a unir.
    - list2: la otra lista a unir.
Devolución:
    - la lista resultado de la unión de las otras dos.
'''
    return list(set(list1) | set(list2))


def sorted_flist(path):
    '''
Objetivo:
    - genera una lista en la que se ordena descendentemente por fecha de
    modificación los archivos que se encuentran en el directorio o ruta
    especificados.
Parámetros:
    - path: la ruta o directorio donde se encuentran los archivos que se desean
    ordenar.
Devolución:
    - una lista con los archivos ordenados.
'''
    mtime = lambda f: os.stat(os.path.join(path, f)).st_mtime
    return list(sorted(os.listdir(path), key=mtime))


def get_dbs_bkped(bkps_list):
    '''
Objetivo:
    - extrae los nombres de las bases de datos que tienen un backup de la lista
    con los archivos de backups que recibe. Genera una lista con el resultado
    obtenido.
Parámetros:
    - bkps_list: una lista de archivos de backups.
Devolución:
    - una lista con los nombres de las bases de datos que tienen un backup en
    la lista que se pasó por parámetro.
'''
    bkped_dbs = []  # De momento no hay ninguna base de datos con backup
    # Declarar la expresión regular que detecta si el nombre del archivo
    # de backup se corresponde con una copia generada por el programa dump.py
    regex = r'(.*)?db_(.+)_(\d{8}_\d{6}_.+)\.(?:dump|bz2|gz|zip)$'
    regex = re.compile(regex)  # Validar la expresión regular
    for f in bkps_list:  # Para cada archivo de la lista...
        if re.match(regex, f):  # Si su nombre sigue el patrón de dump.py...
            # Extraer las partes del nombre ([prefix], dbname, date)
            parts = regex.search(f).groups()
            # Si el nombre de la BD no está en la lista de BDs con backup,
            # se añade (si está, no se añade, para evitar nombres repetidos)
            if parts[1] not in bkped_dbs:
                bkped_dbs.append(parts[1])  # Añadir nombre de BD a la lista
        else:  # Si el archivo no es un backup o no cumple el patrón dump.py...
            continue  # Se ignora...
    return bkped_dbs  # Devolver la lista de BDs que tienen copia


def bkp_warning(logger, pg_dbs, bkped_dbs):
    '''
Objetivo:
    - advertir de las bases de datos que actualmente existen en PostgreSQL y
    que no tienen una copia de seguridad.
Parámetros:
    - logger: el logger que se empleará para mostrar y registrar el mensaje.
    - pg_dbs: las bases de datos que hay en PostgreSQL.
    - bkped_dbs: las bases de datos que tienen una copia de seguridad.
'''
    message = 'Las siguientes bases de datos almacenadas en PostgreSQL no ' \
              'tienen copias de seguridad: '
    for dbname in pg_dbs:  # Para cada BD en PostgreSQL...
        if dbname not in bkped_dbs:  # Si no está entre las BDs con copia...
            if dbname is pg_dbs[-1]:
                message += '"{}".'.format(dbname)
                break
            message += '"{}", '.format(dbname)
    logger_colored(logger, 'warning', message, 'yellow', effect='bold')


def get_files_tsize(files_list, path):
    '''
Objetivo:
    - devuelve el tamaño total en disco del conjunto de archivos que componen
    la lista obtenida por parámetro.
Parámetros:
    - files_list: la lista con el conjunto de archivos del que se desea
    calcular el tamaño en disco.
Devolución:
    - el tamaño en disco del conjuntos de archivos que componen la lista.
'''
    tsize = 0  # Inicializar tamaño a 0 bytes
    for f in files_list:  # Para cada archivo de la lista...
        file_info = os.stat(path + f)  # Almacenar información del archivo
        # Añadir el tamaño del archivo al tamaño total
        tsize += file_info.st_size
    return tsize  # Devolver tamaño total de la lista de archivos


def del_db_bkps(logger, dbname, db_bkps_list, path, min_bkps, obs_days,
                max_tsize):
    '''
Objetivo:
    - elimina los archivos de copias de seguridad de bases de datos, teniendo
    en cuenta los parámetros de configuración del programa y su prioridad
    (mínimo número de copias > copias obsoletas > tamaño máximo del conjunto
    de copias).
Parámetros:
    - logger: el logger que se empleará para mostrar y registrar el mensaje.
    - dbname: el nombre de la base de datos de la que se hará una limpieza.
    - db_bkps_list: lista de archivos de copias de seguridad de una base de
    datos concreta.
    - path: la ruta de la carpeta donde están almacenados los backups de la BD.
    - min_bkps: número mínimo de archivos de copias de seguridad que se deben
    conservar de una base de datos concreta.
    - obs_days: número de días que deben haber pasado desde la última
    modificación para considerar obsoleto el archivo de una base de datos.
    - max_tsize: tamaño máximo en Bytes que debe tener el conjunto de archivos
    de copias de seguridad de una base de datos concreta.
'''
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
    logger_colored(logger, 'info', message, 'white')

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

    tsize = get_files_tsize(db_bkps_lt, path)
    tsize_mb = ceil(tsize / 10 ** 6)

    ## DESCOMENTAR ESTA SECCIÓN PARA PROCEDER CON LA ELIMINACIÓN DE COPIAS SI
    ## EL TAMAÑO DEL TOTAL DE ÉSTAS SUPERA EL TAMAÑO MÁXIMO ESPECIFICADO.
    #db_bkps_list = db_bkps_lt[:]

    #for f in db_bkps_list:
        #if num_bkps <= min_bkps:  # Si hay menos copias de las deseadas...
            #break
        #if tsize <= max_tsize:
            #break
        #else:
            ## Almacenar información del archivo
            #file_info = os.stat(path + f)
            #logger.info('Tamaño de copias de seguridad en disco mayor que '
                        #'{} Bytes: eliminando el archivo {}...' %
                        #(max_tsize_mb, path + f))
            #os.unlink(path + f)  # Eliminar copia de seguridad
            #unlinked = True
            ## Reducir la variable que indica el número de copias de esta BD
            ## almacenadas en el directorio
            #num_bkps -= 1
            ## db_bkps_lt.remove(f)
            #tsize -= file_info.st_size  # Actualizar el tamaño total

    if not unlinked:
        logger.info('No se ha eliminado ninguna copia de la base de '
                    'datos "{}".'.format(dbname))

    if tsize > max_tsize:
        message = 'El tamaño del total de copias de seguridad en disco de ' \
                  'la base de datos {} es de {} MB, que es mayor que el ' \
                  'máximo especificado ({} MB).'.format(
                      dbname, tsize_mb, max_tsize_mb)
        logger_colored(logger, 'warning', message, 'yellow', effect='bold')

    message = 'Limpieza de copias de seguridad de la base de datos ' \
              '"{}" completada.'.format(dbname)
    logger_colored(logger, 'info', message, 'green')


def make_clean(logger, bkps_list, dbs_to_clean, pg_dbs, path, prefix, min_bkps,
               obs_days, max_tsize):
    # Declarar la expresión regular que detecta si el nombre del archivo
    # de backup se corresponde con una copia generada por el programa dump.py
    if prefix:
        regex = r'(' + prefix + ')db_(.+)_(\d{8}_\d{6}_.+)\.' \
                '(?:dump|bz2|gz|zip)$'
    else:
        regex = r'(.*)?db_(.+)_(\d{8}_\d{6}_.+)\.(?:dump|bz2|gz|zip)$'
    regex = re.compile(regex)  # Validar la expresión regular

    # Inicializar lista de BDs que no están en PostgreSQL pero que tienen
    # backups en disco
    notpg_bkp_list = []
    # Para cada BD de la que se desea limpiar sus copias...
    for dbname in dbs_to_clean:
        db_bkps_list = []  # Inicializar lista de backups de una DB concreta

        for f in bkps_list:  # Para cada archivo del directorio...

            # Si es un backup (su nombre sigue el patrón de dump.py)...
            if re.match(regex, f):

                # Extraer las partes del nombre ([prefix], dbname, date)
                parts = regex.search(f).groups()
                # Almacenar el nombre de la BD a la que pertenece ese backup
                fdbname = parts[1]

                # Si esa BD no está en PostgreSQL y no se había previamente
                # añadido a la lista de backups sin BD en PostgreSQL...
                if fdbname not in pg_dbs and fdbname not in notpg_bkp_list:
                    # Añadir BD a la lista BDs ausentes en PostgreSQL pero con
                    # backups en disco
                    notpg_bkp_list.append(fdbname)

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
        del_db_bkps(logger, dbname, db_bkps_list, path, min_bkps, obs_days,
                    max_tsize)

    if notpg_bkp_list:
        message = 'Las siguientes bases de datos tienen copias de ' \
                  'seguridad pero no existen en PostgreSQL: '
        for dbname in notpg_bkp_list:
            if dbname is notpg_bkp_list[-1]:
                message += '"{}".'.format(dbname)
                break
            message += '"{}", '.format(dbname)
        logger_colored(logger, 'warning', message, 'yellow', effect='bold')


# ************************* PROGRAMA PRINCIPAL *************************

if __name__ == "__main__":

    # Crear un logger para los mensajes de información
    logger = create_logger()

    # Asignar ruta por defecto al archivo de configuración
    cfg_path = default_cfg_path('cleaner/cleaner.cfg')
    # Crear parseador para obtener fácilmente los parámetros enviados desde
    # consola
    parser = argparse.ArgumentParser()
    # Crear un parámetro personalizado para enviar al programa desde consola
    parser.add_argument('-c', '--config',
                        help='load a configuration file (.cfg)',
                        default=cfg_path)
    args = parser.parse_args()  # Guardar los parámetros creados

    # Cargar variables del archivo .cfg
    bkp_vars = load_cleaner(logger, args.config)

    # Asegurar la existencia de un directorio donde almacenar las copias de
    # seguridad de PostgreSQL
    bkps_dir = bkp_vars['bkp_path']
    if not os.path.isdir(bkps_dir):
        logger_fatal(logger, 'El directorio especificado en el archivo de '
                             'configuración no existe.')

    # Iniciar conexión a la base de datos "template1" con el usuario
    # especificado
    conn = pg_connect(logger, bkp_vars['server'], bkp_vars['user'],
                      bkp_vars['pwd'], bkp_vars['port'])
    # Inicializar un cursor para realizar operaciones en la base de datos
    cursor = conn.cursor()

    # Comprobar si el usuario actualmente conectado es superusuario de
    # PostgreSQL
    pg_superuser = is_pg_superuser(cursor)
    if not pg_superuser:  # Si no es superusuario de PostgreSQL...
        # Sólo puede manipular las BDs de las que es propietario
        message = 'El usuario especificado para la conexión a PostgreSQL ' \
                  'no tiene rol de superusuario: sólo podrá actuar sobre ' \
                  'las bases de datos de las cuales es propietario.'
        logger_colored(logger, 'warning', message, 'yellow', effect='bold')

    # Ejecutar consulta de PostgreSQL y obtener nombres de todas las bases de
    # datos almacenadas, sus permisos de conexión y sus propietarios
    cursor = get_cursor_dbs(cursor, False, bkp_vars['user'])

    pg_dbs = []
    for record in cursor:  # Para cada registro de la consulta...
        pg_dbs.append(record[0])

    bkps_list = sorted_flist(bkps_dir)

    if bkps_list:

        bkped_dbs = get_dbs_bkped(bkps_list)

        if bkped_dbs:

            dbs_all = union(pg_dbs, bkped_dbs)

            # Almacenar las bases de datos de las que se realizará una copia
            # de seguridad
            dbs_to_clean = get_dbnames_to_bkp(logger, dbs_all, bkp_vars)

            # Realizar las nuevas copias de seguridad (dump)
            make_clean(logger, bkps_list, dbs_to_clean, pg_dbs,
                       bkp_vars['bkp_path'], bkp_vars['prefix'],
                       bkp_vars['min_bkps'], bkp_vars['obs_days'],
                       bkp_vars['max_tsize'])

        else:
            message = 'El directorio especificado en el archivo de ' \
                      'configuración no contiene copias de seguridad cuyos ' \
                      'nombres sigan el patrón del programa.'
            logger_colored(logger, 'warning', message, 'yellow', effect='bold')
    else:
        message = 'El directorio especificado en el archivo de ' \
                  'configuración está vacío.'
        logger_colored(logger, 'warning', message, 'yellow', effect='bold')

    bkp_warning(logger, pg_dbs, bkped_dbs)

    # Cerrar comunicación con la base de datos
    pg_disconnect(logger, conn, cursor)
