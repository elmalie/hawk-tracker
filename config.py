from decouple import config


ADMIN_PASSWORD = config('ADMIN_PASSWORD')
DB_PASSWORD = config('DB_PASSWORD')

DB_USER = config('DB_USER')
DB_NAME = config('DB_NAME')

DEV_DB_USER = config('DEV_DB_USER')
DEV_DB_NAME = config('DEV_DB_NAME')

try:
    FLASK_ENV = config('FLASK_ENV')
except Exception as e:
    FLASK_ENV = 'production'
