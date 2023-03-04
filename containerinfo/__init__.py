from flask import Flask
from config import Config

containerapp = Flask(__name__)
containerapp.config.from_object(Config)

from containerinfo import routes