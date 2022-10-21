from .base import *

if 'RDS_DB_NAME' in os.environ:
    ALLOWED_HOSTS = ['ratenyu-dev.eba-apngxcqy.us-east-1.elasticbeanstalk.com']
    DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.postgresql_psycopg2',
                'NAME': os.environ['RDS_DB_NAME'],
                'USER': os.environ['RDS_USERNAME'],
                'PASSWORD': os.environ['RDS_PASSWORD'],
                'HOST': os.environ['RDS_HOSTNAME'],
                'PORT': os.environ['RDS_PORT'],
            }
    }
    STATICFILES_DIRS = []
    STATIC_ROOT = 'static'
