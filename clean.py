#!/usr/bin/env python3
# -*- encoding: utf-8 -*-


# ************************* CARGA DE LIBRERÍAS *************************

# Importar la funciones create_logger y fatal_logger de la librería
# personalizada logger.logger (para utilizar un logger que proporcione
# información al usuario)
from logger.logger import Logger
# Importar la funciones pg_connect y pg_disconnect de la librería
# personalizada pg_connection.pg_connection (para conectarse y desconectarse a
# PostgreSQL y poder ejecutar consultas)
from pg_connection.pg_connection import Connection
from db_selector.db_selector import DbSelector
# Importar las funciones create_dir, default_bkps_path, default_cfg_path de la
# librería personalizada dir_tools.dir_tools (para crear directorios de forma
# automática y localizar archivos creados por defecto)
from dir_tools.dir_tools import Dir
from config.config_tools import CfgParser
from pg_tools.pg_tools import PgTools
import os  # Importar la librería os (para trabajar con directorios y archivos)
# Importar la librería argparse (para trabajar con el vector argv fácilmente)
import argparse


# ************************* DEFINICIÓN DE FUNCIONES *************************


# ************************* PROGRAMA PRINCIPAL *************************

if __name__ == "__main__":

    # Crear un logger para los mensajes de información
    logger = Logger()

    Dir.is_root(logger)  # Parar la ejecución si el programa lo ejecuta "root"

    # Asignar ruta por defecto al archivo de configuración
    conn_cfg_path = Dir.default_cfg_path('connection/connection.cfg')
    clean_cfg_path = Dir.default_cfg_path('cleaner/clean.cfg')
    # Crear parseador para obtener fácilmente los parámetros enviados desde
    # consola
    arg_parser = argparse.ArgumentParser()
    # Crear un parámetro personalizado para enviar al programa desde consola
    arg_parser.add_argument('-c', '--conn',
                            help='load a configuration file (.cfg) to get the '
                                 'PostgreSQL connection parameters',
                                 default=conn_cfg_path)
    arg_parser.add_argument('-t', '--tidy',
                            help='load a configuration file (.cfg) to get the '
                                 'cleaner conditions', default=clean_cfg_path)

    args = arg_parser.parse_args()  # Guardar los parámetros creados

    parser = CfgParser(logger)

    if parser.bkp_vars['pg_warnings']:
        # Cargar variables de conexión del archivo .cfg obtenido a través de
        # args
        parser.load_cfg(args.conn)
        parser.parse_pgconn()

    # Cargar variables generales del archivo .cfg obtenido a través de args
    parser.load_cfg(args.tidy)
    parser.parse_clean()

    # Asegurar la existencia de un directorio donde almacenar las copias de
    # seguridad de PostgreSQL
    bkps_dir = parser.bkp_vars['bkp_path']
    if not os.path.isdir(bkps_dir):
        logger.stop_exe('El directorio especificado en el archivo de '
                        'configuración no existe.')

    bkps_list = Dir.sorted_flist(bkps_dir)

    if bkps_list:

        bkped_dbs = Dir.get_dbs_bkped(bkps_list)

        if bkped_dbs:

            # Almacenar las bases de datos de las que se realizará una
            # copia de seguridad
            dbs_to_clean = DbSelector.get_filtered_dbnames(
                bkped_dbs, parser.bkp_vars['in_dbs'],
                parser.bkp_vars['ex_dbs'], parser.bkp_vars['in_regex'],
                parser.bkp_vars['ex_regex'], parser.bkp_vars['in_priority'],
                logger)

            # Realizar la limpieza (clean)
            PgTools.clean_dbs(parser.bkp_vars['bkp_path'], bkps_list,
                              dbs_to_clean, parser.bkp_vars['max_tsize'],
                              parser.bkp_vars['min_bkps'],
                              parser.bkp_vars['obs_days'],
                              parser.bkp_vars['prefix'], logger)

        else:
            message = 'El directorio especificado en el archivo de ' \
                      'configuración no contiene copias de seguridad ' \
                      'cuyos nombres sigan el patrón del programa.'
            logger.set_view('warning', message, 'yellow', effect='bold')
    else:
        message = 'El directorio especificado en el archivo de ' \
                  'configuración está vacío.'
        logger.set_view('warning', message, 'yellow', effect='bold')

    if parser.bkp_vars['pg_warnings']:

        # Iniciar conexión a la base de datos "template1" con el usuario
        # especificado
        conn = Connection(parser.conn_vars['server'], parser.conn_vars['user'],
                          parser.conn_vars['pwd'], parser.conn_vars['port'],
                          logger)

        # Ejecutar consulta de PostgreSQL y obtener nombres de todas las bases
        # de datos almacenadas, sus permisos de conexión y sus propietarios
        conn.get_cursor_dbs(False)

        pg_dbs = []
        for record in conn.cursor:  # Para cada registro de la consulta...
            pg_dbs.append(record[0])

        bkped_dbs = Dir.get_dbs_bkped(bkps_list)

        Dir.show_pg_warnings(pg_dbs, bkped_dbs, logger)

        # Cerrar comunicación con la base de datos
        conn.pg_disconnect()
