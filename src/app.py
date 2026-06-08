from flask import Flask
from src.routes import deliver_bp

def create_app():
    app = Flask(__name__)
    app.register_blueprint(deliver_bp)
    return app
