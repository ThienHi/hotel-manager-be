from .base import *  # noqa
from .base import env

# GENERAL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#debug
DEBUG = True
# https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
SECRET_KEY = env(
    "DJANGO_SECRET_KEY",
    default="bsWzFpTdMt4Fxo4ng3L0zy9749FLLjFz8LIKRVphcGUwRd0eI8uo6FU6Bd8bCxq4",
)
# https://docs.djangoproject.com/en/dev/ref/settings/#allowed-hosts
# ALLOWED_HOSTS = ["ec2-175-41-160-73.ap-southeast-1.compute.amazonaws.com"]
ALLOWED_HOSTS = ["*"]

# CACHES
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#caches
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "",
    }
}

# EMAIL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#email-backend
EMAIL_BACKEND = env(
    "DJANGO_EMAIL_BACKEND", default="django.core.mail.backends.console.EmailBackend"
)

# WhiteNoise
# ------------------------------------------------------------------------------
# http://whitenoise.evans.io/en/latest/django.html#using-whitenoise-in-development
INSTALLED_APPS = ["whitenoise.runserver_nostatic"] + INSTALLED_APPS  # noqa F405


# django-debug-toolbar
# ------------------------------------------------------------------------------
# https://django-debug-toolbar.readthedocs.io/en/latest/installation.html#prerequisites
INSTALLED_APPS += ["debug_toolbar"]  # noqa F405
# https://django-debug-toolbar.readthedocs.io/en/latest/installation.html#middleware
MIDDLEWARE += ["debug_toolbar.middleware.DebugToolbarMiddleware"]  # noqa F405
# https://django-debug-toolbar.readthedocs.io/en/latest/configuration.html#debug-toolbar-config
DEBUG_TOOLBAR_CONFIG = {
    "DISABLE_PANELS": ["debug_toolbar.panels.redirects.RedirectsPanel"],
    "SHOW_TEMPLATE_CONTEXT": True,
}
# https://django-debug-toolbar.readthedocs.io/en/latest/installation.html#internal-ips
INTERNAL_IPS = ["127.0.0.1", "10.0.2.2"]
if env("USE_DOCKER") == "yes":
    import socket

    hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
    INTERNAL_IPS += [".".join(ip.split(".")[:-1] + ["1"]) for ip in ips]

# django-extensions
# ------------------------------------------------------------------------------
# https://django-extensions.readthedocs.io/en/latest/installation_instructions.html#configuration
INSTALLED_APPS += ["django_extensions"]  # noqa F405
# Celery
# ------------------------------------------------------------------------------

# https://docs.celeryq.dev/en/stable/userguide/configuration.html#task-eager-propagates
CELERY_TASK_EAGER_PROPAGATES = True
# Your stuff...
# ------------------------------------------------------------------------------


# APP Facebook
SUBSCRIBE_FIELDS = 'messages,messaging_postbacks,feed,inbox_labels,message_reads'

FACEBOOK_APP_ID = '832732297817343'     # 459417807935454
FACEBOOK_APP_SECRET = '2958fe3d1ddc2935fdfd1fa15fce8466'    # 316f7035fded8674d79148a130518ed0
FACEBOOK_GRAPH_API = 'https://graph.facebook.com/v15.0'
URL_FACEBOOK_GRAPH_API_SEND_MESSAGE = 'https://graph.facebook.com/me/messages'
PROFILE_USER_FIELDS = 'first_name,last_name,profile_pic,gender,locale,name,email'


# Setup NATs
CHANNELS_SUBSCRIBE = ["hotel.manager.message.receive.*"]
NATS_URL = env("NATS_URL", default="nats://172.24.222.112:4222")


# Setup Redis
REDIS_HOST = env("REDIS_HOST", default="172.19.0.2")
REDIS_PORT = env("REDIS_PORT", default="6379")
REDIS_PASSWORD = env("REDIS_PASSWORD", default="")
REDIS_USER = env("REDIS_USER", default="")
REDIS_DB = env("REDIS_DB", default=1)
