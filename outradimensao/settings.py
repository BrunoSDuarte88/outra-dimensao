import os
import certifi
from pathlib import Path
import logging
from decouple import config
import dj_database_url

# Corrige certificado SSL no Windows (emails e requisições seguras)
os.environ['SSL_CERT_FILE'] = certifi.where()

# Configurações sensíveis via .env
DEBUG = config('DEBUG', default=False, cast=bool)
SECRET_KEY = config('SECRET_KEY')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL')
RECAPTCHA_SITE_KEY = config('RECAPTCHA_SITE_KEY')
RECAPTCHA_SECRET_KEY = config('RECAPTCHA_SECRET_KEY')

# Logs básicos (desenvolvimento)
logging.basicConfig(level=logging.DEBUG)

# Diretório base
BASE_DIR = Path(__file__).resolve().parent.parent

# Hosts permitidos
ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    'outradimensao.onrender.com',
]

# Aplicativos instalados
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'portal',
    'forum',
]

# Usuário personalizado
AUTH_USER_MODEL = 'portal.CustomUser'

# Login / Logout
LOGIN_URL = '/login/'
LOGOUT_REDIRECT_URL = '/'

# Middlewares
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

# Arquivos estáticos
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'portal/static')]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Templates
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

ROOT_URLCONF = 'outradimensao.urls'
WSGI_APPLICATION = 'outradimensao.wsgi.application'

# Banco de dados (SQLite)
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

DATABASES = {
    'default': dj_database_url.config(
        default=config('DATABASE_URL')
    )
}

# Validação de senha
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internacionalização
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'America/Sao_Paulo'
USE_I18N = True
USE_TZ = True

# Campo padrão de chave primária
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# E-mail
EMAIL_BACKEND = 'portal.email_backend.CustomEmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True

# As variáveis sensíveis são lidas do .env:
# - EMAIL_HOST_USER
# - EMAIL_HOST_PASSWORD
# - DEFAULT_FROM_EMAIL
# - RECAPTCHA_SITE_KEY
# - RECAPTCHA_SECRET_KEY

