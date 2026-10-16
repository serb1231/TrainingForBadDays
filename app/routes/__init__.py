from flask import Blueprint

from app.routes.user_routes import user_bp
from app.routes.authenticate import send_request, get_history, clear_history

blueprints = [send_request, get_history, clear_history]