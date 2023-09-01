import os


class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'postgres://ourenboku:0IywhTXEJKBLZFMmJFFWEygWipodPhin@dpg-cjo8d7j6fquc73fmjir0-a.singapore-postgres.render.com/aigo_fpk5'


class ProdConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
