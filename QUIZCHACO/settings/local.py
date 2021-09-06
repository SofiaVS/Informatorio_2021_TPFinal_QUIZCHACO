from .base import *

DEBUG = True

ALLOWED_HOSTS = []

#  DATABASES = {
    #'default': {
        #'ENGINE': 'sql_server.pyodbc',
        #'NAME': 'QUIZCHACO2',
        #'Trusted_Connection':'yes',
        #'HOST':'localhost\\SQLEXPRESS',
        #'OPTIONS':{
        	#'driver':'SQL Server Native Client 11.0',
        #}
    #}
#}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': str(os.path.join(BASE_DIR, "db2.sqlite3")),

    }
 }
