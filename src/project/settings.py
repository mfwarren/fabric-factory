# Django settings for prj project.
import os
import logging

PROJECT_PATH = os.path.dirname(os.path.normpath(__file__))
PROJECT_ROOT = os.path.normpath(PROJECT_PATH + '/..')

BUILD_PATH = os.path.join(PROJECT_PATH, 'media/build_packages')
BUILD_URL = "/site_media/build_packages"


DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS

DATABASE_ENGINE = 'sqlite3'           # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
DATABASE_NAME = os.path.join(PROJECT_PATH, 'dev.db')             # Or path to database file if using sqlite3.
DATABASE_USER = ''             # Not used with sqlite3.
DATABASE_PASSWORD = ''         # Not used with sqlite3.
DATABASE_HOST = ''             # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT = ''             # Set to empty string for default. Not used with sqlite3.

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = os.path.join(PROJECT_PATH, 'media')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/site_media/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/admin_media/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'kfzm^878p-rrr58hn+tt%sgxo!6jb*ho2xd+7ce!%r_+%yxwjp'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
#     'django.template.loaders.eggs.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
)

ROOT_URLCONF = 'project.urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(PROJECT_PATH, "templates")
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    
    'factory',
    "worker", # added only to be able to run the test suite
)

DEFAULT_FILE_STORAGE = 'factory.storage.FileSystemStorageUuidName'

##################################################
# logging
#
# Set the logging level to control the volume of emitted log messages.
# Use logging.DEBUG to emit all log messages. To get progressively fewer
# messages use logging.INFO, logging.WARNING, logging.ERROR, logging.CRITICAL
#
LOGGING_LEVEL = (logging.DEBUG if DEBUG else logging.WARNING)
# Use this to change the filename and/or location of the logfile as needed.
LOGGING_LOGFILE = os.path.join(PROJECT_PATH, 'factory.log')
# You probably won't need to change the following default settings

LOGGING_FORMAT = "%(asctime)s [%(levelname)s] %(message)s"
LOGGING_DATEFMT = "%m-%d %H:%M:%S"
 
# Uncomment this call to basicConfig code to enable logging.
# (Some deployments will require advanced logging configuration.
# In that case, substitute that logging setup code here instead.)

logging.basicConfig(level=LOGGING_LEVEL,
                    format=LOGGING_FORMAT,
                    datefmt=LOGGING_DATEFMT,
                    filename=LOGGING_LOGFILE,
                    filemode="a")

try:
    from project.local_settings import *
except:
    pass
