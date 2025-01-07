from flask import Flask
from flask_pymongo import PyMongo
import os

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get('SECRET_KEY', 'default_secret_key')
app.config["MONGO_URI"] = os.environ.get('MONGO_URI', 'mongodb+srv://Rutuj:Capcap3942@cluster0.xuw7x.mongodb.net/todo_db?retryWrites=true&w=majority&appName=Cluster0')

mongodb_client = PyMongo(app)
db = mongodb_client.db

from application import routes
