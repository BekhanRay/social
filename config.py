from decouple import config

SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG')

# POSTGRES_DB = config('POSTGRES_DB')
# POSTGRES_USER = config('POSTGRES_USER')
# POSTGRES_PASSWORD = config('POSTGRES_PASSWORD', cast=int)
# POSTGRES_HOST = config('POSTGRES_HOST')
# POSTGRES_PORT = config('POSTGRES_PORT', cast=int)

# EMAIL

# EMAIL_BACKEND = config('EMAIL_BACKEND')
# EMAIL_HOST = config('EMAIL_HOST')
# EMAIL_PORT = config('EMAIL_PORT')
# EMAIL_USE_SSL = config('EMAIL_USE_SSL')
# EMAIL_HOST_USER = config('EMAIL_HOST_USER')
# EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
# DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL')
# SERVER_EMAIL = config('SERVER_EMAIL')

DEBUG = config('DEBUG')

