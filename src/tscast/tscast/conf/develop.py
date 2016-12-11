import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    },
}

CACHES = {
    'redis': {
        'BACKEND': 'redis_cache.cache.RedisCache',
        'LOCATION': 'redis:6379',
        'OPTIONS': {
            'DB': 6,
            'PASSWORD': '',
            'PICKLE_VERSION': -1, # default
            'PARSER_CLASS': 'redis.connection.HiredisParser',
            'CLIENT_CLASS': 'redis_cache.client.DefaultClient',
        },
    },
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    },
    'db': {
        'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
        'LOCATION': 'django_cache_table',
    }
}
