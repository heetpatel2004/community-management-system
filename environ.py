"""
A minimal shim for django-environ used during builds.
This provides enough functionality for the project's settings to run
when the django-environ package isn't yet available in the environment.

This is a temporary workaround; remove this file once builds consistently
install the real django-environ package.
"""
import os
import urllib.parse

class Env:
    def __init__(self, **defaults):
        # defaults: NAME=(type, default)
        self._defaults = {k: v for k, v in defaults.items()}

    def __call__(self, key, default=None):
        val = os.environ.get(key, None)
        if val is None:
            # If a default was provided in the Env(...) call, use it
            if key in self._defaults:
                typ, dflt = self._defaults[key]
                return dflt if dflt is not None else default
            return default
        return val

    def int(self, key, default=None):
        v = self(key, default)
        try:
            return int(v)
        except Exception:
            return default

    def bool(self, key, default=False):
        v = self(key, None)
        if v is None:
            return default
        if isinstance(v, bool):
            return v
        return str(v).lower() in ("1", "true", "yes", "on")

    def list(self, key, default=None):
        v = self(key, None)
        if v is None:
            return default if default is not None else []
        if isinstance(v, (list, tuple)):
            return list(v)
        return [p.strip() for p in str(v).split(',') if p.strip()]

    def db(self, key):
        # Very small DATABASE_URL parser for postgres/mysql/sqlite
        val = self(key, None)
        if not val:
            raise KeyError("DATABASE_URL not set")
        url = urllib.parse.urlparse(val)
        scheme = url.scheme
        if scheme.startswith('postgres') or scheme.startswith('postgresql'):
            engine = 'django.db.backends.postgresql'
        elif scheme.startswith('mysql'):
            engine = 'django.db.backends.mysql'
        elif scheme.startswith('sqlite'):
            engine = 'django.db.backends.sqlite3'
        else:
            engine = 'django.db.backends.postgresql'

        # path may start with /dbname
        name = url.path[1:] if url.path and url.path.startswith('/') else url.path
        user = urllib.parse.unquote(url.username) if url.username else ''
        password = urllib.parse.unquote(url.password) if url.password else ''
        host = url.hostname or ''
        port = str(url.port) if url.port else ''

        if engine == 'django.db.backends.sqlite3':
            # sqlite URL like sqlite:///full/path/to/db.sqlite3
            return {
                'ENGINE': engine,
                'NAME': name or ':memory:',
            }

        return {
            'ENGINE': engine,
            'NAME': name,
            'USER': user,
            'PASSWORD': password,
            'HOST': host,
            'PORT': port,
        }

    @staticmethod
    def read_env(path):
        # Very small .env reader: lines like KEY=VALUE, skip comments
        try:
            with open(path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith('#'):
                        continue
                    if '=' not in line:
                        continue
                    k, v = line.split('=', 1)
                    k = k.strip()
                    v = v.strip().strip('"')
                    # Only set if not already present in environment
                    if k and k not in os.environ:
                        os.environ[k] = v
        except FileNotFoundError:
            return

# Provide a convenience constructor like django-environ
def Env_factory(**defaults):
    return Env(**defaults)

# Keep compatibility: project expects environ.Env
Env = Env

# Module-level alias (django-environ exposes Env class)

# End of shim
