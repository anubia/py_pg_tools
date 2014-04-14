#!/usr/bin/env python3
# -*- encoding: utf-8 -*-


# ************************* CARGA DE LIBRERÍAS *************************

import datetime  # Importar la librería datetime (para manejar fechas)
import time  # Importar la librería time (para manejar fechas)
from dateutil.tz import tzlocal
# Importar la librería tzlocal del paquete dateutil.tz (para manejar fechas)


# ************************* DEFINICIÓN DE FUNCIONES *************************

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


def get_year(date_str, fmt='%Y%m%d_%H%M%S_%Z'):
    '''
Objetivo:
    - obtener el año actual de una fecha dada en formato string.
Devolución:
    - el año actual.
'''
    init_ts = time.strptime(date_str, fmt)  # Convertir string a objeto date
    year = init_ts.tm_year  # Obtener el año
    return year  # Devolver el año
