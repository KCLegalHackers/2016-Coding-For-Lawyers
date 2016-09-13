from flask import Flask


app = Flask(__name__)
app.config.from_object('config')


# imports really needed even though pycharm doesn't think so:
from app import views