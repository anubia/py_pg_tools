#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

import re  # Importar la librería re (para trabajar con expresiones regulares)


class Casting:

    def __init__(self):
        pass

    @staticmethod
    def str_to_bool(boolean):
        '''
    Objetivo:
        - convierte una cadena en un booleano, si la cadena es correcta.
    Parámetros:
        - boolean: la cadena que se convierte a booleano.
    Devolución:
        - una variable de tipo booleano, "None" si la cadena era incorrecta.
    '''
        # Si en el .cfg se escribió True bien...
        if boolean.lower() == 'true':
            return True
        # Si en el .cfg se escribió False bien...
        elif boolean.lower() == 'false':
            return False
        else:  # Si la cadena no se puede convertir a booleano...
            return None

    @staticmethod
    def str_to_list(string):
        '''
    Objetivo:
        - convierte una cadena en una lista de elementos, que vendrán
        delimitados por comas. Se emplea para cargar las variables del archivo
        de configuración que deben ser tratadas como listas.
    Parámetros:
        - string: la cadena que se quiere convertir en una lista.
    Devolución:
        - la lista resultante de dividir la cadena por sus comas.
    '''
        # Partir la cadena por sus comas y generar una lista con los fragmentos
        str_list = string.split(',')
        for i in range(len(str_list)):  # Recorrer cada elemento de la lista
            # Eliminar caracteres de espaciado a cada elemento de la lista
            str_list[i] = str_list[i].strip()
        return str_list  # Devolver una lista de elementos sin espaciados

    @staticmethod
    def str_to_int(string):
        try:
            result = int(string)
            return result
        except:
            return False

    @staticmethod
    def str_to_max_size(string):

        regex = r'(\d+)(MB|GB|TB|PB)$'
        regex = re.compile(regex)  # Validar la expresión regular
        if re.match(regex, string):
            parts = regex.search(string).groups()
            max_size = {
                'size': int(parts[0]),
                'unit': parts[1],
            }
            return max_size
        else:
            return None
