DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'tscast',
        'USER': 'root',
        'PASSWORD': 'sloth',
        'HOST': '120.76.159.185',
        'PORT': '3306',
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            # 'charset': 'utf8mb4',
        },
    },
}



CACHES = {
    'default': {
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
    'locmem': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    },
}
