#COdigo 9: Ajuste de settings.py en auth

from pathlib import Path
from decouple import config
from datetime import timedelta

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


SECRET_KEY = config('SECRET_KEY')

DEBUG = config("DEBUG", default=False, cast=bool)

ALLOWED_HOSTS = [
    "localhost",
    "127.0.0.1",
    "servicio_auth",
]

# Application definition

INSTALLED_APPS = [
    "autentificacion.apps.AutentificacionConfig",
    "rest_framework_simplejwt.token_blacklist",
    "django_filters",
    "drf_yasg",
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
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

ROOT_URLCONF = 'core.urls'

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

WSGI_APPLICATION = 'core.wsgi.application'


# Database
# https://docs.djangoproject.com/en/6.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": config("DATABASE_ENGINE"),
        "NAME": config("DATABASE_NAME"),
        "USER": config("DATABASE_USER"),
        "PASSWORD": config("DATABASE_PASSWORD"),
        "HOST": config("DATABASE_HOST"),
        "PORT": config("DATABASE_PORT"),
    }
}


# Password validation
# https://docs.djangoproject.com/en/6.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/6.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/6.0/howto/static-files/

STATIC_URL = "/api/auth/static/"

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
}

# ─────────────────────────────────────────
# Llaves RS256 (asimétricas) para JWT
# ─────────────────────────────────────────
# servicio_auth es el único servicio que posee la llave PRIVADA: es el
# único autorizado para FIRMAR (emitir) tokens. También conserva la
# pública porque valida sus propios tokens en endpoints como
# log_views.py (IsAuthenticated / IsAdminUser sobre request.user real).
_JWT_PRIVATE_KEY_PATH = BASE_DIR / 'keys' / 'private.pem'
_JWT_PUBLIC_KEY_PATH = BASE_DIR / 'keys' / 'public.pem'

JWT_SIGNING_KEY = _JWT_PRIVATE_KEY_PATH.read_text() if _JWT_PRIVATE_KEY_PATH.exists() else None
JWT_VERIFYING_KEY = _JWT_PUBLIC_KEY_PATH.read_text() if _JWT_PUBLIC_KEY_PATH.exists() else None

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=30),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),

    # Rotación de refresh tokens
    'ROTATE_REFRESH_TOKENS': True,

    # Enviar refresh token usado a blacklist
    'BLACKLIST_AFTER_ROTATION': True,

    'ALGORITHM': 'RS256',
    'SIGNING_KEY': JWT_SIGNING_KEY,
    'VERIFYING_KEY': JWT_VERIFYING_KEY,
    'AUDIENCE': None,
    'ISSUER': None,
    'JWK_URL': None,
    'LEEWAY': 0,

    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',

    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',

    'AUTH_TOKEN_CLASSES': (
        'rest_framework_simplejwt.tokens.AccessToken',
    ),

    'TOKEN_TYPE_CLAIM': 'token_type',
    'TOKEN_USER_CLASS': 'rest_framework_simplejwt.models.TokenUser',

    'JTI_CLAIM': 'jti',

    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': timedelta(minutes=5),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
}
SWAGGER_SETTINGS = {
    'USE_SESSION_AUTH': False,
    'VALIDATOR_URL': None,
    'SECURITY_DEFINITIONS': {
        'Bearer': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header',
            'description': (
                'Encabezado para autenticación JWT con esquema Bearer. '
                'Ejemplo: "Bearer {token}"'
            ),
        }
    },
}

# ─────────────────────────────────────────
# LOGGING — Logs técnicos y de auditoría
# ─────────────────────────────────────────
import os

LOGS_DIR = BASE_DIR / 'logs'
os.makedirs(LOGS_DIR, exist_ok=True)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,

    'formatters': {
        'tecnico_detallado': {
            'format': '[{asctime}] [{levelname}] [{name}] [{module}:{lineno}] {message}',
            'style': '{',
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
        'consola_simple': {
            'format': '[{levelname}] {name}: {message}',
            'style': '{',
        },
        'auditoria_formato': {
            'format': '[{asctime}] [AUDITORIA] [Usuario: {message}]',
            'style': '{',
            'datefmt': '%Y-%m-%d %H:%M:%S',
        }
    },

    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },

    'handlers': {
        'consola': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'consola_simple',
            'filters': ['require_debug_true'],
        },
        'archivo_tecnico': {
            'level': 'WARNING',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': LOGS_DIR / 'tecnico.log',
            'maxBytes': 1024 * 1024 * 5,
            'backupCount': 5,
            'formatter': 'tecnico_detallado',
            'encoding': 'utf-8',
        },
        'archivo_debug': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': LOGS_DIR / 'debug.log',
            'maxBytes': 1024 * 1024 * 5,
            'backupCount': 3,
            'formatter': 'tecnico_detallado',
            'encoding': 'utf-8',
        },
        'archivo_auditoria': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': LOGS_DIR / 'auditoria.log',
            'maxBytes': 1024 * 1024 * 10,
            'backupCount': 10,
            'formatter': 'auditoria_formato',
            'encoding': 'utf-8',
        }
    },

    'loggers': {
        'django': {
            'handlers': ['consola', 'archivo_tecnico'],
            'level': 'WARNING',
            'propagate': False,
        },
        'django.request': {
            'handlers': ['archivo_tecnico'],
            'level': 'WARNING',
            'propagate': False,
        },
        'django.db.backends': {
            'handlers': ['archivo_debug'],
            'level': 'DEBUG',
            'propagate': False,
            'filters': ['require_debug_true'],
        },

        'servicio_auth': {
            'handlers': ['consola', 'archivo_tecnico', 'archivo_debug'],
            'level': 'DEBUG',
            'propagate': False,
        },
        # Logger usado por autentificacion/serializers.py y views.py
        # (logging.getLogger('auditoria'))
        'auditoria': {
            'handlers': ['archivo_auditoria', 'consola'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}