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
from date_tools.date_tools import DateTools  # Librería personalizada
# Importar la función get_date de la librería date (para obtener la fecha
# de la zona en el formato deseado)
from const.const import Default
from checker.checker import Checker
from casting.casting import Casting


# ************************* DEFINICIÓN DE FUNCIONES *************************

class CustomRotatingFileHandler(logging.handlers.RotatingFileHandler):

    import re
    ansi_escape = re.compile(r'\x1b[^m]*m')

    def emit(self, record):
        record.msg = self.ansi_escape.sub('', record.msg)
        logging.handlers.RotatingFileHandler.emit(self, record)


class Logger:

    logger = None
    log_dir = None
    level = None
    mute = False

    def __init__(self, log_dir=None, level=None, mute=False):
        '''
    Objetivo:
        - generar un logger con handlers para consola (en nivel INFO) y para
        archivo (en nivel DEBUG). Crear directorio "log" si no existe y
        almacenar en su interior los archivos "log" generados.
    Devolución:
        - el logger que se usará para mostrar mensajes.
    '''
        if log_dir:
            self.log_dir = log_dir
        else:
            # Obtener directorio de esta librería
            script_dir = os.path.dirname(os.path.realpath(__file__))
            # Obtener directorio padre de esta librería
            script_pardir = os.path.abspath(os.path.join(script_dir,
                                                         os.pardir))
            self.log_dir = os.path.join(script_pardir, 'log/')

        if level in Default.LOG_LEVELS:
            self.level = level
        else:
            self.level = Default.LOG_LEVEL

        if isinstance(mute, bool):
            self.mute = mute
        elif Checker.str_is_bool(mute):
            self.mute = Casting.str_to_bool(mute)
        else:
            self.mute = Default.MUTE

        # Obtener fecha y hora actuales de la zona
        init_ts = DateTools.get_date()
        # Obtener nombre de este archivo
        script_filename = os.path.basename(sys.argv[0])
        # Obtener nombre de este script
        script_name = os.path.splitext(script_filename)[0]
        # Establecer formato para el nombre de los archivos "logs"
        log_name = script_name + '_' + init_ts + '.log'
        # Establecer ruta completa de los archivos "logs"
        log_file = os.path.join(self.log_dir, log_name)
        # Crear logger con el mismo nombre de este script
        self.logger = logging.getLogger(script_name)
        # Establecer DEBUG como nivel máximo para el logger
        self.logger.setLevel(logging.DEBUG)
        # Crear un handler para consola
        ch = logging.StreamHandler()
        # Poner el nivel del handler de consola a sólo "INFO" (no ver "DEBUG")
        ch.setLevel(logging.INFO)
        # Si en el directorio actual no existe un directario llamado "log"...
        formatter = logging.Formatter('%(asctime)s - %(levelname)-4s - '
                                      '%(message)s',
                                      datefmt='%Y.%m.%d_%H:%M:%S_%Z')
        if self.mute is False:
            if not os.path.exists(self.log_dir):
                os.makedirs(self.log_dir)  # Crear directorio "log"
            # Establecer tamaño que tendrán los archivos "log"
            max_bytes = 4 * 1024 * 1024  # 4MiB
            # Crear un handler para un archivo
            fh = CustomRotatingFileHandler(log_file, 'a', max_bytes, 10)
            # Poner el nivel del handler de archivo a "DEBUG" (ver todos los
            # mensajes)
            if self.level == 'debug':
                fh.setLevel(logging.DEBUG)
            if self.level == 'info':
                fh.setLevel(logging.INFO)
            if self.level == 'warning':
                fh.setLevel(logging.WARNING)
            if self.level == 'error':
                fh.setLevel(logging.ERROR)
            if self.level == 'critical':
                fh.setLevel(logging.CRITICAL)
            # Establecer un formato para los mensajes del logger
            fh.setFormatter(formatter)  # Añadir formato al handler del archivo

        ch.setFormatter(formatter)  # Añadir formato al handler de la consola
        self.logger.addHandler(ch)  # Añadir handler de la consola al logger

        if self.mute is False:
            self.logger.addHandler(fh)  # Añadir handler del archivo al logger

    def debug(self, message):
        self.logger.debug(message)

    def info(self, message):
        self.logger.info(message)

    def warning(self, message):
        self.logger.warning(message)

    def error(self, message):
        self.logger.error(message)

    def critical(self, message):
        self.logger.critical(message)

    def highlight(self, level, message, txtcolor='default', bgcolor='black',
                  effect='default'):

        eff = Logger.__get_effect_code(effect)
        bg = Logger.__get_bgcolor_code(bgcolor)
        txt = Logger.__get_txtcolor_code(txtcolor)

        if level == 'info':
            self.info('\033[{};{};{}m'.format(eff, bg, txt) + message +
                      '\033[0m')
        elif level == 'warning':
            self.warning('\033[{};{};{}m'.format(eff, bg, txt) + message +
                         '\033[0m')
        elif level == 'error':
            self.error('\033[{};{};{}m'.format(eff, bg, txt) + message +
                       '\033[0m')
        elif level == 'critical':
            self.critical('\033[{};{};{}m'.format(eff, bg, txt) + message +
                          '\033[0m')
        else:
            self.debug('\033[{};{};{}m'.format(eff, bg, txt) + message +
                       '\033[0m')

    def stop_exe(self, message):
        '''
    Objetivo:
        - mostrar y registrar un mensaje de error, e interrumpir la ejecución
        del programa.
    Parámetros:
        - logger: el logger que se empleará para mostrar y registrar el
        mensaje.
        - message: el mensaje a mostrar al usuario y registrar en log.
    '''
        self.highlight('error', message, 'white', 'red', 'bold')
        sys.exit(1)  # Interrumpir la ejecución del programa

    @staticmethod
    def __get_txtcolor_code(txtcolor):
        # Declarar un diccionario con los códigos ANSI de colores de texto
        # en consola
        txtcolors = {
            'black': 90,
            'darkred': 31,
            'red': 91,
            'darkgreen': 32,
            'green': 92,
            'orange': 33,
            'yellow': 93,
            'darkblue': 34,
            'blue': 94,
            'darkpurple': 35,
            'purple': 95,
            'darkcyan': 36,
            'cyan': 96,
            'white': 97,
            'default': 37,
        }
        return txtcolors[txtcolor]

    @staticmethod
    def __get_bgcolor_code(bgcolor):
        # Declarar un diccionario con los códigos ANSI de colores de fondo en
        # consola
        bgcolors = {
            'black': 40,
            'red': 41,
            'green': 42,
            'orange': 43,
            'blue': 44,
            'purple': 45,
            'cyan': 46,
            'white': 47,
        }
        return bgcolors[bgcolor]

    @staticmethod
    def __get_effect_code(effect):
        # Declarar un diccionario con los códigos ANSI de efectos en consola
        effects = {
            'default': 0,
            'bold': 1,
            'underline': 4,
            'blink': 5,
            'inverse': 7,
            'hidden': 8,
        }
        return effects[effect]
