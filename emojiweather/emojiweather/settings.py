# Settings
# https://docs.djangoproject.com/en/2.2/topics/settings/
# https://docs.djangoproject.com/en/2.2/ref/settings/
# https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

import os


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = os.environ.get('SECRET_KEY', 'fake-key')

DEBUG = os.environ.get('DEBUG', True)

ALLOWED_HOSTS = [
    '.emojiweather.app',
]

INTERNAL_IPS = [
    '127.0.0.1',
]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.sitemaps',
    'django.contrib.sites',
    'django.contrib.staticfiles',
    'debug_toolbar',
    'widget_tweaks',
    'about',
    'commands',
    'search',
    'sms',
    'utils',
    'voice',
]

MIDDLEWARE = [
    'django.middleware.cache.UpdateCacheMiddleware',  # must be first
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.sites.middleware.CurrentSiteMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware',  # must be last
]

ROOT_URLCONF = 'emojiweather.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
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
]

WSGI_APPLICATION = 'emojiweather.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]


# Sites
# https://docs.djangoproject.com/en/2.2/ref/contrib/sites/

SITE_ID = os.environ.get('SITE_ID', 1)


# Geolocation
# https://docs.djangoproject.com/en/2.2/ref/contrib/gis/geoip2/
# http://dev.maxmind.com/geoip/geoip2/geolite2/

GEOIP_PATH = os.path.join(BASE_DIR, 'utils', 'maxmind')


# Google Geocoding API
# https://developers.google.com/maps/documentation/geocoding/start

GOOGLE_GEOCODING_API_KEY = os.environ.get('GOOGLE_GEOCODING_API_KEY', '')


# Google Maps JavaScript API
# https://developers.google.com/maps/documentation/javascript/tutorial

GOOGLE_MAPS_API_KEY = os.environ.get('GOOGLE_MAPS_API_KEY', '')


# Dark Sky API
# https://darksky.net/dev/docs

DARK_SKY_API_KEY = os.environ.get('DARK_SKY_API_KEY', '')


# Mattermost API
# https://docs.mattermost.com/developer/slash-commands.html
# https://developers.mattermost.com/integrate/slash-commands/
# https://docs.mattermost.com/help/messaging/formatting-text.html

MATTERMOST_TOKEN_ASK = os.environ.get('MATTERMOST_TOKEN_ASK', '')
MATTERMOST_TOKEN_CHUCK = os.environ.get('MATTERMOST_TOKEN_CHUCK', '')
MATTERMOST_TOKEN_FACT = os.environ.get('MATTERMOST_TOKEN_FACT', '')
MATTERMOST_TOKEN_HOT = os.environ.get('MATTERMOST_TOKEN_HOT', '')
MATTERMOST_TOKEN_PRINT = os.environ.get('MATTERMOST_TOKEN_PRINT', '')
MATTERMOST_TOKEN_WEATHER = os.environ.get('MATTERMOST_TOKEN_WEATHER', '')


# Caching
# https://docs.djangoproject.com/en/2.2/topics/cache/

CACHE_MIDDLEWARE_ALIAS = 'default'

CACHE_MIDDLEWARE_SECONDS = 604800

CACHE_MIDDLEWARE_KEY_PREFIX = ''

if DEBUG:
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.locmem.LocMemCache'
        }
    }
else:
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.memcached.PyLibMCCache',
            'TIMEOUT': None,
            'LOCATION': os.environ.get('MEMCACHIER_SERVERS', ''),
            'OPTIONS': {
                'binary': True,
                'username': os.environ.get('MEMCACHIER_USERNAME', ''),
                'password': os.environ.get('MEMCACHIER_PASSWORD', ''),
                'behaviors': {
                    'no_block': True,
                    'tcp_nodelay': True,
                    'tcp_keepalive': True,
                    'connect_timeout': 2000,  # ms
                    'send_timeout': 750 * 1000,  # us
                    'receive_timeout': 750 * 1000,  # us
                    '_poll_timeout': 2000,  # ms
                    'ketama': True,
                    'remove_failed': 1,
                    'retry_timeout': 2,
                    'dead_timeout': 30,
                }
            }
        }
    }


# Heroku
# https://devcenter.heroku.com/articles/django-app-configuration

import django_heroku

django_heroku.settings(locals())
