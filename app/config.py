import os

class Config:
    """ base configurations """
    SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///flight.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True

class DevelopmentConfig(Config):
    """ Development configuration """
    DEBUG = True
    SQLALCHEMY_ECHO = True

class ProductionConfig(Config):
    """ Production configurations """
    DEBUG = False

class TestingConfig(Config):
    """ Testing configurstions """
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'

config_by_name = {
        'development': DevelopmentConfig,
        'production': ProductionConfig,
        'testing': TestingConfig
        }
