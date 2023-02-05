import os

from decouple import Csv
from pathlib import Path
from dotenv import load_dotenv, dotenv_values
from decouple import config
from dj_database_url import parse as dburl

print("Loading ENV variables..")
env_path = '/app/.env'
dotenv_conf = dotenv_values(env_path)
print(dotenv_conf)
load_dotenv(dotenv_path=env_path, verbose=True)

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=False, cast=bool)

ALLOWED_HOSTS = config('ALLOWED_HOSTS', default=['*'], cast=Csv())
SERVER_URL = config('SERVER_URL', default='http://localhost:8000')

# Application definition

INSTALLED_APPS = [
    'corsheaders',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.postgres',
    'client.register',
    'client.login',
    'client.consumer',
    'client.public',
    'client.company',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

AUTHENTICATION_BACKENDS = [
    'client.register.backends.SessionTokenAuthBackend',
    'django.contrib.auth.backends.ModelBackend', #valida o token no backend
    'client.register.backends.ActivationKeyAuthBackend',
]

ROOT_URLCONF = 'client.urls'

AUTH_USER_MODEL = 'register.User'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'client.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

#DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.sqlite3',
#        'NAME': BASE_DIR / 'db.sqlite3',
#    }
#}

DATABASES = {
     'default': {
         'ENGINE': 'django.db.backends.postgresql',
         'NAME': 'projetodev',
         'USER': 'projetodev',
         'PASSWORD': 'programacao75_full',
         'HOST': 'client-db',
         'PORT': '5432'
     }
 }

#default_dburl = 'sqlite:///' + os.path.join(BASE_DIR, 'db.sqlite3')
#
#DATABASES = {
#    'default': config('DATABASE_URL', default=default_dburl, cast=dburl),
#}


# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

CREDENCIAIS = {
        'client_id': config('DEV_CLIENT_KEY'),
        'client_secret': config('DEV_SECRET_KEY'),
        'sandbox': True,
        'certificate': 'client/credinciais/homologacao-436362-Verification-dev.pem'
    }


# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

#login

LOGIN_URL = '/login'

STAGING = config('STAGING', cast=bool, default=True)
