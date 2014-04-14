#!/usr/bin/env python3
# -*- encoding: utf-8 -*-


# ************************* CARGA DE LIBRERÍAS *************************

import sys  # Importar la librería sys (para trabajar con el vector argv)
import logging
# Importar la librería logging (para crear un logger y poder mostrar mensajes
# por consola y registrar más información en un archivo)
import logging.handlers
# Importar la librería logging.handlers (para crear handlers para consola y
# archivo en el logger)
import os.path
# Importar la librería os.path (para comprobar la existencia de archivos)
from date_tools.date_tools import get_date  # Librería personalizada
# Importar la función get_date de la librería date (para obtener la fecha
# de la zona en el formato deseado)


# ************************* DEFINICIÓN DE FUNCIONES *************************

def create_logger():
    '''
Objetivo:
    - generar un logger con handlers para consola (en nivel INFO) y para
    archivo (en nivel DEBUG). Crear directorio "log" si no existe y almacenar
    en su interior los archivos "log" generados.
Devolución:
    - el logger que se usará para mostrar mensajes.
'''
    init_ts = get_date()  # Obtener fecha y hora actuales de la zona
    # Obtener nombre de este archivo
    script_filename = os.path.basename(sys.argv[0])
    # Obtener nombre de este script
    script_name = os.path.splitext(script_filename)[0]
    # Obtener directorio de esta librería
    script_dir = os.path.dirname(os.path.realpath(__file__))
    # Obtener directorio padre de esta librería
    script_pardir = os.path.abspath(os.path.join(script_dir, os.pardir))
    # Establecer formato para el nombre de los archivos "logs"
    log_name = script_name + '_' + init_ts + '.log'
    # Establecer directorio para los archivos "logs"
    log_dir = os.path.join(script_pardir, 'log/')
    # Establecer ruta completa de los archivos "logs"
    log_file = os.path.join(log_dir, log_name)
    # Crear logger con el mismo nombre de este script
    logger = logging.getLogger(script_name)
    # Establecer DEBUG como nivel máximo para el logger
    logger.setLevel(logging.DEBUG)
    # Crear un handler para consola
    ch = logging.StreamHandler()
    # Poner el nivel del handler de consola a sólo "INFO" (no ver "DEBUG")
    ch.setLevel(logging.INFO)
    # Si en el directorio actual no existe un directario llamado "log"...
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)  # Crear directorio "log"
    # Establecer tamaño que tendrán los archivos "log"
    max_bytes = 4 * 1024 * 1024  # 4MiB
    # Crear un handler para un archivo
    fh = logging.handlers.RotatingFileHandler(log_file, 'a', max_bytes, 10)
    # Poner el nivel del handler de archivo a "DEBUG" (ver todos los mensajes)
    fh.setLevel(logging.DEBUG)
    # Establecer un formato para los mensajes del logger
    formatter = logging.Formatter('%(asctime)s - %(levelname)-4s - '
                                  '%(message)s',
                                  datefmt='%Y.%m.%d_%H:%M:%S_%Z')
    ch.setFormatter(formatter)  # Añadir formato al handler de la consola
    fh.setFormatter(formatter)  # Añadir formato al handler del archivo
    logger.addHandler(ch)  # Añadir handler de la consola al logger
    logger.addHandler(fh)  # Añadir handler del archivo al logger
    return logger  # Devolver logger


def highlight_msg(color, bgcolor='black', effect='default'):
    '''
Objetivo:
    - resaltar un mensaje por consola modificando su color de fondo, texto y
    efectos visuales.
Parámetros:
    - color: el color del texto del mensaje.
    - bgcolor: el color de fondo del mensaje.
    - effect: el efecto visual del mensaje
'''
    # Declarar un diccionario con los códigos ANSI de colores en consola
    cl_code = {
        'black': {'color': 90, 'bg': 40, },
        'red': {'color': 91, 'bg': 41, },
        'green': {'color': 92, 'bg': 42, },
        'yellow': {'color': 93, 'bg': 43, },
        'blue': {'color': 94, 'bg': 44, },
        'purple': {'color': 95, 'bg': 45, },
        'cyan': {'color': 96, 'bg': 46, },
        'white': {'color': 97, 'bg': 47, },
    }
    # Declarar un diccionario con los códigos ANSI de efectos en consola
    eff_code = {
        'default': 0,
        'bold': 1,
        'underline': 4,
        'blink': 5,
        'inverse': 7,
        'hidden': 8,
    }
    # Aplicar cambios a los próximos mensajes en consola
    print('\033[{};{};{}m'.format(eff_code[effect], cl_code[bgcolor]['bg'],
                                  cl_code[color]['color']))


def default_msg():
    '''
Objetivo:
    - reestablecer los colores y efectos de mensajes en consola a su estado por
    defecto.
'''
    # Aplicar cambios a los próximos mensajes en consola
    print('\033[0m')


def logger_colored(logger, level, message, color, bgcolor='black',
                   effect='default'):
    '''
Objetivo:
    - resaltar un mensaje de logger por consola modificando su color de fondo,
    texto y efectos visuales.
Parámetros:
    - logger: el logger que se empleará para mostrar y registrar el mensaje.
    - level: el nivel de información del mensaje de logger.
    - message: el mensaje a mostrar al usuario y registrar en log.
    - color: el color del texto del mensaje.
    - bgcolor: el color de fondo del mensaje.
    - effect: el efecto visual del mensaje
'''
    highlight_msg(color, bgcolor, effect)
    if level == 'info':
        logger.info(message)
    elif level == 'warning':
        logger.warning(message)
    else:
        logger.error(message)
    default_msg()


def logger_fatal(logger, message):
    '''
Objetivo:
    - mostrar y registrar un mensaje de error, e interrumpir la ejecución del
    programa.
Parámetros:
    - logger: el logger que se empleará para mostrar y registrar el mensaje.
    - message: el mensaje a mostrar al usuario y registrar en log.
'''
    highlight_msg('white', 'red', 'bold')
    logger.error(message)  # Mostrar y registrar el error
    default_msg()
    sys.exit(1)  # Interrumpir la ejecución del programa
