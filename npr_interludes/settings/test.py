from .base import *


ALLOWED_HOSTS = ['localhost']

SECRET_KEY = 'foo'

DEFAULT_FILE_STORAGE = 'inmemorystorage.InMemoryStorage'

STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    },
}

TEMPLATE_LOADERS = (
    ('django.template.loaders.cached.Loader', (
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
    )),
)
