import os
import ast

# config function: check DEBUG
def check_debug(DEBUG, app_env):

    if DEBUG is None or DEBUG.lower() not in ('true', 'false'):
        raise ValueError("DEBUG must be 'true' or 'false'")

    debug_enabled = DEBUG.lower() == 'true'

    if app_env == 'production' and debug_enabled:
        raise ValueError("DEBUG must be False when APP_ENV=production")

    return debug_enabled



# config function: check APP_ENV
def check_env(APP_ENV):

    if APP_ENV is None:
        raise ValueError(f"Invalid config value: [APP_ENV]={type(APP_ENV)}")

    elif APP_ENV.lower() not in ('development', 'production'):
         raise ValueError(f"Invalid config value: [APP_ENV]={APP_ENV}")

    return APP_ENV.lower()

# config function: check SECRET_KEY
def check_secret_key(SECRET_KEY):
    placeholders = ['change-me']
    if SECRET_KEY is None or SECRET_KEY == "" or SECRET_KEY in placeholders:
        raise ValueError('SECRET_KEY is not valid')

    return SECRET_KEY

# config function: parse ALLOWED_HOSTS
def parse_allowed_hosts(allowed_host):

    if allowed_host is None or len(allowed_host) == 0:
        raise ValueError('ALLOWED_HOSTS must not be None or empty')

    clean_list = []
    for host in allowed_host.split(","):
        host = host.strip()
        if host == '':
            raise ValueError("host cannot be ''")
        clean_list.append(host)

    return clean_list

def database_selection(app_env, base_dir):
    if app_env is None:
        raise ValueError("DB setting cannot be None")

    elif app_env == 'production':

        prod_settings = {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME':     os.getenv("DB_NAME"),
            'USER':     os.getenv("DB_USER"),
            'PASSWORD': os.getenv("DB_PASSWORD"),
            'HOST':     os.getenv("DB_HOST"),
            'PORT':     os.getenv("DB_PORT")
        }

        for key in prod_settings:
            if prod_settings[key] is None:
                raise ValueError(f'DB setting {key} cannot be none')
            elif prod_settings[key] == "":
                raise ValueError(f'DB setting {key} cannot be ""')


        return prod_settings
    else:
        development_settings = {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': base_dir / 'db.sqlite3',
        }

        return development_settings
