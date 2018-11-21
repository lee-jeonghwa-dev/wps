from .base import *
DEBUG = True

secrets = json.load(open(os.path.join(SECRET_DIR, 'dev.json')))

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = secrets['DATABASE']
