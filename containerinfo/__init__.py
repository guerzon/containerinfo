from flask import Flask

containerapp = Flask(__name__)

from containerinfo import routes