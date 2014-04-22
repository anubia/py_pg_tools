#!/usr/bin/env python3
# -*- encoding: utf-8 -*-


# ************************* CARGA DE LIBRERÍAS *************************

# Importar la funciones create_logger y fatal_logger de la librería
# personalizada logger.logger (para utilizar un logger que proporcione
# información al usuario)
from logger.logger import Logger
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
    cfg_path = Dir.default_cfg_path('cleaner/cleanerall.cfg')
    # Crear parseador para obtener fácilmente los parámetros enviados desde
    # consola
    parser = argparse.ArgumentParser()
    # Crear un parámetro personalizado para enviar al programa desde consola
    parser.add_argument('-c', '--config',
                        help='load a configuration file (.cfg)',
                        default=cfg_path)
    args = parser.parse_args()  # Guardar los parámetros creados

    # Cargar variables del archivo .cfg
    parser = CfgParser(args.config, logger)
    # Cargar variables generales del archivo .cfg obtenido a través de args
    parser.parse_cleanall()

    # Asegurar la existencia de un directorio donde almacenar las copias de
    # seguridad de PostgreSQL
    bkps_dir = parser.bkp_vars['bkp_path']
    if not os.path.isdir(bkps_dir):
        logger.stop_exe('El directorio especificado en el archivo de '
                        'configuración no existe.')

    bkps_list = Dir.sorted_flist(bkps_dir)

    if bkps_list:
        PgTools.clean_cluster(parser.bkp_vars['bkp_path'], bkps_list,
                              parser.bkp_vars['max_tsize'],
                              parser.bkp_vars['min_bkps'],
                              parser.bkp_vars['obs_days'],
                              parser.bkp_vars['prefix'], logger)
    else:
        message = 'El directorio especificado en el archivo de ' \
                  'configuración está vacío.'
        logger.set_view('warning', message, 'yellow', effect='bold')
