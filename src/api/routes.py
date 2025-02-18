from flask import Flask
from .endpoints import register_endpoints

def create_app():
    app = Flask(__name__)
    register_endpoints(app)
    return app
