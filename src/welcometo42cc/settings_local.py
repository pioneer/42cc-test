DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Serge Tarkovski', 'serge.tarkovski@gmail.com'),
)

MANAGERS = ADMINS

DATABASE_ENGINE = 'sqlite3'
DATABASE_NAME = '42cc.db'
DATABASE_USER = '42cc'
DATABASE_PASSWORD = ''
DATABASE_HOST = 'localhost'
DATABASE_PORT = ''

#Mail settings
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'serge.tarkovski@gmail.com'
EMAIL_HOST_PASSWORD = '******'
EMAIL_USE_TLS = True
