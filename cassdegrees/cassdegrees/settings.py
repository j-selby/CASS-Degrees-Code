"""
Django settings for cassdegrees project.

Generated by 'django-admin startproject' using Django 2.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# Please generate at least 16 character long random string with special characters and numbers
# in the /etc/secret_key.txt file before running (create one before proceeding).
with open('/etc/secret_key.txt') as f:
    SECRET_KEY = f.read().strip()

# When username and password for the PSQL database is being set, please update them here or db connection will fail.
# Also, for better security purposes, please configure your PSQL to only allow local connections (i.e. 127.0.0.1).
psql_username = ""
psql_password = ""

if psql_username == "" or psql_password == "":
    raise NotImplementedError("Please configure your PSQL database username and password!")

# https://docs.djangoproject.com/en/2.2/ref/settings/#std:setting-STATIC_ROOT
STATIC_ROOT = ""

if STATIC_ROOT == "":
    raise NotImplementedError("Please specify STATIC_ROOT in settings.py before proceeding.")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# Please configure ALLOWED_HOSTS before deployment.
# Look at https://docs.djangoproject.com/en/2.2/ref/settings/#std:setting-ALLOWED_HOSTS for more information.
ALLOWED_HOSTS = [

]


# Application definition

INSTALLED_APPS = [
    'api',  # our API app
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.postgres',  # added this for our postgresql database
    'django.contrib.staticfiles',
    'rest_framework',  # added this for the REST framework
    'ui',  # our UI app
    'corsheaders',  # for api call in multiselect
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'cassdegrees.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates').replace('\\', '/')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'cassdegrees.wsgi.application'

REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    )
}

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    # 'default': {
    #     'ENGINE': 'django.db.backends.sqlite3',
    #     'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    # }
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'cassdegrees',
        'USER': psql_username,
        'PASSWORD': psql_password,
        'HOST': 'localhost',
        'PORT': '5432',
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {'min_length': 10}
    },
    {
        'NAME': 'api.Validators.ANUValidator'
    },
]


# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Australia/Sydney'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/static/'

# Todo: check on consistency with Allowed Hosts before final deployment
# https://www.youtube.com/watch?v=OIbndrrUYiY
CORS_ORIGIN_WHITELIST = 'http://localhost:8000', 'http://127.0.0.1:8000',

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]

LOGIN_REDIRECT_URL = '/'

# Default value of 1000 restricted the ability to delete courses en masse.
DATA_UPLOAD_MAX_NUMBER_FIELDS = 2147483647
