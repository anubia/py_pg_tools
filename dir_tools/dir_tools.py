#!/usr/bin/env python3
# -*- encoding: utf-8 -*-


# ************************* CARGA DE LIBRERÍAS *************************

from logger.logger import Logger
# Importar la librería getpass (para obtener nombres de usuarios del sistema)
from getpass import getuser
import os  # Importar la librería os (para trabajar con directorios y archivos)
import re  # Importar la librería glob (para buscar archivos en directorios)


# ************************* DEFINICIÓN DE FUNCIONES *************************

class Dir:

    def __init__(self):
        pass

    @staticmethod
    def forbid_root(logger=None):
        '''
    Objetivo:
        - comprobar que no se ejecute el programa como usuario "root".
    '''
        # Si el usuario del sistema que lanza el programa es "root"...
        if not logger:
            logger = Logger()
        try:
            if getuser() == 'root':
                raise Exception()  # Lanzar una excepción
        except Exception as e:  # Si salta una excepción...
            logger.debug('Error en la función "forbid_root": {}.'.format(
                str(e)))
            logger.stop_exe('Por seguridad, no se permite la ejecución del '
                            'programa como usuario "root".')

    @staticmethod
    def create_dir(path, logger=None):
        '''
    Objetivo:
        - comprobar que exista una ruta determinada, de no ser así, crearla.
    Parámetros:
        - logger: el logger que se empleará para mostrar y registrar el
        mensaje.
        - path: la ruta que debe existir o generarse.
    '''
        if not logger:
            logger = Logger()
        try:  # Comprobar si al intentar leer o generar un directorio hay error
            if not os.path.exists(path):  # Si la ruta no existe...
                os.makedirs(path)  # Generar ruta
        except Exception as e:  # Si salta una excepción...
            logger.debug('Error en la función "create_dir": {}.'.format(
                str(e)))
            logger.stop_exe('El programa no pudo generar directorios o '
                            'archivos necesarios para su funcionamiento: '
                            'revise los permisos de las carpetas que emplea.')

    @staticmethod
    def default_bkps_path():
        '''
    Objetivo:
        - devuelve la ruta por defecto donde debe estar el archivo de
        configuración en caso de que no se indique una ruta mediante el comando
        -c en la llamada al programa desde consola.
    Devolución:
        - la ruta absoluta que debe tener el archivo de configuración por
        defecto.
    '''
        ## Obtener el directorio donde se encuentra este script
        #script_dir = os.path.dirname(os.path.realpath(__file__))
        ## Cuidado con la ubicación de la librería dir_tools
        #parent_dir = os.path.abspath(os.path.join(script_dir, os.pardir))
        #bkps_folder = 'pg_backups/'
        ## Localizar el archivo .cfg que contiene la información deseada
        #bkps_file = os.path.join(parent_dir, bkps_folder)
        bkps_file = '/opt/backups/pg_backups/'
        return bkps_file

    @staticmethod
    def default_cfg_path(subpath):
        '''
    Objetivo:
        - devuelve la ruta por defecto donde debe estar el archivo de
        configuración en caso de que no se indique una ruta mediante el comando
        -c en la llamada al programa desde consola.
    Parámetros:
        - subpath: el nombre del archivo de configuración por defecto, que
        podrá tener diversos nombres según la operación que se esté llevando a
        cabo, y la carpeta que lo contiene.
    Devolución:
        - la ruta absoluta que debe tener el archivo de configuración por
        defecto.
    '''
        # Obtener el directorio donde se encuentra este script
        script_dir = os.path.dirname(os.path.realpath(__file__))
        # Localizar el archivo .cfg que contiene la información deseada
        parent_dir = os.path.abspath(os.path.join(script_dir, os.pardir))
        cfg_folder = 'config/' + subpath
        cfg_file = os.path.join(parent_dir, cfg_folder)
        return cfg_file

    @staticmethod
    def sorted_flist(path):
        '''
    Objetivo:
        - genera una lista en la que se ordena descendentemente por fecha de
        modificación los archivos que se encuentran en el directorio o ruta
        especificados.
    Parámetros:
        - path: la ruta o directorio donde se encuentran los archivos que se
        desean ordenar.
    Devolución:
        - una lista con los archivos ordenados.
    '''
        #mtime = lambda f: os.stat(os.path.join(path, f)).st_mtime
        #return list(sorted(os.listdir(path), key=mtime))
        files_list = []
        for dirname, dirnames, filenames in os.walk(path):
            for file in filenames:
                filepath = os.path.realpath(os.path.join(dirname, file))
                files_list.append(filepath)
        sorted_list = sorted(files_list, key=lambda f: os.stat(f).st_mtime)
        return sorted_list

    @staticmethod
    def get_dbs_bkped(bkps_list=[]):
        '''
    Objetivo:
        - extrae los nombres de las bases de datos que tienen un backup de la
        lista con los archivos de backups que recibe. Genera una lista con el
        resultado obtenido.
    Parámetros:
        - bkps_list: una lista de archivos de backups.
    Devolución:
        - una lista con los nombres de las bases de datos que tienen un backup
        en la lista que se pasó por parámetro.
    '''
        bkped_dbs = []  # De momento no hay ninguna base de datos con backup
        # Declarar la expresión regular que detecta si el nombre del archivo
        # de backup se corresponde con una copia generada por el programa
        # dump.py
        regex = r'(.*)?db_(.+)_(\d{8}_\d{6}_.+)\.(?:dump|bz2|gz|zip)$'
        regex = re.compile(regex)  # Validar la expresión regular
        for f in bkps_list:  # Para cada archivo de la lista...
            # Si su nombre sigue el patrón de dump.py...
            filename = os.path.basename(f)
            if re.match(regex, filename):
                # Extraer las partes del nombre ([prefix], dbname, date)
                parts = regex.search(filename).groups()
                # Si el nombre de la BD no está en la lista de BDs con backup,
                # se añade (si está, no se añade, para evitar nombres
                # repetidos)
                if parts[1] not in bkped_dbs:
                    # Añadir nombre de BD a la lista
                    bkped_dbs.append(parts[1])
            # Si el archivo no es un backup o no cumple el patrón dump.py...
            else:
                continue  # Se ignora...
        return bkped_dbs  # Devolver la lista de BDs que tienen copia

    @staticmethod
    def show_pg_warnings(pg_dbs=[], bkped_dbs=[], logger=None):  # CORREGIR ESTO: LOS MENSAJES ACABAN EN COMA; NO EN PUNTO
        '''
    Objetivo:
        - advertir de las bases de datos que actualmente existen en PostgreSQL
        y que no tienen una copia de seguridad y de las copias de seguridad de
        bases de datos que no existen en PostgreSQL.
    Parámetros:
        - logger: el logger que se empleará para mostrar y registrar el
        mensaje.
        - pg_dbs: las bases de datos que hay en PostgreSQL.
        - bkped_dbs: las bases de datos que tienen una copia de seguridad.
    '''
        if not logger:
            logger = Logger()
        show_msg = False
        message = 'Las siguientes bases de datos almacenadas en PostgreSQL ' \
                  'no tienen copias de seguridad en el directorio ' \
                  'especificado en el archivo de configuración: '
        for dbname in pg_dbs:  # Para cada BD en PostgreSQL...
            if dbname not in bkped_dbs:  # Si no está entre las BDs con copia..
                show_msg = True
                if dbname is pg_dbs[-1]:
                    message += '"{}".'.format(dbname)
                    break
                message += '"{}", '.format(dbname)
        if show_msg:
            logger.highlight('warning', message, 'purple', effect='bold')

        show_msg = False
        message = 'Las siguientes bases de datos tienen copias de seguridad ' \
                  'pero no existen en PostgreSQL: '
        for dbname in bkped_dbs:  # Para cada BD con copia...
            # Si no está entre las BDs de PostgreSQL...
            if dbname not in pg_dbs:
                show_msg = True
                if dbname is bkped_dbs[-1]:
                    message += '"{}".'.format(dbname)
                    break
                message += '"{}", '.format(dbname)
        if show_msg:
            logger.highlight('warning', message, 'purple', effect='bold')

    @staticmethod
    def get_files_tsize(files_list=[]):
        '''
    Objetivo:
        - devuelve el tamaño total en disco del conjunto de archivos que
        componen la lista obtenida por parámetro.
    Parámetros:
        - files_list: la lista con el conjunto de archivos del que se desea
        calcular el tamaño en disco.
    Devolución:
        - el tamaño en disco del conjuntos de archivos que componen la lista.
    '''
        tsize = 0  # Inicializar tamaño a 0 bytes
        for f in files_list:  # Para cada archivo de la lista...
            file_info = os.stat(f)  # Almacenar información del archivo
            # Añadir el tamaño del archivo al tamaño total
            tsize += file_info.st_size
        return tsize  # Devolver tamaño total de la lista de archivos

    @staticmethod
    def remove_empty_dir(path):
        try:
            os.rmdir(path)
        except OSError:
            pass

    @staticmethod
    def remove_empty_dirs(path):
        for root, dirnames, filenames in os.walk(path, topdown=False):
            for dirname in dirnames:
                Dir.remove_empty_dir(os.path.realpath(os.path.join(root,
                                                                   dirname)))
