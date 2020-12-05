
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
TEMPLATES_DIRS = BASE_DIR / 'templates'
STATIC_DIR = BASE_DIR / 'static'
MEDIA_DIR = BASE_DIR / 'media'



# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '_=)o-=&uj@*gi46h^^sweb-&4qt2y)t!ya2lx7b@1yx(t)9z^)'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['67.205.162.114','faruk.hamzazahid.com','www.faruk.hamzazahid.com']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'phonenumber_field',
    'rest_framework',
    'crispy_forms',
    'django_cleanup',


    'Login_app',
    'Dashboard_app',
    'Product_inventory_app',
    'Todo_app',
    'Message_app',
    'Product_record_for_final_calculation_app',
    'setting_app',
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

ROOT_URLCONF = 'Shop_management.urls'
AUTH_USER_MODEL = 'Login_app.User'
CRISPY_TEMPLATE_PACK = 'bootstrap4'


PHONENUMBER_DB_FORMAT = 'NATIONAL'
PHONENUMBER_DEFAULT_REGION = 'BD'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATES_DIRS, ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',

                'Dashboard_app.context_processors.user_role',
                'Dashboard_app.context_processors.today_all_payments',
                'Todo_app.context_processors.all_tasks',
                'Message_app.context_processors.unread_messages',
                'Message_app.context_processors.online_active_user',
            ],
        },
    },
]

WSGI_APPLICATION = 'Shop_management.wsgi.application'





# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'faruk',
        'USER': 'shajjad',
        'PASSWORD': 'shajjad2015',
        'HOST': 'localhost',
        'PORT': '',
    }
}



# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Dhaka'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'


STATICFILES_DIRS = [
    STATIC_DIR,
]
STATIC_ROOT = BASE_DIR / 'staticfiles/'
MEDIA_ROOT = MEDIA_DIR
MEDIA_URL = '/media/'
LOGIN_URL = '/account/login'



# celery app
# REDIS_HOST = 'localhost'

# CELERY_BROKER_URL = 'redis://:p2e249ee785968eb914d440c05326b4a0a9df8d71e4415413e861902b45917e6d@ec2-18-214-6-8.compute-1.amazonaws.com:13069'

# CELERY_BEAT_SCHEDULE = {
#     'call-fn': {
#         'task': 'Product_record_for_final_calculation_app.tasks.update_balance_sheet',
#         'schedule': 5,
#         'args': [2]
#     }
# }




EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'shaturngbd@gmail.com'
EMAIL_HOST_PASSWORD = 'shapla2015'
EMAIL_PORT = 587
EMAIL_USE_TLS = True


