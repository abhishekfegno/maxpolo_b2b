"""
Django settings for maxpolob2b project.

Generated by 'django-admin startproject' using Django 4.0.2.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""
import os

from django.urls import reverse_lazy
from dotenv import load_dotenv

load_dotenv()
env = os.environ.get
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-b0u)v=*cyp-+kpl-=04+uf@=z@k!^d$mo9f&gvf7$%xf$bqa04'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['maxpolob2b.dev.fegno.com', 'www.maxpolob2b.dev.fegno.com', 'localhost']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'django.contrib.gis',

    'django.contrib.sites',
    'django.contrib.flatpages',

    'apps.user',
    'apps.infrastructure',
    'apps.catalogue',
    'apps.order',
    'apps.executivetracking',
    'apps.payment',
    'apps.notification',

    'dg',
    'django_extensions',
    'rest_framework',
    'rest_auth',
    'rest_framework.authtoken',
    'django_filters',
    'crispy_forms',
    'debug_toolbar',
    'import_export',
    'rest_framework_gis',
    'chartjs',


]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

]
INTERNAL_IPS = [
    # ...
    "127.0.0.1",
    # ...
]

DEBUG_TOOLBAR_PANELS = [
    'debug_toolbar.panels.versions.VersionsPanel',
    'debug_toolbar.panels.timer.TimerPanel',
    'debug_toolbar.panels.settings.SettingsPanel',
    'debug_toolbar.panels.headers.HeadersPanel',
    'debug_toolbar.panels.request.RequestPanel',
    'debug_toolbar.panels.sql.SQLPanel',
    'debug_toolbar.panels.staticfiles.StaticFilesPanel',
    'debug_toolbar.panels.templates.TemplatesPanel',
    'debug_toolbar.panels.cache.CachePanel',
    'debug_toolbar.panels.signals.SignalsPanel',
    'debug_toolbar.panels.logging.LoggingPanel',
    'debug_toolbar.panels.redirects.RedirectsPanel',
]

ROOT_URLCONF = 'maxpolob2b.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['public/templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'apps.context_processors.settings',
            ],
            'libraries': {
                'templatetags': 'apps.templatetags',
            }
        },
    },
]

SITE_ID = 1

REST_FRAMEWORK = {

    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],

    # "DEFAULT_PERMISSION_CLASSES": [
        # 'rest_framework.permissions.IsAuthenticated',
    # ],

    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'django_filters.rest_framework.OrderingFilter',
    ],

    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ],
    # 'DEFAULT_PAGINATION_CLASS': 'lib.utils.PageNumberPagination',
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',

}
WSGI_APPLICATION = 'maxpolob2b.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }
DATABASES = {
    'default': {
        'ENGINE': os.environ.get('BB2B_DB_ENGINE', 'django.contrib.gis.db.backends.postgis'),
        'NAME': os.environ.get('BB2B_DB_NAME', 'buildwareb2b'),
        'USER': os.environ.get('BB2B_DB_USER', 'buildwareb2b'),
        'PASSWORD': os.environ.get('BB2B_DB_PASSWORD', 'password'),
        'HOST': os.environ.get('BB2B_DB_HOST', 'localhost'),
        'PORT': os.environ.get('BB2B_DB_PORT', '5432'),
    },
}
AUTH_USER_MODEL = 'user.User'

CRISPY_TEMPLATE_PACK = 'bootstrap4'

# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    # {
    #     'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    # },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    # },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    # },
]

# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kolkata'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

TOKEN_EXPIRED_AFTER_SECONDS = 300

LOGIN_REDIRECT_URL = 'index'
LOGIN_URL = 'login'
LOGOUT_REDIRECT_URL = 'login'
LOGOUT_URL = 'login'

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = "abhishekfegno@gmail.com"
EMAIL_HOST_PASSWORD = "abhishek@fegno123"

EMAIL_FILE_PATH = BASE_DIR / "sent_emails"

STATIC_URL = '/assets/'
MEDIA_URL = '/src/'

SITE_NAME = "MaxPolo Ceramics"

DEFAULT_IMAGE = 'default/image_not_found.jpg'

PLACEHOLDER_PROFILE_DEFAULT_IMAGE = 'images/Placeholder-Image.png'

STATIC_ROOT = os.path.join(BASE_DIR, 'public/staticfiles/')
MEDIA_ROOT = os.path.join(BASE_DIR, 'public/src/')

STATICFILES_DIRS = [os.path.join(BASE_DIR, 'public/static')]

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
LOGO = f'{STATIC_URL}company_logo.png'

BREAD_HOME = ('Home', reverse_lazy('index'))

BREAD = {
    'banners-list': [BREAD_HOME, ('Banners', reverse_lazy('banners-list'))],
    'user-list': [BREAD_HOME, ('Users', reverse_lazy('user-list'))],
    'quotation-list': [BREAD_HOME, ('Quotation', reverse_lazy('quotation-list'))],
    'salesorder-list': [BREAD_HOME, ('Sales Order', reverse_lazy('salesorder-list'))],
    'invoice-list': [BREAD_HOME, ('Invoice', reverse_lazy('invoice-list'))],
    'cancelled_order': [BREAD_HOME, ('Cancelled', reverse_lazy('cancelled_order'))],
    'transaction-list': [BREAD_HOME, ('Payments', reverse_lazy('transaction-list'))],
    'category-list': [BREAD_HOME, ('Category', reverse_lazy('category-list'))],
    'pdf-list': [BREAD_HOME, ('PDF', reverse_lazy('pdf-list'))],
    'brand-list': [BREAD_HOME, ('Brand', reverse_lazy('brand-list'))],
    'product-list': [BREAD_HOME, ('Product', reverse_lazy('product-list'))],
    'complaint-list': [BREAD_HOME, ('Claims', reverse_lazy('complaint-list'))],
    'branch-list': [BREAD_HOME, ('Branch', reverse_lazy('branch-list'))],
}
