from flask import Flask

from app.routes import blueprints
from app.routes.user_routes import user_bp

def create_app():
    app = Flask(__name__)

    for  blueprint in blueprints:
        app.register_blueprint(blueprint)

    return app