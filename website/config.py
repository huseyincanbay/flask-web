import os

#flask configuration

DEBUG = True
SECRET_KEY = 'mySecretKey'

#sql alchemy configuration
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root@localhost/mechsoft'
SQLALCHEMY_TRACK_MODIFICATIONS = False
