from .base import *
DEBUG = False

secrets = json.load(open(os.path.join(SECRET_DIR, 'production.json')))

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = secrets['DATABASE']

DEFAULT_FILE_STORAGE = 'config.storages.MediaStorage'
AWS_ACCESS_KEY_ID = secrets['AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY = secrets['AWS_SECRET_ACCESS_KEY']
AWS_STORAGE_BUCKET_NAME = secrets['AWS_STORAGE_BUCKET_NAME']