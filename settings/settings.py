DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'sqlite.db',
    }
}

INSTALLED_APPS = (
    'parse',
    'proxy'
    )

SECRET_KEY = 'REPLACE_ME'
