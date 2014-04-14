#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

#import re
import os  # Importar la librería os (para trabajar con directorios y archivos)


#def sorted_ls(path):
    #mtime = lambda f: os.stat(os.path.join(path, f)).st_mtime
    #return list(sorted(os.listdir(path), key=mtime))

#dbname = '01'  # OJO: ESCAPAR \ DEL NOMBRE DE LA DB
#regex = r"(.*)?db_(" + dbname + ")_(\d{8}_\d{6}_.+)\.(?:dump|bz2|gz|zip)$"
##regex = 'r"^([^_]*)_(.*)_(\d{8}_\d{6}_[^_]+\.(?:dump|bz2|gz|zip))$"'

directory = '/mnt/store1/devel/code/ide-workspace/py_pg_tools/' \
            'pg_backups/dump/2014/'

#bkps_list = sorted_ls(directory)
print(directory)
for filename in os.listdir(directory):
    info = os.stat(directory + filename)
    print(info.st_mtime, end='')

#pg_dbs = ['postgres', 'template1', 'template0', 'devel__v61__test_01',
          #'devel__v7__01_xmlrpc']

#dbs_to_del = ['01']

#bkp_dbs = []

#regex2 = r"(.*)?db_(.+)_(\d{8}_\d{6}_.+)\.(?:dump|bz2|gz|zip)$"
#regex2 = re.compile(regex2)
#for f in bkps_list:
    #print('*' * 80)
    #print(f)
    #if re.match(regex2, f):
        #almacen = regex2.search(f).groups()
        #if almacen[1] not in bkp_dbs:
            #print(almacen)
            #bkp_dbs.append(almacen[1])
    #else:
        #continue

#print('=' * 80)
#print('LAS BASES DE DATOS DE LAS QUE HAY UN BACKUP SON:')
#print(bkp_dbs)
#print('=' * 80)

#for dbname in pg_dbs:
    #if dbname not in bkp_dbs:
        #print('\033[93m' + 'OJO: LA BD {} DE POSTGRES NO TIENE '
              #'BACKUP.'.format(dbname) + '\033[0m')

#regex = re.compile(regex)
#for f in bkps_list:
    #print('*' * 80)
    #print(f)
    #if re.match(regex2, f):
        #almacen = regex2.search(f).groups()
        #print(almacen)
        #if almacen[1] not in pg_dbs:
            #print('OJO: ESTA BD NO ESTÁ EN POSTGRES.')
        #if almacen[1] in dbs_to_del:
        ## if almacen[1] == dbname:
            #print('Coincide: eliminar.')
        #else:
            #print('No coincide.')
    #else:
        #print('No coincide.')
