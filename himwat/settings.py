"""
Django settings for Himwatkhanda Vastu project.
"""

from pathlib import Path
import os
from dotenv import load_dotenv

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# =============================================================================
# CONDITIONAL ENV FILE LOADING
# =============================================================================

# Determine which .env file to load based on DEBUG environment variable
# If DEBUG is not set, default to True (development mode)
debug_env_value = True

# Load the appropriate .env file based on DEBUG setting
if debug_env_value:
    # Development mode - load .env-local
    env_file = BASE_DIR / '.env-local'
    if env_file.exists():
        load_dotenv(env_file)
        print(f"[DEBUG MODE] Loaded environment variables from .env-local")
    else:
        # Fallback to .env if .env-local doesn't exist
        load_dotenv()
        print(f"[DEBUG MODE] .env-local not found, using .env")
else:
    # Production mode - load .env
    env_file = BASE_DIR / '.env'
    if env_file.exists():
        load_dotenv(env_file)
        print(f"[PRODUCTION MODE] Loaded environment variables from .env")
    else:
        raise FileNotFoundError(
            "Production .env file not found! Please create a .env file with production settings."
        )


# =============================================================================
# SECURITY SETTINGS
# =============================================================================

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')
if not SECRET_KEY:
    raise ValueError("DJANGO_SECRET_KEY environment variable is not set!")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG', 'True').lower() in ('true', '1', 'yes', 'on')

# Allowed hosts - configured via environment variable
ALLOWED_HOSTS_STR = os.environ.get('ALLOWED_HOSTS', 'localhost,127.0.0.1')
ALLOWED_HOSTS = [host.strip() for host in ALLOWED_HOSTS_STR.split(',') if host.strip()]

# CSRF Trusted Origins
CSRF_TRUSTED_ORIGINS_STR = os.environ.get('CSRF_TRUSTED_ORIGINS', '')
CSRF_TRUSTED_ORIGINS = [origin.strip() for origin in CSRF_TRUSTED_ORIGINS_STR.split(',') if origin.strip()]
if not CSRF_TRUSTED_ORIGINS and not DEBUG:
    # Fallback for production if not explicitly set
    CSRF_TRUSTED_ORIGINS = [f"https://{host}" for host in ALLOWED_HOSTS if not host.startswith(('localhost', '127.0.0.1', '*'))]

# Security Headers (HTTPS only in production)
if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SECURE_HSTS_SECONDS = 31536000  # 1 year
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_BROWSER_XSS_FILTER = True
    X_FRAME_OPTIONS = 'DENY'
    SECURE_REFERRER_POLICY = 'strict-origin-when-cross-origin'
    
    # If behind a proxy
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')


# =============================================================================
# APPLICATION DEFINITION
# =============================================================================

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    # Local apps
    'accounts',
    'dashboard',
    'pages',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # For static files
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # Cache control middleware (only active in DEBUG mode)
    'himwat.middleware.DisableBrowserCachingMiddleware',
]

ROOT_URLCONF = 'himwat.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': DEBUG,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'pages.context_processors.site_context',
                'pages.context_processors.home_context',
                'pages.context_processors.page_context',
            ],
        },
    },
]

WSGI_APPLICATION = 'himwat.wsgi.application'


# =============================================================================
# DATABASE
# =============================================================================

DATABASES = {
    'default': {
        'ENGINE': os.environ.get('DB_ENGINE', 'django.db.backends.sqlite3'),
        'NAME': os.environ.get('DB_NAME', BASE_DIR / 'db.sqlite3'),
        'USER': os.environ.get('DB_USER', ''),
        'PASSWORD': os.environ.get('DB_PASSWORD', ''),
        'HOST': os.environ.get('DB_HOST', ''),
        'PORT': os.environ.get('DB_PORT', ''),
    }
}

# PostgreSQL-specific options
if os.environ.get('DB_ENGINE') == 'django.db.backends.postgresql':
    DATABASES['default']['OPTIONS'] = {
        'connect_timeout': 10,
    }
elif os.environ.get('DB_ENGINE') == 'django.db.backends.mysql':
    DATABASES['default']['OPTIONS'] = {
        'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        'charset': 'utf8mb4',
    }


