#!/usr/bin/env python3
# -*- encoding: utf-8 -*-


# ************************* CARGA DE LIBRERÍAS *************************

# Importar la funciones create_logger y fatal_logger de la librería
# personalizada logger.logger (para utilizar un logger que muestre información
# al usuario)
from logger.logger import Logger
# Importar la funciones pg_connect y pg_disconnect de la librería
# personalizada pg_connection.pg_connection (para conectarse y desconectarse a
# PostgreSQL y poder ejecutar consultas)
from pg_connection.pg_connection import Connection
# Importar la funciones create_dir, default_bkps_path y default_cfg_path de la
# librería personalizada dir_tools.dir_tools (para trabajar con directorios y
# archivos)
from dir_tools.dir_tools import Dir
# Importar la función load_dump de la librería personalizada
# config.config_tools (para obtener datos del archivo config)
from config.config_tools import CfgParser
from pg_tools.pg_tools import PgTools
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
    dumpall_cfg_path = Dir.default_cfg_path('dumper/dumpall.cfg')
    # Crear parseador para obtener fácilmente los parámetros enviados desde
    # consola
    arg_parser = argparse.ArgumentParser()
    # Crear un parámetro personalizado para enviar al programa desde consola
    arg_parser.add_argument('-c', '--conn',
                            help='load a configuration file (.cfg) to get the '
                                 'PostgreSQL connection parameters',
                                 default=conn_cfg_path)
    arg_parser.add_argument('-D', '--dumpall',
                            help='load a configuration file (.cfg) to get the '
                                 'dumper conditions',
                                 default=dumpall_cfg_path)

    args = arg_parser.parse_args()  # Guardar los parámetros creados

    parser = CfgParser(logger)

    # Cargar variables de conexión del archivo .cfg obtenido a través de args
    parser.load_cfg(args.conn)
    parser.parse_pgconn()
    # Cargar variables generales del archivo .cfg obtenido a través de args
    parser.load_cfg(args.dumpall)
    parser.parse_dumpall()

    # Iniciar conexión a la base de datos "template1" con el usuario
    # especificado
    conn = Connection(parser.conn_vars['server'], parser.conn_vars['user'],
                      parser.conn_vars['pwd'], parser.conn_vars['port'],
                      logger)

    # Comprobar si el usuario actualmente conectado es superusuario de
    # PostgreSQL
    pg_superuser = conn.is_pg_superuser()
    if not pg_superuser:  # Si no es superusuario de PostgreSQL...
        logger.stop_exe('El usuario especificado para la conexión a '
                        'PostgreSQL no tiene rol de superusuario: no puede '
                        'actuar sobre el clúster de bases de datos.')

    # Asegurar la existencia de un directorio donde almacenar las copias de
    # seguridad de PostgreSQL
    if parser.bkp_vars['bkp_path']:
        bkps_dir = parser.bkp_vars['bkp_path']
    else:
        bkps_dir = Dir.default_bkps_path()
    Dir.create_dir(bkps_dir, logger)

    if parser.bkp_vars['vacuum']:
        # Ejecutar consulta de PostgreSQL y obtener nombres de todas las bases
        # de datos almacenadas, sus permisos de conexión y sus propietarios
        conn.get_cursor_dbs(ex_templates=False)

        dbs_all = []  # Inicializar lista de nombres de las bases de datos
        for record in conn.cursor:  # Para cada registro de la consulta...
            dictionary = {  # Crear diccionario con...
                'name': record[0],  # Nombre de la base de datos
                'allow_connection': record[1],  # Permiso de conexión
                'owner': record[2],  # Propietario de la base de datos
            }
            dbs_all.append(dictionary)  # Añadir diccionario a la lista de BDs

        # La siguiente línea es para poder hacer el vacuum sin tener que
        # agregar "in_forbidden" al config de dumpall
        parser.bkp_vars['in_forbidden'] = True
        message = 'Iniciando limpieza previa del clúster de bases de datos...'
        logger.set_view('info', message, 'white')
        #vacuum_dbs(conn, dbs_all, bkp_vars, logger)

    # Realizar copias de seguridad del cluster (dumpall)
    PgTools.dump_cluster(conn, bkps_dir, parser.bkp_vars['bkp_type'],
                         parser.bkp_vars['prefix'],
                         parser.bkp_vars['server_alias'], logger)

    # Cerrar comunicación con la base de datos
    conn.pg_disconnect()
