import django.conf.global_settings as DEFAULT_SETTINGS
import os


BASE_DIR = os.path.dirname(__file__)

SECRET_KEY = 'tsktsktsk'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    },
}

TEMPLATE_CONTEXT_PROCESSORS = DEFAULT_SETTINGS.TEMPLATE_CONTEXT_PROCESSORS + (
    'django.core.context_processors.request',
)

INSTALLED_APPS = (
    # Default Django apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # We load dependencies
    'bootstrap3',
    'backbone_calendar',
)

ROOT_URLCONF = 'backbone_calendar.urls'

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

# html validation (django-html-validator)

HTMLVALIDATOR_ENABLED = True

HTMLVALIDATOR_FAILFAST = True

# HTMLVALIDATOR_VNU_URL = 'http://validator.nu/'
HTMLVALIDATOR_VNU_URL = 'https://validator.nu/'
# HTMLVALIDATOR_VNU_JAR = '~/dev/dist/vnu.jar'

HTMLVALIDATOR_DUMPDIR = os.path.join(BASE_DIR, 'validation_errors')

HTMLVALIDATOR_OUTPUT = 'file'  # default is 'file'