# =============================================================================
# PASSWORD VALIDATION
# =============================================================================

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


# =============================================================================
# INTERNATIONALIZATION
# =============================================================================

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kathmandu'
USE_I18N = True
USE_TZ = True


# =============================================================================
# STATIC & MEDIA FILES
# =============================================================================

STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Whitenoise for static file serving in production
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'


# =============================================================================
# DEFAULT PRIMARY KEY FIELD TYPE
# =============================================================================

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# =============================================================================
# CUSTOM USER MODEL
# =============================================================================

AUTH_USER_MODEL = 'accounts.User'


# =============================================================================
# LOGIN SETTINGS
# =============================================================================

LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/dashboard/'
LOGOUT_REDIRECT_URL = '/'


# =============================================================================
# SITE SETTINGS
# =============================================================================

SITE_NAME = os.environ.get('SITE_NAME', 'Himwatkhanda Vastu Pvt. Ltd.')
SITE_DESCRIPTION = os.environ.get('SITE_DESCRIPTION', 'Your Blueprint for Harmony, Structure, and Expertise')
SITE_URL = os.environ.get('SITE_URL', 'https://himawatkhandavastu.com')


# =============================================================================
# EMAIL CONFIGURATION
# =============================================================================

# Default to console backend for development
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL', 'noreply@localhost')
SERVER_EMAIL = os.environ.get('SERVER_EMAIL', 'server@localhost')
EMAIL_SUBJECT_PREFIX = '[Himwatkhanda Vastu] '
ADMINS = [('Admin', os.environ.get('ADMIN_EMAIL', 'admin@localhost'))]

# Load email configuration from database if available
def load_email_config():
    """Load active email configuration from database"""
    try:
        from dashboard.models import EmailConfiguration
        config = EmailConfiguration.get_active()
        if config:
            settings_dict = config.apply_to_settings()
            for key, value in settings_dict.items():
                globals()[key] = value
            globals()['ADMINS'] = [('Admin', config.admin_email)]
    except Exception:
        pass

load_email_config()


# =============================================================================
# CACHE SETTINGS
# =============================================================================

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
            'LOCATION': 'unique-snowflake',
        }
    }

# Template caching - Disabled in development
if not DEBUG:
    TEMPLATES[0]['OPTIONS']['loaders'] = [
        ('django.template.loaders.cached.Loader', (
            'django.template.loaders.filesystem.Loader',
            'django.template.loaders.app_directories.Loader',
        ))
    ]


# =============================================================================
# LOGGING CONFIGURATION
# =============================================================================

LOGS_DIR = BASE_DIR / 'logs'
os.makedirs(LOGS_DIR, exist_ok=True)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        'file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': LOGS_DIR / 'django.log',
            'maxBytes': 1024 * 1024 * 10,  # 10 MB
            'backupCount': 10,
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'level': 'INFO' if DEBUG else 'WARNING',
            'propagate': True,
        },
        'django.request': {
            'handlers': ['console', 'file'],
            'level': 'ERROR',
            'propagate': False,
        },
        'dashboard': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG' if DEBUG else 'INFO',
            'propagate': False,
        },
    },
    'root': {
        'handlers': ['console', 'file'],
        'level': 'INFO' if DEBUG else 'WARNING',
    },
}


# =============================================================================
# FILE UPLOAD SETTINGS
# =============================================================================

# Maximum upload size (10MB)
DATA_UPLOAD_MAX_MEMORY_SIZE = 10 * 1024 * 1024
FILE_UPLOAD_MAX_MEMORY_SIZE = 10 * 1024 * 1024

# Allowed file types for uploads
ALLOWED_UPLOAD_EXTENSIONS = ['.jpg', '.jpeg', '.png', '.gif', '.pdf', '.doc', '.docx', '.mp3', '.mp4']


# =============================================================================
# SESSION & COOKIE SETTINGS
# =============================================================================

SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_HTTPONLY = True

if not DEBUG:
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SESSION_COOKIE_SAMESITE = 'Strict'
    CSRF_COOKIE_SAMESITE = 'Strict'
