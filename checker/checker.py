#!/usr/bin/env python3
# -*- encoding: utf-8 -*-


# ************************* CARGA DE LIBRERÍAS *************************

#from logger.logger import Logger
# Importar la librería configparser (para obtener datos de un archivo .cfg)
import re  # Importar la librería re (para trabajar con expresiones regulares)
from messenger.messenger import Default


# ************************* DEFINICIÓN DE FUNCIONES *************************

class Checker:

    def __init__(self):
        pass

    @staticmethod
    def str_is_bool(string):
        if string in Default.VALID_BOOLS:
            return True
        else:
            return False

    @staticmethod
    def str_is_int(string):
        try:
            int(string)
            return True
        except:
            return False

    @staticmethod
    def str_is_valid_exp_days(string):
        try:
            result = int(string)
            if result >= -1:
                return True
            else:
                return False
        except:
            return False

    @staticmethod
    def str_is_valid_max_size(string):
        regex = r'(\d+)(MB|GB|TB|PB)$'
        regex = re.compile(regex)  # Validar la expresión regular
        if re.match(regex, string):
            return True
        else:
            return False

    @staticmethod
    def check_regex(regex):
        '''
    Objetivo:
        - comprobar que una expresión regular sea correcta.
    Parámetros:
        - regex: la expresión regular a analizar.
    Devolución:
        - el resultado de la comprobación.
    '''
        try:  # Probar si hay excepciones en...
            re.compile(regex)  # Compilar regex
            return True
        except re.error:  # Si salta la excepción re.error...
            #logger.debug('Error en la función "check_regex": {}.'.format(
                #str(e)))
            return False  # Marcar regex como incorrecta

    @staticmethod
    def check_compress_type(c_type):
        '''
    Objetivo:
        - comprobar la validez de los tipos de extensión para comprimir
        archivos.
    Parámetros:
        - logger: el logger que se empleará para mostrar y registrar el
        mensaje.
        - c_type: el tipo de extensión a analizar.
    '''
        # Comprobar si las extensiones para comprimir las copias son válidas
        if c_type in Default.BKP_TYPES:
            return c_type
        else:
            #logger.debug('Error en la función "check_compress_type".')
            return False
