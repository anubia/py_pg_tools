#!/usr/bin/env python3
# -*- encoding: utf-8 -*-


# ************************* DEFINICIÓN DE FUNCIONES *************************

def is_pg_superuser(cursor):
    '''
Objetivo:
    - comprobar si el usuario actualmente conectado a PostgreSQL es
    superusuario.
Parámetros:
    - cursor: cursor de la conexión para permitir realizar operaciones y
    consultas a las bases de datos de PostgreSQL.
Devolución:
    - un booleano, True si la conexión establecida es como superusuario, False
    de lo contrario.
'''
    query_is_superuser = (
        'SELECT usesuper '
        'FROM pg_user '
        'WHERE usename = CURRENT_USER;'
    )
    cursor.execute(query_is_superuser)
    row = cursor.fetchone()
    return(row[0])


def get_cursor_dbs(cursor, ex_templates=True, db_owner=''):
    '''
Objetivo:
    - realizar una consulta a PostgreSQL para devolver un cursor que contiene
    la lista de bases de datos correspondiente a los parámetros del archivo de
    configuración.
Parámetros:
    - cursor: cursor de la conexión para permitir realizar operaciones y
    consultas a las bases de datos de PostgreSQL.
    - ex_templates: indica si se deben ignorar las bases de datos que sean
    plantillas en PostgreSQL.
    - db_owner: indica el propietario que deben tener las bases de datos que se
    desean obtener. Si el propietario es nulo, se obtienen todas las bases de
    datos que hay en PostgreSQL.
Devolución:
    - un booleano, True si la conexión establecida es como superusuario, False
    de lo contrario.
'''
    query_get_dbs = (
        'SELECT d.datname, d.datallowconn, '
        'pg_catalog.pg_get_userbyid(d.datdba) '
        'FROM pg_catalog.pg_database d;'
    )
    query_get_no_template_dbs = (
        'SELECT d.datname, d.datallowconn, '
        'pg_catalog.pg_get_userbyid(d.datdba) '
        'FROM pg_catalog.pg_database d '
        'WHERE not datistemplate;'
    )
    query_get_owner_dbs = (
        'SELECT d.datname, d.datallowconn, '
        'pg_catalog.pg_get_userbyid(d.datdba) '
        'FROM pg_catalog.pg_database d '
        'WHERE pg_catalog.pg_get_userbyid(d.datdba) = (%s);'
    )
    query_get_no_template_owner_dbs = (
        'SELECT d.datname, d.datallowconn, '
        'pg_catalog.pg_get_userbyid(d.datdba) '
        'FROM pg_catalog.pg_database d '
        'WHERE not datistemplate '
        'AND pg_catalog.pg_get_userbyid(d.datdba) = (%s);'
    )

    # Obtener todas BDs (que no sean templates) de un propietario concreto
    if db_owner and ex_templates:
        cursor.execute(query_get_no_template_owner_dbs, (db_owner, ))
    # Obtener todas BDs (templates incluidas) de un propietario concreto
    elif db_owner and not ex_templates:
        cursor.execute(query_get_owner_dbs, (db_owner, ))
    # Obtener todas BDs (que no sean templates) de PostgreSQL
    elif not db_owner and ex_templates:
        cursor.execute(query_get_no_template_dbs)
    else:  # Obtener todas BDs (templates incluidas) de PostgreSQL
        cursor.execute(query_get_dbs)
    return cursor  # Devolver el cursor con el resultado de la consulta


def allow_db_conn(conn, cursor, dbname):
    '''
Objetivo:
    - habilitar las conexiones a una base de datos determinada.
Parámetros:
    - conn: conexión realizada desde el script a PostgreSQL
    - cursor: cursor de la conexión para permitir realizar operaciones y
    consultas a las bases de datos de PostgreSQL.
    - dbname: el nombre de la base de datos a la que se modifica su atributo
    "datallowconn" para habilitar conexiones.
'''
    query_db_allow_conn = (
        'UPDATE pg_database '
        'SET datallowconn = TRUE '
        'WHERE datname = (%s)', (dbname, )
    )
    # Habilitar conexiones para esta base de datos
    cursor.execute(query_db_allow_conn)
    conn.commit()  # Hacer los cambios permanentes


def disallow_db_conn(conn, cursor, dbname):
    '''
Objetivo:
    - deshabilitar las conexiones a una base de datos determinada.
Parámetros:
    - conn: conexión realizada desde el script a PostgreSQL
    - cursor: cursor de la conexión para permitir realizar operaciones y
    consultas a las bases de datos de PostgreSQL.
    - dbname: el nombre de la base de datos a la que se modifica su atributo
    "datallowconn" para deshabilitar conexiones.
'''
    query_db_disallow_conn = (
        'UPDATE pg_database '
        'SET datallowconn = FALSE '
        'WHERE datname = (%s)', (dbname, )
    )
    cursor.execute(query_db_disallow_conn)
    # Deshabilitar conexiones para esta base de datos
    conn.commit()  # Hacer los cambios permanentes
