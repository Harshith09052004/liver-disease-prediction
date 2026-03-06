import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# ---------------- SECURITY ----------------

SECRET_KEY = 'django-insecure-key'

DEBUG = True

ALLOWED_HOSTS = [
"liver-disease-prediction-e4jd.onrender.com",
"localhost",
"127.0.0.1"
]

# ---------------- INSTALLED APPS ----------------

INSTALLED_APPS = [
'django.contrib.admin',
'django.contrib.auth',
'django.contrib.contenttypes',
'django.contrib.sessions',
'django.contrib.messages',
'django.contrib.staticfiles',

```
'liver_disease_prediction.Remote_User',
'liver_disease_prediction.Service_Provider',
```

]

# ---------------- MIDDLEWARE ----------------

MIDDLEWARE = [
'django.middleware.security.SecurityMiddleware',

```
# WhiteNoise for static files (required for Render)
'whitenoise.middleware.WhiteNoiseMiddleware',

'django.contrib.sessions.middleware.SessionMiddleware',
'django.middleware.common.CommonMiddleware',
'django.middleware.csrf.CsrfViewMiddleware',
'django.contrib.auth.middleware.AuthenticationMiddleware',
'django.contrib.messages.middleware.MessageMiddleware',
'django.middleware.clickjacking.XFrameOptionsMiddleware',
```

]

ROOT_URLCONF = 'liver_disease_prediction.urls'

# ---------------- TEMPLATES ----------------

TEMPLATES = [
{
'BACKEND': 'django.template.backends.django.DjangoTemplates',

```
    'DIRS': [
        os.path.join(BASE_DIR, 'Template')
    ],

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
```

]

WSGI_APPLICATION = 'liver_disease_prediction.wsgi.application'

# ---------------- DATABASE ----------------

DATABASES = {
'default': {
'ENGINE': 'django.db.backends.sqlite3',
'NAME': BASE_DIR / 'db.sqlite3',
}
}

# ---------------- PASSWORD VALIDATION ----------------

AUTH_PASSWORD_VALIDATORS = [
{
'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
},
{
'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
},
]

# ---------------- LANGUAGE ----------------

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'

USE_I18N = True
USE_TZ = True

# ---------------- STATIC FILES ----------------

STATIC_URL = '/static/'

STATICFILES_DIRS = [
os.path.join(BASE_DIR, 'Template', 'images')
]

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# ---------------- MEDIA FILES ----------------

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'Template', 'media')

# ---------------- DEFAULT AUTO FIELD ----------------

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
