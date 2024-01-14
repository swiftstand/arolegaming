"""
Django settings for drag4me project.

Generated by 'django-admin startproject' using Django 3.0.5.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = '=k1xc4g)g9b4s%161lr6llpauxxc8up4cbn$2z2j!$5g5%0*&0'
SECRET_KEY = os.getenv("SECRET_KEY", "=k1xc4g)g9b4s%161lr6llpauxxc8up4cbn$2z2j!$5g5%0*&0")


DEVELOPMENT_MODE = os.getenv("DEVELOPMENT", "True") == "True"

# SECURITY WARNING: don't run with debug turned on in production!
if DEVELOPMENT_MODE:
    DEBUG = True
else:
    DEBUG = False

ALLOWED_HOSTS = os.getenv("HOSTS", "*").split(",")


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken',
    'corsheaders',
    'storages',

    'event',
    'user',
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication'
    ],
    # 'DEFAULT_PAGINATION_CLASS' : 'rest_framework.pagination.PageNumberPagination',
    # 'PAGE_SIZE' : 2,
}


DEFAULT_FROM_EMAIL = os.environ.get('FROM_SENDER')
EMAIL_STARTTLS = True
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.privateemail.com'
EMAIL_HOST_USER = os.environ.get('MAIL_SENDER') 
EMAIL_HOST_PASSWORD = os.environ.get('SENDER_PASSWORD')
EMAIL_PORT = 465
EMAIL_USE_SSL = True
EMAIL_USE_TSL = False


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware'
]

ROOT_URLCONF = 'drag4me.urls'

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

WSGI_APPLICATION = 'drag4me.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

if os.environ.get("API_ENV", "dev") == "prd":
    db = {
    'ENGINE': "django.db.backends.postgresql",
    'NAME': os.environ['DATABASE_NAME'],
    'USER': os.environ['RDS_USERNAME'],
    'PASSWORD': os.environ['RDS_PASSWORD'],
    'HOST': os.environ["RDS_HOST"],
    'PORT': int(os.environ['RDS_PORT']),
    }      

else:
    db = {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }

DATABASES = {
    'default': db
}


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

# TIME_ZONE = 'UTC'

TIME_ZONE = 'Africa/Lagos'

USE_I18N = True

USE_L10N = True

# USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/
TEST = "https://arolegaming.pythonanywhere.com"
LOCAL =  "http://192.168.56.56:8000"
PROD = "https://arole-playstation-center.onrender.com"
MY_SITE = PROD

LOGIN_REDIRECT_URL= 'index'
LOGIN_URL = 'login'

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
# MEDIA_URL = '{}/media/'.format(MY_SITE)
MEDIA_URL = '/media/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL= 'user.User'

CORS_ORIGIN_ALLOW_ALL = True

PUBLIC_KEY = os.environ.get('paystack_public', "FLWPUBK_TEST-60c00b51d6cf9dd5f372c47e9efc8587-X")
SECRET_KEY = os.environ.get('paystack_secret', "FLWSECK_TEST-c08f710bd7097c8e3f22bf6a3dacab68-X")

HASH_ENC = os.environ.get("pay_hash", "FLWSECK_TEST7080904cc8cf")

# PRD_SECRET = 

NUMBER_OF_TICKETS = 1000

TICKET_COST = 3000
