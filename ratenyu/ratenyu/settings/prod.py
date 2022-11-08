from .base import *

if "RDS_DB_NAME" in os.environ:
    DEBUG = False
    ALLOWED_HOSTS = [
        "ratenyu.eba-apngxcqy.us-east-1.elasticbeanstalk.com",
        "ratenyu.com",
    ]
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

PATH_TO_LOGS_FOLDER = BASE_DIR.parent / "logs"

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
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': str(PATH_TO_LOGS_FOLDER) + '/django.log',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'project': {
            'handlers': ['debug1'],
            'level': 'ERROR',
            'propagate': True,
        },
    },
}

SITE_ID = 4

ACCOUNT_SIGNUP_REDIRECT_URL = "/register"
LOGIN_REDIRECT_URL = "/"

# SMTP Configuration

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'ratenyuteam@gmail.com'
EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD")
