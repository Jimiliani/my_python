import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'wnmi1q*o6zqe57y^dm&kp2cb&#691xamv$#+d+996)f(2n1889'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'greenleaf',
        'USER': 'greenleaf_admin',
        'PASSWORD': 'greenleaf_admin',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}


STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static')
]
