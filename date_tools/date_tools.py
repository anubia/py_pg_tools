#!/usr/bin/env python3
# -*- encoding: utf-8 -*-


# ************************* CARGA DE LIBRERÍAS *************************

import datetime  # Importar la librería datetime (para manejar fechas)
import time  # Importar la librería time (para manejar fechas)
from dateutil.tz import tzlocal
# Importar la librería tzlocal del paquete dateutil.tz (para manejar fechas)


# ************************* DEFINICIÓN DE FUNCIONES *************************

class DateTools:

    def __init__(self):
        pass

    @staticmethod
    def get_date(fmt='%Y%m%d_%H%M%S_%Z'):
        '''
    Objetivo:
        - obtener la fecha actual de la zona en un formato determinado.
    Devolución:
        - la fecha actual en el formato establecido.
    '''
        # Obtener fecha y hora actuales de la zona
        init_time = datetime.datetime.now(tzlocal())
        init_ts = init_time.strftime(fmt)  # Cambiar el formato de la fecha
        return init_ts  # Devolver la fecha actual en el formato deseado

    @staticmethod
    def get_year(date_str, fmt='%Y%m%d_%H%M%S_%Z'):
        '''
    Objetivo:
        - obtener el año de una fecha dada en formato string.
    Devolución:
        - el año de la fecha dada en formato string.
    '''
        # Convertir string a objeto date
        init_ts = time.strptime(date_str, fmt)
        yy = init_ts.tm_year  # Obtener el año
        # Añadir ceros a la derecha a los años de menos de cuatro dígitos
        year = str(yy).rjust(4, '0')
        return year  # Devolver el año

    @staticmethod
    def get_month(date_str, fmt='%Y%m%d_%H%M%S_%Z'):
        '''
    Objetivo:
        - obtener el mes de una fecha dada en formato string.
    Devolución:
        - el mes de la fecha dada en formato string.
    '''
        # Convertir string a objeto date
        init_ts = time.strptime(date_str, fmt)
        mm = init_ts.tm_mon  # Obtener el mes
        # Añadir un cero a la derecha a los meses de un dígito
        month = str(mm).rjust(2, '0')
        return month  # Devolver el mes
