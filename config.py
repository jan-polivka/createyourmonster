import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'whatevs'

#    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
#            'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://admin:Vs2iezqPNu46y5oEhwiz@database-1.cmvprbv0qsfx.eu-central-1.rds.amazonaws.com:3306/tst' 
    SQLACHEMY_TRACK_MODIFICATIONS = False
