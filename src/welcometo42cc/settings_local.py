DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Serge Tarkovski', 'serge.tarkovski@gmail.com'),
)

MANAGERS = ADMINS

DATABASE_ENGINE = 'sqlite3'           # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
DATABASE_NAME = '42cc.db'             # Or path to database file if using sqlite3.
DATABASE_USER = '42cc'                # Not used with sqlite3.
DATABASE_PASSWORD = ''                # Not used with sqlite3.
DATABASE_HOST = 'localhost'           # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT = ''                    # Set to empty string for default. Not used with sqlite3.

#Mail settings
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'serge.tarkovski@gmail.com'
EMAIL_HOST_PASSWORD = '******'
EMAIL_USE_TLS = True
