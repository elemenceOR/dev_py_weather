#initialize flask app by creating the app, importing configs and blueprints


from flask import Flask
from app.config import Config

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    from app.routes import main_blueprint
    app.register_blueprint(main_blueprint)

    return app