"""
Django settings for event_meet project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG')

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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


# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Allow all host headers
ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_eventbrite',
    'django_twilio',
    'circly',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'event_meet.urls'

WSGI_APPLICATION = 'event_meet.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases
# Parse database configuration from $DATABASE_URL
import dj_database_url

DATABASES = {'default': dj_database_url.config(default=os.environ.get('DATABASE_URL'))}


EMAIL_HOST = os.environ.get('EMAIL_HOST_VAR')
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER_VAR')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD_VAR')
EMAIL_PORT = os.environ.get('EMAIL_PORT_VAR')
EMAIL_USE_TLS = True

BITLY_SECRET_KEY = os.environ.get('BITLY_SECRET_VAR')
BITLY_CLIENT_ID = os.environ.get('BITLY_CLIENT_ID_VAR')
BITLY_ACCESS_TOKEN = os.environ.get('BITLY_ACCESS_TOKEN_VAR')
BITLY_LOGIN = os.environ.get('BITLY_LOGIN_VAR')

CIRCLE_MAX_SIZE = 8
CIRCLE_MIN_SIZE = 4

circle_count = CIRCLE_MAX_SIZE
range_str = ""

while circle_count != 1:
    range_str = range_str + str(circle_count)
    circle_count = circle_count - 1

# Reverse the string of numbers
CONTACT_RANGE_STR = range_str[::-1]


# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/New_York'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static asset configuration
# Static files (CSS, JavaScript, Images)
#STATIC_ROOT = os.path.join(BASE_DIR, "static")
STATIC_URL = '/static/'
STATIC_ROOT = '/event_meet/event_meet/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
    '/event_meet/static/',
)
