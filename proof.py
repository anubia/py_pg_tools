#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

#from connecter import Connecter

#connecter = Connecter('localhost', 'anubia', 5432)

#query_get_dbs = (
    #'SELECT * '
    #'FROM pg_user;'
#)

#connecter.cursor.execute(query_get_dbs)

#for record in connecter.cursor:
    #print(record)

#s = -1

#if isinstance(s, int):
    #print('Lo es')
#else:
    #print('No lo es')

import re
size = '20000TB'
regex = r'(\d+)(MB|GB|TB|PT)$'
regex = re.compile(regex)  # Validar la expresión regular
if re.match(regex, size):
    parts = regex.search(size).groups()
    num = parts[0]
    unit = parts[1]
    print('El tamaño es de {} y la unidad de medida los {}'.format(num, unit))
else:
    print('No es un tamaño')
