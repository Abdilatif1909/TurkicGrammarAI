from .base import *  # noqa: F403

DEBUG = True
ALLOWED_HOSTS = env_list("ALLOWED_HOSTS", "localhost,127.0.0.1,0.0.0.0")  # noqa: F405
