#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

import os

lista = []
path = '/opt/backups/pg_backups/anubia/db_backups/'
#for dirname, dirnames, filenames in os.walk(path):
    #for file in filenames:
        #filepath = os.path.realpath(os.path.join(dirname, file))
        #lista.append(filepath)
#print(lista)
#print('*' * 80)

#sorted_list = sorted(lista, key=lambda f: os.stat(f).st_mtime)
#print(sorted_list)

#for f in sorted_list:
    #print(os.path.dirname(f))


def remove_empty_dir(path):
    try:
        os.rmdir(path)
    except OSError:
        pass


def remove_empty_dirs(path):
    for root, dirnames, filenames in os.walk(path, topdown=False):
        for dirname in dirnames:
            print(os.path.realpath(os.path.join(root, dirname)))
            remove_empty_dir(os.path.realpath(os.path.join(root, dirname)))

remove_empty_dirs(path)

#import shutil
#shutil.rmtree(path)
