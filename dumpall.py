#!/usr/bin/env python3
# -*- encoding: utf-8 -*-


# ************************* CARGA DE LIBRERÍAS *************************

# Importar la funciones create_logger y logger_fatal de la librería
# personalizada logger.logger (para utilizar un logger que muestre información
# al usuario)
from logger.logger import create_logger, logger_fatal, logger_colored
# Importar la funciones pg_connect y pg_disconnect de la librería
# personalizada pg_connection.pg_connection (para conectarse y desconectarse a
# PostgreSQL y poder ejecutar consultas)
from pg_connection.pg_connection import pg_connect, pg_disconnect
# Importar la funciones create_dir, default_bkps_path y default_cfg_path de la
# librería personalizada dir_tools.dir_tools (para trabajar con directorios y
# archivos)
from pg_tools.pg_tools import is_pg_superuser
from dir_tools.dir_tools import create_dir, default_bkps_path, default_cfg_path
# Importar la función get_date de la librería personalizada
# custom_date.custom_date (para obtener la fecha y hora actuales de la zona en
# el formato deseado)
from date_tools.date_tools import get_date, get_year
# Importar la función load_dump de la librería personalizada
# config.config_tools (para obtener datos del archivo config)
from config.config_tools import load_dumpall
# Importar la librería subprocess (para realizar consultas a las bases de datos
# de PostgreSQL)
import subprocess
# Importar la librería argparse (para trabajar con el vector argv fácilmente)
import argparse


# ************************* DEFINICIÓN DE FUNCIONES *************************

def dump_cluster(bkps_dir, ext, user, prefix='', server='localhost',
                 port=5432):
    '''
Objetivo:
    - crear una copia de seguridad del cluster de PostgreSQL del servidor
    especificado.
Parámetros:
    - bkp_dir: directorio donde se guardan las copias de seguridad.
    - ext: tipo de extensión que tendrá el archivo que contiene la copia.
    - user: usuario de PostgreSQL.
    - prefix: prefijo a incluir en el nombre de las copias de seguridad
    - server: servidor donde se se encuentra alojado el cluster de bases de
    datos que se quiere copiar.
    - port: puerto por el que se realiza la conexión.
'''
    success = True
    init_ts = get_date()  # Obtener fecha y hora actuales de la zona
    year = str(get_year(init_ts))  # Obtener el año de la fecha almacenada
    bkp_dir = bkps_dir + year + '/'
    create_dir(logger, bkp_dir)
    # Establecer nombre del archivo que contiene la copia de seguridad
    file_name = prefix + 'ht_' + server + '_cluster_' + init_ts + ext
    # Almacenar la instrucción a realizar en consola
    if ext == '.gz':  # Comprimir con gzip
        command = 'pg_dumpall -U {} -h {} -p {} | gzip > {}'.format(
            user, server, port, bkp_dir + file_name)
    elif ext == '.bz2':  # Comprimir con bzip2
        command = 'pg_dumpall -U {} -h {} -p {} | bzip2 > {}'.format(
            user, server, port, bkp_dir + file_name)
    elif ext == '.zip':  # Comprimir con zip
        command = 'pg_dumpall -U {} -h {} -p {} | zip > {}'.format(
            user, server, port, bkp_dir + file_name)
    else:  # No comprimir la copia
        command = 'pg_dumpall -U {} -h {} -p {} > {}'.format(
            user, server, port, bkp_dir + file_name)
    try:  # Probar que la copia se realiza correctamente
        # Ejecutar la instrucción de la copia de seguridad en consola
        result = subprocess.call(command, shell=True)
        if result != 0:  # Si el comando no de resultados en consola...
            raise Exception()  # Lanzar excepción
    except Exception as e:
        logger.debug('Error en la función "dump_cluster": {}.'.format(str(e)))
        success = False
    return success


def make_bkp(logger, bkps_dir, bkp_vars):
    '''
Objetivo:
    - crear copias de seguridad de las bases de datos especificadas, las que
    están incluidas en la variable "dbs_all".
Parámetros:
    - logger: el logger que se empleará para mostrar y registrar el mensaje.
    - bkp_dir: directorio donde se guardan las copias de seguridad.
    - bkp_vars: diccionario con los parámetros especificados en el archivo .cfg
'''
    message = 'Comprobando directorio de destino de las copias... '
    bkp_dir = bkps_dir + bkp_vars['server_alias'] + '/dumpall/'
    create_dir(logger, bkps_dir)
    message += 'Directorio de destino existente.'
    logger_colored(logger, 'info', message, 'white')

    message = 'Iniciando copia de seguridad de del clúster de bases de ' \
              'datos...'
    logger_colored(logger, 'info', message, 'white')

    success = dump_cluster(bkp_dir, bkp_vars['bkp_type'], bkp_vars['user'],
                           bkp_vars['prefix'], bkp_vars['server'],
                           bkp_vars['port'])
    if success:
        message = 'Copia de seguridad del clúster de bases de datos ' \
                  'completada.'
        logger_colored(logger, 'info', message, 'green')
    else:
        message = 'La copia de seguridad del clúster de bases de datos ' \
                  'no se pudo completar.'
        logger_colored(logger, 'warning', message, 'yellow', effect='bold')


# ************************* PROGRAMA PRINCIPAL *************************

if __name__ == "__main__":

     # Crear un logger para los mensajes de información
    logger = create_logger()

    # Asignar ruta por defecto al archivo de configuración
    cfg_path = default_cfg_path('dumper/dumpall.cfg')
    # Crear parseador para obtener fácilmente los parámetros enviados desde
    # consola
    parser = argparse.ArgumentParser()
    # Crear un parámetro personalizado para enviar al programa desde consola
    parser.add_argument('-c', '--config',
                        help='load a configuration file (.cfg)',
                        default=cfg_path)
    args = parser.parse_args()  # Guardar los parámetros creados

    # Cargar variables del archivo .cfg
    bkp_vars = load_dumpall(logger, args.config)

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
        logger_fatal(logger, 'El usuario especificado para la conexión a '
                             'PostgreSQL no tiene rol de superusuario: no '
                             'puede actuar sobre el clúster de bases de '
                             'datos.')

    # Asegurar la existencia de un directorio donde almacenar las copias de
    # seguridad de PostgreSQL
    if bkp_vars['bkp_path']:
        bkps_dir = bkp_vars['bkp_path']
    else:
        bkps_dir = default_bkps_path()
    create_dir(logger, bkps_dir)

    # Realizar copias de seguridad del cluster (dumpall)
    make_bkp(logger, bkps_dir, bkp_vars)

    # Cerrar comunicación con la base de datos
    pg_disconnect(logger, conn, cursor)
