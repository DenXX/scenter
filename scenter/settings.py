# Django settings for scenter project.

# PROJECT_ROOT = '/home/ubuntu/Projects/scenter'
PROJECT_ROOT = '/Users/denis/Projects/scenter'

DEBUG = False
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Denis Savenkov', 'dsavenk@emory.edu'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'scenter',                      # Or path to database file if using sqlite3.
        'USER': 'scenter',
        'PASSWORD': 'scenterpass',
        'HOST': '',                             # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        #'HOST': 'scenterdb.cqfiqn6m4ik6.us-east-1.rds.amazonaws.com',
        'CONN_MAX_AGE': None,
        'PORT': '',                      # Set to empty string for default.
    },
    # 'production' : {
    #     'ENGINE': 'dbpool.db.backends.postgis',  # Using pgbouncer
    #     'OPTIONS': {'MAX_CONNS': 100},           # Using pgbouncer
    #     'NAME': 'scenter',                      # Or path to database file if using sqlite3.
    #     'USER': 'scenter',
    #     'PASSWORD': 'scenterpass',
    #     'HOST': '127.0.0.1',                      # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
    #     'PORT': 5433,                           # Using pgbouncer
    # }
}

SOUTH_DATABASE_ADAPTERS = {
    'default': 'south.db.postgresql_psycopg2',
}


# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = ['*']

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/var/www/example.com/media/"
MEDIA_ROOT = PROJECT_ROOT + '/media/'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://example.com/media/", "http://media.example.com/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/var/www/example.com/static/"
STATIC_ROOT = PROJECT_ROOT + '/static_root/'

# URL prefix for static files.
# Example: "http://example.com/static/", "http://static.example.com/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    
    PROJECT_ROOT + '/scenter_static/',
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'li(@8)ip32ogo!w1#7g@=k!tg9s6wbj!(*7*)k4p8jl=c_*7sq'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.request',
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.contrib.messages.context_processors.messages"
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

CORS_ALLOW_HEADERS = (
'x-requested-with',
'content-type',
'accept',
'origin',
'authorization',
'X-CSRFToken')

ROOT_URLCONF = 'scenter.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'scenter.wsgi.application'

TEMPLATE_DIRS = (
    PROJECT_ROOT + '/template',
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)



INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.gis',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    'rest_framework',
    'rest_framework.authtoken',
    'registration',
    'bootstrap3',
    'debug_toolbar',
    'south',
    'api',
    'website',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
)

ACCOUNT_ACTIVATION_DAYS = 7

# Email settings
DEFAULT_FROM_EMAIL = 'denissavenkov@gmail.com'
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'denissavenkov@gmail.com'
EMAIL_HOST_PASSWORD = 'Barsik%777'
EMAIL_PORT = 587

LOGIN_REDIRECT_URL = '/'

AUTH_USER_MODEL = 'api.ScenterUser'

REST_FRAMEWORK = {
    # Use hyperlinked styles by default.
    # Only used if the `serializer_class` attribute is not set on a view.
    'DEFAULT_MODEL_SERIALIZER_CLASS':
        'rest_framework.serializers.HyperlinkedModelSerializer',

    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    )
}

DEBUG_TOOLBAR_PATCH_SETTINGS = False
INTERNAL_IPS = '170.140.151.52'

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

# Allow 5 meters error in detecting fences you are in
# TODO: removed for now, SQL is slow
DEFAULT_LOCATION_MATCH_ACCURACY = 5
# Minimum fraction of polygon area to bounding box 
# area for a polygon to be displayed
AREA_RATIO_FILTER_DEFAULT = 0.0001
# Scents page size
SCENTS_PAGE_SIZE = 50
