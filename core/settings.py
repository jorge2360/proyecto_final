"""
Django settings for core project (OffTheRack).

Optimizado para despliegue en Railway con MySQL remoto.
"""

from pathlib import Path
import os
import pymysql
import dj_database_url

# ================================================
# CONFIGURACIONES BASE
# ================================================
BASE_DIR = Path(__file__).resolve().parent.parent

# Instalar soporte MySQL
pymysql.install_as_MySQLdb()

# Clave secreta y modo debug (usando variables de entorno)
SECRET_KEY = os.environ.get("SECRET_KEY", "offtherack_default_key")
DEBUG = os.environ.get("DEBUG", "False") == "True"

# Railway asigna dominio dinámico
ALLOWED_HOSTS = ["*"]

# ================================================
# APLICACIONES INSTALADAS
# ================================================
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Aplicaciones del proyecto
    'usuarios',
    'productos',
    'pedidos',
    'carrito',
    'pagos',
    'dashboard',
]

# ================================================
# MIDDLEWARE
# ================================================
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# ================================================
# TEMPLATES
# ================================================
ROOT_URLCONF = 'core.urls'

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

WSGI_APPLICATION = 'core.wsgi.application'

# ================================================
# BASE DE DATOS (Railway)
# ================================================
DATABASES = {
    'default': dj_database_url.config(
        default=os.environ.get("DATABASE_URL"),
        conn_max_age=600,
        ssl_require=False
    )
}

# ================================================
# VALIDACIÓN DE CONTRASEÑAS
# ================================================
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ================================================
# CONFIGURACIÓN DE USUARIOS
# ================================================
AUTH_USER_MODEL = "usuarios.Usuario"
LOGIN_URL = '/usuarios/login/'
LOGIN_REDIRECT_URL = "home"
LOGOUT_REDIRECT_URL = "home"

# ================================================
# INTERNACIONALIZACIÓN
# ================================================
LANGUAGE_CODE = 'es'
TIME_ZONE = 'America/Guatemala'
USE_I18N = True
USE_TZ = True

# ================================================
# ARCHIVOS ESTÁTICOS Y MEDIA
# ================================================
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# ================================================
# CONFIGURACIÓN POR DEFECTO DE ID
# ================================================
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
