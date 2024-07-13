from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# CSRF
CSRF_USE_SESSIONS = True
CSRF_TRUSTED_ORIGINS = ['http://social_back/',
                        'http://localhost/',
                        ]


# Cors

CORS_ALLOW_ALL_ORIGINS = True