import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    """ Parent configuration class."""
    MAIL_SERVER = os.getenv('MAIL_SERVER')
    MAIL_PORT = os.getenv('MAIL_PORT')
    MAIL_USE_TLS = os.getenv('MAIL_USE_TLS')
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    DEBUG = False 
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')

class DevelopmentConfig(Config):
    """ Configurations for Development."""
    DEBUG = True
    SECRET_KEY = os.getenv('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    # SQLALCHEMY_DATABASE_URI = postgres_local_base + database_name

class TestingConfig(Config):
    """ Configurations for Testing, with a separate test database."""
    TESTING = True
    DEBUG = True
    SECRET_KEY = os.getenv('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.getenv('TEST_DB_URL')

class StagingConfig(Config):
    """ Configurations for Staging."""
    DEBUG = True

class ProductionConfig(Config):
    """ Configurations for Production."""
    SECRET_KEY = os.getenv('SECRET_KEY')
    DEBUG = False
    TESTING = False

app_config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'staging': StagingConfig,
    'production': ProductionConfig,
}