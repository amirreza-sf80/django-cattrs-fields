SECRET_KEY = "django_tests_secret_key"  # noqa: S105
PASSWORD_HASHERS = ("django.contrib.auth.hashers.MD5PasswordHasher",)

# Include `django.contrib.auth` and `django.contrib.contenttypes` for mypy /
# django-stubs.

# See:
# - https://github.com/typeddjango/django-stubs/issues/318
# - https://github.com/typeddjango/django-stubs/issues/534
INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
]

USE_TZ = True
