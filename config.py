import os

class Config:
    SECRET_KEY = '6a5b826c18f5db76e78adf63ecd0af76'
    UPLOADED_PHOTOS_DEST ='app/static/photos'
    
class ProdConfig(Config):
    pass

class TestConfig(Config):
    pass

class DevConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://kagus:Muraya11$@localhost/blogspot'
    DEBUG = True

config_options = {
    'development': DevConfig,
    'production': ProdConfig,
    'test': TestConfig
}