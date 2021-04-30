"""
Django settings for locallibrary project.

Generated by 'django-admin startproject' using Django 3.1.2.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

from pathlib import Path

import environ
# reading .env file
try:
    environ.Env.read_env()
except:
    print('Ignoring .env file...')

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
import os
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'cg#p$g+j9tax!#a3cup@1$8obt2_+&k3q+pmu)5%asj6yjpkag')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Set hosts to allow any app on Heroku and the local testing URL
ALLOWED_HOSTS = ['*']

# Media files, uploaded by user
MEDIA_ROOT_LOCAL = os.path.join(BASE_DIR, 'media')
MEDIA_URL_LOCAL = '/media/'

# Application definition

INSTALLED_APPS = [
    'crispy_forms',
    'django.forms',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'catalog.apps.CatalogConfig', # This object was created for us in /catalog/apps.py
    'storages',
    's3direct',
    'NovelBlog',
    'djstripe',
    'star_ratings',
    'taggit'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'locallibrary.urls'

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

FORM_RENDERER = 'django.forms.renderers.TemplatesSetting'

WSGI_APPLICATION = 'locallibrary.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Redirect to home URL after login (Default redirects to /accounts/profile/)
LOGIN_REDIRECT_URL = '/'

# Add to test email:
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Heroku: Update database configuration from $DATABASE_URL.
import dj_database_url
db_from_env = dj_database_url.config(conn_max_age=500)
DATABASES['default'].update(db_from_env)

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/
# The absolute path to the directory where collectstatic will collect static files for deployment.
STATIC_ROOT = BASE_DIR / 'staticfiles'  #. os.path.join(BASE_DIR, 'staticfiles')

# The URL to use when referring to static files (where they will be served from)
STATIC_URL = '/static/'

# Static file serving with AWS.
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID', '')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY', '')
AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME', '')
AWS_S3_ENDPOINT_URL = os.environ.get('AWS_S3_ENDPOINT_URL', '')
AWS_S3_REGION_NAME = os.environ.get('AWS_S3_REGION_NAME', '')

S3DIRECT_DESTINATIONS = {
    # Allow anybody to upload jpeg's and png's. Limit sizes to 5kb - 20mb
    'images': {
        'key': 'uploads/images',
        'auth': lambda u: True,
        'allowed': [
            'image/jpeg',
            'image/png'
        ],
        'content_length_range': (5000, 20000000),
        'allow_existence_optimization': True
    },

    # Allow authenticated users to upload mp4's
    'videos': {
        'key': 'uploads/videos',
        'auth': lambda u: True,#u.is_authenticated,
        'allowed': ['video/mp4']
    },
}

CRISPY_TEMPLATE_PACK = 'bootstrap4'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'novelpublichealthunc@gmail.com'
EMAIL_HOST_PASSWORD = os.environ.get('NOVEL_GMAIL_PASSWORD')
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False

STRIPE_LIVE_MODE = False  # Change to True in production
STRIPE_TEST_PUBLIC_KEY = os.environ.get('STRIPE_TEST_PUBLIC_KEY', 'pk_test_51IgJISLTF5lDg6OomxJ6O9xeztdzfrRQbU2fjMjVnECuzuuSluuLQS9wVZiJYBMqsgHsUxygx4mLaLJR5tItL6kJ00XI8ZFyyz')
STRIPE_TEST_SECRET_KEY = os.environ.get('STRIPE_TEST_SECRET_KEY', 'sk_test_51IgJISLTF5lDg6Ooh5OUF2dqZq6KDHMjlHAHhJwxpDdGgqqaX1767krbRdXbqa3tAMXg6haeaPxiHlxbCU4QOPTf00XSXluXoC')
STRIPE_LIVE_PUBLIC_KEY = '' #todo - activate account. Should look similar to the above. Place these new variables in the .env file as well.
STRIPE_LIVE_SECRET_KEY = '' #todo

DJSTRIPE_WEBHOOK_SECRET = os.environ.get('DJSTRIPE_WEBHOOK_SECRET', 'whsec_7PdcaUNOxl49pN8MlSrl5iEAPMtDBjty')
DJSTRIPE_USE_NATIVE_JSONFIELD = True
DJSTRIPE_FOREIGN_KEY_TO_FIELD = "id"

# Rating star system
STAR_RATINGS_STAR_WIDTH = 24
STAR_RATINGS_STAR_HEIGHT = 24
STAR_RATINGS_RANGE = 5
STAR_RATINGS_ANONYMOUS = False
STAR_RATINGS_STAR_SPRITE = 'images/stars.png'