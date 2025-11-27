class Config:
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class LocalDevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///parkingDb.sqlite3'
    JWT_SECRET_KEY = 'jwt_secret_key'
    CACHE_TYPE = "RedisCache"
    CACHE_REDIS_URL = "redis://localhost:6379/0"
    CACHE_DEFAULT_TIMEOUT = 300
    
    # MailHog Configuration
    MAIL_SERVER = 'localhost'
    MAIL_PORT = 1025
    MAIL_USE_TLS = False
    MAIL_USE_SSL = False