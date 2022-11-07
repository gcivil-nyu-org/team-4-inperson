from .base import *

if "RDS_DB_NAME" in os.environ:
    ALLOWED_HOSTS = ["ratenyu-dev.eba-apngxcqy.us-east-1.elasticbeanstalk.com"]
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql_psycopg2",
            "NAME": os.environ["RDS_DB_NAME"],
            "USER": os.environ["RDS_USERNAME"],
            "PASSWORD": os.environ["RDS_PASSWORD"],
            "HOST": os.environ["RDS_HOSTNAME"],
            "PORT": os.environ["RDS_PORT"],
        }
    }
    STATICFILES_DIRS = []
    STATIC_ROOT = "static"

PATH_TO_LOGS_FOLDER = "/logs"

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(asctime)s %(levelname)s %(filename)s %(message)s'
        }
    },
    'handlers': {
        'debug1': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': str(PATH_TO_LOGS_FOLDER) + '/django.log',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'project': {
            'handlers': ['debug1'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}
