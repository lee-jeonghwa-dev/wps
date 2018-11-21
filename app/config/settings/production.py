from .base import *
DEBUG = False

secrets = json.load(open(os.path.join(SECRET_DIR, 'production.json')))

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = secrets['DATABASE']
