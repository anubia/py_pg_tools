#!/usr/bin/env python3
# -*- encoding: utf-8 -*-


# ************************* CARGA DE LIBRERÍAS *************************

# Importar la función logger_fatal de la librería personalizada logger.logger
# (para utilizar un logger que proporcione información al usuario)
from logger.logger import logger_fatal
import os  # Importar la librería os (para trabajar con directorios y archivos)


# ************************* DEFINICIÓN DE FUNCIONES *************************

def create_dir(logger, path):
    '''
Objetivo:
    - comprobar que exista una ruta determinada, de no ser así, crearla.
Parámetros:
    - logger: el logger que se empleará para mostrar y registrar el mensaje.
    - path: la ruta que debe existir o generarse.
'''
    try:  # Comprobar si al intentar leer o generar un directorio hay error
        if not os.path.exists(path):  # Si la ruta no existe...
            os.makedirs(path)  # Generar ruta
    except Exception as e:  # Si salta una excepción...
        logger.debug('Error en la función "create_dir": {}.'.format(str(e)))
        logger_fatal(logger, 'El programa no pudo generar el directorio '
                             'necesario para su ejecución: revise los permisos'
                             ' de las carpetas que éste emplea.')


def default_bkps_path():
    '''
Objetivo:
    - devuelve la ruta por defecto donde debe estar el archivo de configuración
    en caso de que no se indique una ruta mediante el comando -c en la llamada
    al programa desde consola.
Devolución:
    - la ruta absoluta que debe tener el archivo de configuración por defecto.
'''
    # Obtener el directorio donde se encuentra este script
    script_dir = os.path.dirname(os.path.realpath(__file__))
    # Cuidado con la ubicación de la librería dir_tools
    parent_dir = os.path.abspath(os.path.join(script_dir, os.pardir))
    bkps_folder = 'pg_backups/'
    # Localizar el archivo .cfg que contiene la información deseada
    bkps_file = os.path.join(parent_dir, bkps_folder)
    return bkps_file


def default_cfg_path(subpath):
    '''
Objetivo:
    - devuelve la ruta por defecto donde debe estar el archivo de configuración
    en caso de que no se indique una ruta mediante el comando -c en la llamada
    al programa desde consola.
Parámetros:
    - subpath: el nombre del archivo de configuración por defecto, que podrá
    tener diversos nombres según la operación que se esté llevando a cabo, y la
    carpeta que lo contiene.
Devolución:
    - la ruta absoluta que debe tener el archivo de configuración por defecto.
'''
    # Obtener el directorio donde se encuentra este script
    script_dir = os.path.dirname(os.path.realpath(__file__))
    # Localizar el archivo .cfg que contiene la información deseada
    parent_dir = os.path.abspath(os.path.join(script_dir, os.pardir))
    cfg_folder = 'config/' + subpath
    cfg_file = os.path.join(parent_dir, cfg_folder)
    return cfg_file
