"""
Django settings for thelix project.
"""

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
SECRET_KEY = 'django-insecure-wnx+#tn3lti*sz@3un)lrl-i6d*ilfzkg##z1&ip@gpgmt8f$4'

DEBUG = False

ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'himawatkhandavastu.com', 'www.himawatkhandavastu.com', '*']

# CSRF Trusted Origins
CSRF_TRUSTED_ORIGINS = [
    'https://himawatkhandavastu.com',
    'https://www.himawatkhandavastu.com',
    'http://himawatkhandavastu.com',
    'http://www.himawatkhandavastu.com',
    'http://localhost:8000',
    'http://127.0.0.1:8000',
]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',

    # Third-party apps
    'django_cleanup.apps.CleanupConfig',

    # Local apps
    'accounts',
    'dashboard',
    'pages',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # Add cache control middleware last (only active in DEBUG mode)
    'himwat.middleware.DisableBrowserCachingMiddleware',
]

ROOT_URLCONF = 'himwat.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'pages.context_processors.site_context',
                'pages.context_processors.page_context',
            ],
        },
    },
]

WSGI_APPLICATION = 'himwat.wsgi.application'


if DEBUG:
# Database
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'himawat1_cms',  # The name of the database you created in MySQL
            'USER': 'himawat1_cms',  # Your MySQL username (e.g., 'root')
            'PASSWORD': 'd4CXWYzFEESYeYUuXS4w',  # Your MySQL password
            'HOST': '127.0.0.1',  # Use 'localhost' or '127.0.0.1'
            'PORT': '3306',  # Default MySQL port
            'OPTIONS': {
                'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
                'charset': 'utf8mb4',
            },
        }
    }


# Password validation
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
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kathmandu'
USE_I18N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Custom user model
AUTH_USER_MODEL = 'accounts.User'

# Login settings
LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/dashboard/'
LOGOUT_REDIRECT_URL = '/'

# Site settings
SITE_NAME = 'Himwatkhanda Vastu Pvt. Ltd.'
SITE_DESCRIPTION = 'Your Blueprint for Harmony, Structure, and Expertise'
SITE_URL = 'https://himawatkhandavastu.com'


# Cache settings - Disabled in development
if DEBUG:
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
        }
    }
else:
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        }
    }

# Template caching - Disabled in development
# When DEBUG is False, cached loaders will be used for better performance
if not DEBUG:
    TEMPLATES[0]['OPTIONS']['loaders'] = [
        ('django.template.loaders.cached.Loader', (
            'django.template.loaders.filesystem.Loader',
            'django.template.loaders.app_directories.Loader',
        ))
    ]
