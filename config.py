from decouple import config

SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG')

# POSTGRES_DB = config('POSTGRES_DB')
# POSTGRES_USER = config('POSTGRES_USER')
# POSTGRES_PASSWORD = config('POSTGRES_PASSWORD', cast=int)
# POSTGRES_HOST = config('POSTGRES_HOST')
# POSTGRES_PORT = config('POSTGRES_PORT', cast=int)

# EMAIL

EMAIL_HOST = config('EMAIL_HOST')
EMAIL_PORT = config('EMAIL_PORT')
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
EMAIL_USE_SSL = config('EMAIL_USE_SSL')
