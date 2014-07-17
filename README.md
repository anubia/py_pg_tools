
PY_PG_TOOLS:

    A powerful tool to use PostgreSQL in an easier and faster way. It allows
    the possibility to:

    - Change the owner of a database and all of its tables.
    - Make a custom backup of a PostgreSQL database or a whole cluster.
    - Delete a PostgreSQL database.
    - Get some information about some PostgreSQL databases, users or its
      current active connections.
    - Clone a PostgreSQL database.
    - Restore a database or cluster's backup in PostgreSQL.
    - Add to, delete or get some instructions from the user's crontab file, to
      execute automatically the program in a specific date and time.
    - Terminate some connections to PostgreSQL.
    - Delete a group of backups depending on a very customizable options.
    - Vacuum some PostgreSQL databases.

    See more information about py_pg_tools and its modules' characteristics
    letters specifying the argument -h or --help in console. For example
    (supposing you are in the same directory of py_pg_tools.py):

    - python3 py_pg_tools.py -h

    If you want to see more information about a specific module, write its
    characteristic letter and then the argument -h or --help. For example,
    in case you need information about how to make a backup (supposing you are
    in the same directory of py_pg_tools.py):

    - python3 py_pg_tools.py B -h

IMPORTED PACKAGES:

    python3 (v >= 3.2) (aptitude)
    python-crontab (v == 1.8) (pip)
    python3-dateutil (v >= 2.0) (aptitude)
    python3-psycopg2 (v >= 2.4.5) (aptitude)
    netifaces (v >= 0.10.4) (pip3)

INSTALLATION:

    This program only runs in Linux OS. Check you do the next steps:

    - Install the package python3.
    - Install the package python3-psycopg2.
    - Install the package python3-dateutil.
    - Install the package python-crontab (exactly version 1.8). This one is
      bound to be installed in python2.x directories. Look for the cronlog.py
      and crontab.py files in your Linux OS. If they are in a python2.x
      directory, make a symbolic link to each one in the python3.x counterpart
      directory.
    - Install the package netifaces. This one has to be installed via pip3. If
      Ubuntu version is older than 13.04, python3-pip (pip3) will not be
      available to install. To manage this, install python3-setuptools with
      aptitude and then pip with easy_install3 (sudo easy_install3 pip). Now,
      pip3 will be available. Make sure you have installed python3-dev before
      installing netifaces with pip3 (install it via aptitude if you have not).

USAGE:

    - Open a terminal.
    - Go to the directory where you have the py_pg_tools.py file.
    - Execute the command:

      python3 py_pg_tools.py ...

      Where ... are your specified arguments.
