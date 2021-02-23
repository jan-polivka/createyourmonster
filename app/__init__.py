from flask import Flask
from flask_bootstrap import Bootstrap

app = Flask(__name__)

from app import routes #Different URLs that the application implements

boostrap = Bootstrap(app)
