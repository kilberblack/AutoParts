"""
Django settings for AutoParts project.

Generated by 'django-admin startproject' using Django 5.2.1.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.2/ref/settings/
"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

AUTH_USER_MODEL = 'api.Usuario'

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-_4adan$s&nbx&+6q@gk2eo-goija6#9p)g5_p@#zr%yzmqkc(+'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

STATIC_URL = '/static/'

STATIC_ROOT = BASE_DIR / 'staticfiles'
# Application definition

INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'frontend',
    'api',
]

JAZZMIN_SETTINGS = {
    "site_title": "AutoParts Admin",
    "site_header": "Panel de Administración de AutoParts",
    "site_brand": "AutoParts",
    "welcome_sign": "Bienvenido al Panel de AutoParts",
    "copyright": "AutoParts",
    "show_sidebar": True,
    "navigation_expanded": True,
    "hide_apps": ["auth", "contenttypes", "sessions", "messages", "staticfiles"],
    "hide_models": ["api.CarritoItem", "api.PedidoItem"],

    "order_with_respect_to": [
        "api.Pedido",
        "api.Carrito",
        "api.ClienteDistribuidor",
        "api.Producto",
        "api.Usuario",
        "api.LogEntryProxy",
    ],

    "topmenu_links": [
        {"name": "Volver a la pagina", "url": "/", "permissions": ["auth.view_user"]},
    ],


    "icons": {
        "api.Pedido": "fas fa-box",
        "api.Carrito": "fas fa-shopping-basket",
        "api.ClienteDistribuidor": "fas fa-user-friends",
        "api.Producto": "fas fa-cube",
        "api.Usuario": "fas fa-user",
        "api.LogEntryProxy": "fas fa-file-alt",
    },

    "related_modal_active": True, 
    "use_google_fonts_cdn": True,
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'AutoParts.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'AutoParts.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.2/topics/i18n/

TIME_ZONE = 'America/Santiago'

LANGUAGE_CODE = 'es-ar'

USE_I18N = True
USE_L10N = True
USE_TZ = True

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

TRANSBANK_API_URL = "https://webpay3gint.transbank.cl"
TRANSBANK_COMMERCE_CODE = "597055555532"  
TRANSBANK_API_KEY = "579B532A7440BB0C9079DED94D31EA1615BACEB56610332264630D42D0A36B1C"  
TRANSBANK_ENVIRONMENT = 'TEST'  


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
