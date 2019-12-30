"""Модуль инициализации приложения"""
from loguru import logger
from flask import Flask
from .config import LOGFL
from . import pay

logger.add(LOGFL, format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}")

def create_app():
    """Создаются подпрограммы
    """
    app = Flask(__name__)
    with app.app_context():
        app.register_blueprint(pay.BP_PAY)
        return app
