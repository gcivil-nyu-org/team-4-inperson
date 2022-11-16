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

PATH_TO_LOGS_FOLDER = BASE_DIR.parent / "logs"

class PackagePathFilter(logging.Filter):
    def filter(self, record):
        pathname = record.pathname
        record.relativepath = None
        abs_sys_paths = map(os.path.abspath, sys.path)
        for path in sorted(abs_sys_paths, key=len, reverse=True):
            if not path.endswith(os.sep):
                path += os.sep
            if pathname.startswith(path):
                record.relativepath = os.path.relpath(pathname, path)
                break
        return True

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {
        "filter_path": {
            "()": PackagePathFilter,
        },
    },
    "formatters": {
        "verbose": {"format": "[%(asctime)s] [%(levelname)s] [%(relativepath)s:%(lineno)d] %(message)s"}
    },
    "handlers": {
        "debug1": {
            "level": "DEBUG",
            "class": "logging.FileHandler",
            "filename": str(PATH_TO_LOGS_FOLDER) + "/django.log",
            "formatter": "verbose",
            "filters": ["filter_path"],
        },
    },
    "loggers": {
        "project": {
            "handlers": ["debug1"],
            "level": "DEBUG",
            "propagate": True,
        },
    },
}

SITE_ID = 3

ACCOUNT_SIGNUP_REDIRECT_URL = "/register"
LOGIN_REDIRECT_URL = "/"

# SMTP Configuration

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = "ratenyuteam@gmail.com"
EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD")
