from .common import *

# 실습을 위한 임시 설정, TODO: False로 변경해야 한다.
DEBUG = os.environ.get("DEBUG") in ["1", "t", "true", "T", "True"]

# Debug가 True일 때에는 localhost가 자동으로 포함된다.
ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "").split(",")

STATICFILES_STORAGE = "backend.storages.StaticAzureStorage"  # STATIC
DEFAULT_FILE_STORAGE = "backend.storages.MediaAzureStorage"  # MEDIA

# django-environ 라이브러리를 활용하여 환경변수를 관리할 수도 있다고 한다.
AZURE_ACCOUNT_NAME = os.environ["AZURE_ACCOUNT_NAME"]  # storage account name
AZURE_ACCOUNT_KEY = os.environ["AZURE_ACCOUNT_KEY"]  # storage account key

# CORS 설정
CORS_ORIGIN_WHITELIST = os.environ.get("CORS_ORIGIN_WHITELIST", "").split(",")

# DATABASE 설정
DATABASES = {
    "default": {
        "ENGINE": os.environ.get("DB_ENGINE", "django.db.backends.postgresql"),
        "HOST": os.environ["DB_HOST"],
        "USER": os.environ["DB_USER"],
        "PASSWORD": os.environ["DB_PASSWORD"],
        "NAME": os.environ.get("DB_NAME", "postgres"),
    }
}

# SENTRY 서비스를 활용하면 여러 서버의 로그를 정리하여 확인할 수 있다고 한다.
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {"console": {"level": "ERROR", "class": "logging.StreamHandler"}},
    "loggers": {"django": {"handlers": ["console"], "level": "ERROR"}},
}
