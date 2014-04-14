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
# Importar las funciones create_dir, default_bkps_path, default_cfg_path de la
# librería personalizada dir_tools.dir_tools (para crear directorios de forma
# automática y localizar archivos creados por defecto)
from dir_tools.dir_tools import default_cfg_path
from config.config_tools import load_cleanerall
from math import ceil
import os  # Importar la librería os (para trabajar con directorios y archivos)
import re  # Importar la librería glob (para buscar archivos en directorios)
import time  # Importar la librería time (para calcular intervalos de tiempo)
# Importar la librería argparse (para trabajar con el vector argv fácilmente)
import argparse


# ************************* DEFINICIÓN DE FUNCIONES *************************

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


def del_ht_bkps(logger, ht_bkps_list, path, min_bkps, obs_days, max_tsize):
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
    num_bkps = len(ht_bkps_list)
    # Realizar una copia de la lista de copias de seguridad para poderla
    # manipular sin problemas en mitad de un bucle
    ht_bkps_lt = ht_bkps_list[:]

    unlinked = False

    message = 'Iniciando limpieza de copias de seguridad del clúster de ' \
              'PostgreSQL del servidor.'
    logger_colored(logger, 'info', message, 'white')

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

    tsize = get_files_tsize(ht_bkps_lt, path)
    tsize_mb = ceil(tsize / 10 ** 6)

    ## DESCOMENTAR ESTA SECCIÓN PARA PROCEDER CON LA ELIMINACIÓN DE COPIAS SI
    ## EL TAMAÑO DEL TOTAL DE ÉSTAS SUPERA EL TAMAÑO MÁXIMO ESPECIFICADO.
    #ht_bkps_list = ht_bkps_lt[:]

    #for f in ht_bkps_list:
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
            ## ht_bkps_lt.remove(f)
            #tsize -= file_info.st_size  # Actualizar el tamaño total

    if not unlinked:
        logger.info('No se ha eliminado ninguna copia del cúster del '
                    'servidor.')

    if tsize > max_tsize:
        message = 'El tamaño del total de copias de seguridad en disco del ' \
                  'clúster es de {} MB, que es mayor que el máximo ' \
                  'especificado ({} MB).'.format(tsize_mb, max_tsize_mb)
        logger_colored(logger, 'warning', message, 'yellow', effect='bold')

    message = 'Limpieza de copias de seguridad del clúster del servidor ' \
              'completada.'
    logger_colored(logger, 'info', message, 'green')


def make_clean(logger, bkps_list, path, prefix, min_bkps, obs_days, max_tsize):
    # Declarar la expresión regular que detecta si el nombre del archivo
    # de backup se corresponde con una copia generada por el programa dump.py
    if prefix:
        regex = r'(' + prefix + ')ht_(.+_cluster)_(\d{8}_\d{6}_.+)\.' \
                '(?:dump|bz2|gz|zip)$'
    else:
        regex = r'(.*)?ht_(.+_cluster)_(\d{8}_\d{6}_.+)\.(?:dump|bz2|gz|zip)$'
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
        del_ht_bkps(logger, ht_bkps_list, path, min_bkps, obs_days, max_tsize)
    else:
        message = 'El directorio especificado en el archivo de ' \
                  'configuración no contiene copias de seguridad cuyos ' \
                  'nombres sigan el patrón del programa.'
        logger_colored(logger, 'warning', message, 'yellow', effect='bold')


# ************************* PROGRAMA PRINCIPAL *************************

if __name__ == "__main__":

    # Crear un logger para los mensajes de información
    logger = create_logger()

    # Asignar ruta por defecto al archivo de configuración
    cfg_path = default_cfg_path('cleaner/cleanerall.cfg')
    # Crear parseador para obtener fácilmente los parámetros enviados desde
    # consola
    parser = argparse.ArgumentParser()
    # Crear un parámetro personalizado para enviar al programa desde consola
    parser.add_argument('-c', '--config',
                        help='load a configuration file (.cfg)',
                        default=cfg_path)
    args = parser.parse_args()  # Guardar los parámetros creados

    # Cargar variables del archivo .cfg
    bkp_vars = load_cleanerall(logger, args.config)

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

    # Ejecutar consulta de PostgreSQL y obtener nombres de todas las bases de
    # datos almacenadas, sus permisos de conexión y sus propietarios

    bkps_list = sorted_flist(bkps_dir)

    if bkps_list:
        # Realizar las nuevas copias de seguridad (dump)
        make_clean(logger, bkps_list, bkp_vars['bkp_path'], bkp_vars['prefix'],
                   bkp_vars['min_bkps'], bkp_vars['obs_days'],
                   bkp_vars['max_tsize'])
    else:
        message = 'El directorio especificado en el archivo de ' \
                  'configuración está vacío.'
        logger_colored(logger, 'warning', message, 'yellow', effect='bold')

    # Cerrar comunicación con la base de datos
    pg_disconnect(logger, conn, cursor)
