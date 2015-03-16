"""
Django settings for gudfud project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import datetime

BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 's+y5%&3g5uzy3-2f9f85zy+t*xm@bs+ttx-^ow(rlwy2$=0*)!'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'foodie',
    'rest_framework',
    'rest_framework.authtoken',
    'social.apps.django_app.default',
    'corsheaders'
)

MIDDLEWARE_CLASSES = (
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    # 'django.contrib.auth.middleware.AuthenticationMiddleware',
    # 'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    # 'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

CORS_ORIGIN_ALLOW_ALL = True

ROOT_URLCONF = 'gudfud.urls'

WSGI_APPLICATION = 'gudfud.wsgi.application'

AUTH_USER_MODEL = 'foodie.BaseUser'

# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'


# REST Framework global settings
REST_FRAMEWORK = {
    # Use hyperlinked styles by default.
    # Only used if the `serializer_class` attribute is not set on a view.
    'DEFAULT_MODEL_SERIALIZER_CLASS': 'rest_framework.serializers.HyperlinkedModelSerializer',
    'URL_FIELD_NAME': 'uri',
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
    )
}

AUTHENTICATION_BACKENDS = (
    'social.backends.facebook.FacebookAppOAuth2',
    'social.backends.facebook.FacebookOAuth2',
    'social.backends.google.GoogleOAuth2',
    'social.backends.twitter.TwitterOAuth',
    'django.contrib.auth.backends.ModelBackend',
)


# SOCIAL_AUTH_PIPELINE = (
# 'social.pipeline.social_auth.social_details',
# 'social.pipeline.social_auth.social_uid',
# 'social.pipeline.social_auth.auth_allowed',
# 'social.pipeline.social_auth.social_user',
# 'social.pipeline.user.get_username',
# 'social.pipeline.social_auth.associate_by_email',
# 'social.pipeline.user.create_user',
# 'social.pipeline.social_auth.associate_user',
# 'social.pipeline.social_auth.load_extra_data',
# 'social.pipeline.user.user_details'
# )

# ---- Facebook settings ------
# FACEBOOK_APP_ID = '406752779495620'
# FACEBOOK_APP_SECRET = 'b38ac3bf53da327d8d6cefb2a26a5572'

SOCIAL_AUTH_FACEBOOK_KEY = '406752779495620'
SOCIAL_AUTH_FACEBOOK_SECRET = 'b38ac3bf53da327d8d6cefb2a26a5572'
SOCIAL_AUTH_FACEBOOK_SCOPE = ['email']

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = '228356886278-r9237hs99u0iogtjmovogvrvmuaohptr.apps.googleusercontent.com'
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = 'uxM2i6FG41CVK31TF414Zm2k'
SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE = ['email', 'profile']

SOCIAL_AUTH_TWITTER_KEY = 'tdqHkvZb6FlmmIxd8JaHJJWca'
SOCIAL_AUTH_TWITTER_SECRET = ' OBu9RFtMMSKXDPNY5jthTjB9IlriIbahWzpgmt6kDH94Xu7klP'

SOCIAL_AUTH_USER_MODEL = 'foodie.BaseUser'
SOCIAL_AUTH_USERNAME_IS_FULL_EMAIL = True

# ---- GUDFUD settings -----
# Global constants
GUDFUD_USER_IMAGE_FILE_MAX_SIZE = 1000
# Image max dimensions
GUDFUD_USER_IMAGE_MAX_HEIGHT = 1000
GUDFUD_USER_IMAGE_MAX_WIDTH = 1000
# Thumbnail image dimensions
GUDFUD_USER_THUMBNAIL_HEIGHT = 60
GUDFUD_USER_THUMBNAIL_WIDTH = 50


TEMPLATE_CONTEXT_PROCESSORS = (
    'social.apps.django_app.context_processors.backends',
    'social.apps.django_app.context_processors.login_redirect'
)
