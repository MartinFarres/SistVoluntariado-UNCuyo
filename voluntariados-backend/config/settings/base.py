from pathlib import Path
from dotenv import load_dotenv
import os


BASE_DIR = Path(__file__).resolve().parent.parent.parent
load_dotenv(os.path.join(BASE_DIR, '.env'))

SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'unsafe-secret-key')
DEBUG = int(os.environ.get('DEBUG', 1))

ALLOWED_HOSTS = ['*']

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

AUTHENTICATION_BACKENDS = (
    "django.contrib.auth.backends.ModelBackend",  # default
    "allauth.account.auth_backends.AuthenticationBackend",  # needed for allauth
)

AUTH_USER_MODEL = 'users.User'

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.IsAuthenticated",
    ),
}


# Allauth settings
ACCOUNT_USER_MODEL_USERNAME_FIELD = None  # still needed because your User has no username
ACCOUNT_LOGIN_METHODS = {"email"}  # Only allow login with email
ACCOUNT_SIGNUP_FIELDS = ["email*", "password1*", "password2*"]


INSTALLED_APPS = [
    # Django
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    "django.contrib.sites",   # required by allauth
    # 3rd party
    'rest_framework',
    "allauth",
    "allauth.account",
    "allauth.socialaccount",  # For social login
    "allauth.socialaccount.providers.google",

    # Tus apps 
    'apps.users',           
    'apps.persona',
    'apps.voluntariado',
    'apps.asistencia',
    'apps.capacitacion',
    'apps.organizacion',
    'apps.ubicacion',
    'apps.certificado',    
    'apps.facultad',        
    'apps.soft_delete',        
]

SITE_ID = 1  # required by allauth

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware'
]

ROOT_URLCONF = 'config.urls'

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
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('POSTGRES_DB', 'voluntariados'),
        'USER': os.environ.get('POSTGRES_USER', 'voluntario'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD', 'voluntario'),
        'HOST': os.environ.get('POSTGRES_HOST', 'db'),
        'PORT': os.environ.get('POSTGRES_PORT', 5432),
    }
}

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

LANGUAGE_CODE = 'es-ar'
TIME_ZONE = 'America/Argentina/Buenos_Aires'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'static'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'