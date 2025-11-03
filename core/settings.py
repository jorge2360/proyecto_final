from pathlib import Path
import os
import pymysql
import dj_database_url

# Necesario para Django 5.x con PyMySQL
pymysql.install_as_MySQLdb()

# Ruta base
BASE_DIR = Path(__file__).resolve().parent.parent

# Seguridad
SECRET_KEY = os.environ.get("SECRET_KEY", "dev-insecure-key")
DEBUG = os.environ.get("DEBUG", "False").lower() == "true"

# Hosts permitidos (Render usa dominio dinámico)
ALLOWED_HOSTS = ["localhost", "127.0.0.1", ".onrender.com"]
RENDER_EXTERNAL_HOSTNAME = os.environ.get("RENDER_EXTERNAL_HOSTNAME")
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)
CSRF_TRUSTED_ORIGINS = ["https://*.onrender.com"]

# Aplicaciones instaladas
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "usuarios",
    "productos",
    "pedidos",
    "carrito",
    "pagos",
    "dashboard",
]

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

ROOT_URLCONF = "core.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "core.wsgi.application"

# =====================
#  BASE DE DATOS MYSQL
# =====================
import dj_database_url
import os

DATABASES = {
    'default': dj_database_url.parse(
        'mysql://root:IkUhmgnDlWZvBEFcaTakSDIVyqMZoZAY@shortline.proxy.rlwy.net:12276/railway',
        engine='django.db.backends.mysql',
        conn_max_age=600,
        ssl_require=False
    )
}


# =====================
#  CONFIGURACIONES VARIAS
# =====================

AUTH_USER_MODEL = "usuarios.Usuario"  # Si tienes modelo personalizado

LANGUAGE_CODE = "es"
TIME_ZONE = "America/Guatemala"
USE_I18N = True
USE_TZ = True

STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"] if (BASE_DIR / "static").exists() else []
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# HTTPS y proxy Render
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
