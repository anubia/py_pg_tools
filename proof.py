#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

#from connecter import Connecter

#connecter = Connecter('localhost', 'anubia', '', 5432)

#query_get_dbs = (
    #'SELECT d.datname, d.datallowconn, '
    #'pg_catalog.pg_get_userbyid(d.datdba) as owner '
    #'FROM pg_catalog.pg_database d;'
#)

#connecter.cursor.execute(query_get_dbs)

#for record in connecter.cursor:
    #print(record[0])

import zipfile
import os.path
import os

def unzip(zipFilePath, destDir):
    zfile = zipfile.ZipFile(zipFilePath)
    for name in zfile.namelist():
        print(name)
        (dirName, fileName) = os.path.split(name)
        if fileName == '':
            # directory
            newDir = destDir + '/' + dirName
            if not os.path.exists(newDir):
                os.mkdir(newDir)
        else:
            # file
            fd = open(destDir + '/' + name, 'wb')
            fd.write(zfile.read(name))
            fd.close()
    zfile.close()

unzip("/opt/backups/pg_backups/my_server/db_backups/2014/05/db_devel__v61__test_01_20140509_115129_CEST.zip", '/opt/backups/pg_backups/my_server/db_backups/2014/05')
