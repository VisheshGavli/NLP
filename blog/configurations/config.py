import os

#print(os.environ.get('SQLALCHEMY_DATABASE_URI')+'test.db')

class Config:

    '''
    For ease of execution and evaluation , below configurations are hard-coded.
    Usually these parameters would be set at OS level environment settings and would be read
    as below
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')+'site.db'
    '''

    SECRET_KEY = ''
    SQLALCHEMY_DATABASE_URI = 'sqlite:///database//site.db'
