"""
Django settings for tscast project.

Generated by 'django-admin startproject' using Django 1.10.2.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'v5#gix1jc-r!n#mqy!ky6ey7!sf@b+(44fy=d)q8h8n)axu)$i'

# SECURITY WARNING: don't run with debug turned on in production!
TSCAST_ENV = os.environ.get('TSCAST_ENV')
if TSCAST_ENV != 'PRODUCT':
    DEBUG = True
else:
    DEBUG = False


ALLOWED_HOSTS = ['127.0.0.1', '120.25.232.11',]


# Application definition

INSTALLED_APPS = [
    'jet.dashboard',
    'jet',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'raven.contrib.django.raven_compat',
    'podcast',
    'member',
    'term',
    'wechat',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'tscast.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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
]


CACHES = {
    'default': {
        'BACKEND': 'redis_cache.cache.RedisCache',
        'LOCATION': '127.0.0.1:6379',
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
    'db': {
        'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
        'LOCATION': 'django_cache_table',
    }
}

WSGI_APPLICATION = 'tscast.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(BASE_DIR, 'tscast/static/')

MEDIA_URL = '/media/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'tscast/media/')


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(asctime)s %(message)s'
        },
    },
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            # 'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'filters': ['require_debug_false']
        },
#         'file': {
#             'level': 'INFO',
#             'class': 'logging.handlers.TimedRotatingFileHandler',
#             'filename': os.path.join(LOG_FILE_PATH, 'mjtt_django.log'),
#             'when': 'd',
#             'formatter': 'verbose'
#         },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'propagate': True,
        },
        'podcast': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': True,
        }
    }
}


# DJANGO JET
JET_SIDE_MENU_CUSTOM_APPS = [
        ('podcast', [
            'PodcastChannel',
            'PodcastHost',
            'PodcastAlbum',
            'PodcastEpisode',
            # 'PodcastEnclosure',
        ]),
        ('member', [
            'Member',
            'TrialMember',
            'PodcastAlbumSubscription',
        ]),
        ('term', [
            'Tier',
            'Order',
            'Payment',
            'Purchase',
        ]),
        ('wechat', [
            'WeChatMemberGroup',
            'WeChatMember',
            # 'WeChatMenuMatchRule',
            'WeChatMenuButton',
        ]),
        ('auth', [
            'User',
            'Group',
        ]),
    ]

JET_SIDE_MENU_COMPACT = True
JET_INDEX_DASHBOARD = 'tscast.dashboard.CustomIndexDashboard'



# REST FRAMEWORK
REST_FRAMEWORK = {
        'DEFAULT_AUTHENTICATION_CLASSES': (
            'member.authentication.MemberTokenAuthentication',
            ),
        'DEFAULT_FILTER_BACKENDS': (
            'rest_framework.filters.DjangoFilterBackend',
            'rest_framework.filters.SearchFilter',
            'rest_framework.filters.OrderingFilter',
            ),
        'SEARCH_PARAM': 'search',
        'DEFAULT_PAGINATION_CLASS': 'tscast.utils.pagination.CommonPageNumberPagination',
        'DEFAULT_RENDERER_CLASSES': (
            'rest_framework.renderers.JSONRenderer',
            'rest_framework.renderers.BrowsableAPIRenderer',
            ) if DEBUG else (
            'rest_framework.renderers.JSONRenderer',
            ),
        'DEFAULT_PERMISSION_CLASSES': (
            'tscast.utils.permissions.ReadOnly',
            ),
        }

PODCAST_ENCLOSURE_STORAGE = 'django.core.files.storage.FileSystemStorage'

PODCAST_IMAGE_STORAGE = 'django.core.files.storage.FileSystemStorage'

MEMBER_IMAGE_STORAGE = 'django.core.files.storage.FileSystemStorage'

UPLOAD_BASE_DIR = 'upload'


# SENTRY RAVEN
RAVEN_CONFIG = {
    'dsn': 'https://52ff3091d44543fbbf7468a84358da06:0bdd2be3023d4be4820b878c2f5b714f@sentry.io/117413',
    #  If you are using git, you can also automatically configure the 
    #  release based on the git info.
    # 'release': raven.fetch_git_sha(os.path.dirname(os.pardir)),
}


# WECHAT
WECHAT_TOKEN = 'gNHmLEkaE/JL8DH0TIFFhquB2xP9fYqdDnUufc6Xfnw='
WECHAT_APPID = 'wx4ff6dd6b015ca309'
WECHAT_APPSECRET = '5e2b01725af0c546ebcecf9ebe087136'
