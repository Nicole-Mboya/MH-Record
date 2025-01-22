"""
Django settings for MHRecord project.

Generated by 'django-admin startproject' using Django 5.1.4.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from pathlib import Path
from datetime import timedelta

import environ
import os
from django.shortcuts import render


# Initialize environment variables
env = environ.Env()
environ.Env.read_env()  # Read .env file

# SECRET_KEY from environment variable or fallback to a default
SECRET_KEY = env('DJANGO_SECRET_KEY', default='default-insecure-secret-key')


import os

# Base directory for the project
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Static files settings
STATIC_URL = '/static/'

# For development, if you're serving static files from the frontend React app (during dev):
STATICFILES_DIRS = [os.path.join(BASE_DIR, './frontend/build/static')]

# For production, you'll collect static files into a folder for serving
STATIC_ROOT = os.path.join(BASE_DIR, 'static')



# Build paths inside the project like this: BASE_DIR / 'subdir'

def index(request):
    # Serve the built React index.html file
    return render(request, 'frontend/build/index.html')


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [
    '127.0.0.1' , 'localhost',
]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Optional but recommended
    'django.contrib.sites',
    'django.contrib.humanize',
    'corsheaders',
    # Third-party apps
    'rest_framework',          # Django REST Framework
    'crispy_forms',            # Enhanced form rendering
    'django_extensions',       # Extended management commands

    # Your apps
    'Record',                   # Your custom app
]



# settings.py

SESSION_ENGINE = 'django.contrib.sessions.backends.db'
SESSION_COOKIE_AGE = 3600  # Session duration in seconds (1 hour)
SESSION_EXPIRE_AT_BROWSER_CLOSE = False  # Optional: session expires when browser is closed
SESSION_COOKIE_SECURE = False  # Set to True if using HTTPS in production



MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # CORS middleware must be placed first
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',  # For authentication management
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]




ROOT_URLCONF = 'MHRecord.urls'

CORS_ALLOWED_ORIGINS = [
    'http://localhost:3000',  # Allow React development server
]

CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True  


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

WSGI_APPLICATION = 'MHRecord.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'mh_record',
        'USER': 'root',
        'PASSWORD': 'Luvchild254#',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/



# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# JWT Authentication settings (use if you are using simplejwt)

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
    ],
}


# JWT Configuration (optional, if using JWT)

