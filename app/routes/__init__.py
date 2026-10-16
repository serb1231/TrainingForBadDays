from flask import Blueprint

from app.routes.user_routes import user_bp
from app.routes.authenticate import chat_bp

blueprints = [chat_bp]