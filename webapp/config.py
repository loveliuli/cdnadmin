class Config(object):
    SECRET_KEY = '736670cb10a600b695a55839ca3a5aa54a7d7356cdef815d2ad6e19a2031182b'
    RECAPTCHA_PUBLIC_KEY = "6LdY-RkUAAAAAJmnaYfLWuoWaFe-S97ES28mCHA2"
    RECAPTCHA_PRIVATE_KEY = '6LdY-RkUAAAAAC_9-pCchurb-GkYcu-4BOC-3K3X'


class ProdConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///database.db'


class DevConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///database.db'
    CELERY_BROKER_URL = "amqp://guest:guest@localhost:5672//"
    CELERY_BACKEND_URL = "amqp://guest:guest@localhost:5672//"
