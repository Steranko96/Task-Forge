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
