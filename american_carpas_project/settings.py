"""
Django settings for american_carpas_project project.
"""

import os
from pathlib import Path

# Base
BASE_DIR = Path(__file__).resolve().parent.parent

# Seguridad
SECRET_KEY = os.environ.get(
    'SECRET_KEY',
    'django-insecure-s&b(1-wb_g@0(ck2%4i(im5s)t5k0yl#e&rld+h$0#g^&urcvl'
)
DEBUG = os.environ.get('DEBUG', 'True') == 'True'

# Hosts permitidos y CSRF
# - Acepta localhost y dominios de Railway (.up.railway.app).
# - Permite ampliar vía variable ALLOWED_HOSTS.
# - Si existe RAILWAY_PUBLIC_DOMAIN, lo agrega.
railway_domain = os.environ.get('RAILWAY_PUBLIC_DOMAIN')  # p.ej. web-xxx.up.railway.app

default_hosts = ['localhost', '127.0.0.1', '.up.railway.app']
env_hosts = os.environ.get('ALLOWED_HOSTS', '')
env_hosts_list = [h.strip() for h in env_hosts.split(',') if h.strip()]
ALLOWED_HOSTS = list(dict.fromkeys(default_hosts + env_hosts_list + ([railway_domain] if railway_domain else [])))

# CSRF_TRUSTED_ORIGINS debe incluir esquemas (http/https). En prod, usa https.
csrf_env = os.environ.get('CSRF_TRUSTED_ORIGINS', '')
CSRF_TRUSTED_ORIGINS = [o.strip() for o in csrf_env.split(',') if o.strip()]

if railway_domain:
    domain_url = f"https://{railway_domain}"
    if domain_url not in CSRF_TRUSTED_ORIGINS:
        CSRF_TRUSTED_ORIGINS.append(domain_url)

# Aplicaciones
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'trabajadores',  # App personalizada
]

# Middleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Archivos estáticos en prod
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'american_carpas_project.urls'

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

WSGI_APPLICATION = 'american_carpas_project.wsgi.application'

# Base de datos (MySQL)
# Lee primero variables estándar de Railway (MYSQL*), y permite override con DB_*.
MYSQL_NAME = os.environ.get('MYSQLDATABASE') or os.environ.get('DB_NAME', 'american_carpas_db')
MYSQL_USER = os.environ.get('MYSQLUSER') or os.environ.get('DB_USER', 'root')
MYSQL_PASSWORD = os.environ.get('MYSQLPASSWORD') or os.environ.get('DB_PASSWORD', '')
MYSQL_HOST = os.environ.get('MYSQLHOST') or os.environ.get('DB_HOST', 'localhost')
MYSQL_PORT = os.environ.get('MYSQLPORT') or os.environ.get('DB_PORT', '3306')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': MYSQL_NAME,
        'USER': MYSQL_USER,
        'PASSWORD': MYSQL_PASSWORD,
        'HOST': MYSQL_HOST,
        'PORT': str(MYSQL_PORT),
        'OPTIONS': {
            'charset': 'utf8mb4',
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        },
        'CONN_MAX_AGE': 60,  # Mantén conexiones abiertas para performance
    }
}

# Validadores de contraseña
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internacionalización
LANGUAGE_CODE = 'es-co'
TIME_ZONE = 'America/Bogota'
USE_I18N = True
USE_TZ = True

# Archivos estáticos
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Archivos de media
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Clave primaria por defecto
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Seguridad en producción
# Railway está detrás de proxy; respeta protocolo original para redirects y CSRF.
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

if not DEBUG:
    # Fuerza HTTPS
    SECURE_SSL_REDIRECT = True

    # Cookies seguras
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True

    # Cabeceras de seguridad
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = 'DENY'

    # HSTS
    SECURE_HSTS_SECONDS = 31536000  # 1 año
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True