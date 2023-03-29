from parallax.settings import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME', 'parallax'),
        'USER': os.getenv('DB_USER', 'parallax'),
        'PASSWORD': os.getenv('DB_PASSWORD', 'parallax'),
        'HOST': os.getenv('DB_HOST', 'localhost'),
        'PORT': 5432,
    }
}
