import os

class Config:
    QUOTE_API_BASE_URL='http://quotes.stormconsultancy.co.uk/random.json'
    SECRET_KEY = '6a5b826c18f5db76e78adf63ecd0af76'
    UPLOADED_PHOTOS_DEST ='app/static/photos'
        #  email configurations
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")


    # simple mde  configurations
    SIMPLEMDE_JS_IIFE = True
    SIMPLEMDE_USE_CDN = True
    
class ProdConfig(Config):
    
  #  SQLALCHEMY_DATABASE_URI = 'postgres://acwlugsmzrivlo:10d797150cae07af83bde7f55358625dbf4a75e8b1b6a3742c83125bc0bec29d@ec2-107-22-245-82.compute-1.amazonaws.com:5432/ddju05pm0hvkn3'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL').replace("://", "ql://", 1)
     

class TestConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://kagus:Muraya11$@localhost/blogspot_test'
    

class DevConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://kagus:Muraya11$@localhost/blogspot'
    DEBUG = True

config_options = {
    'development': DevConfig,
    'production': ProdConfig,
    'test': TestConfig
}