""" Модуль содержит описание всех путей API """
import json
from flask import Blueprint

BP_ROUTER = Blueprint('router', __name__)

ROUTERS = {
        'example'      : {
        'name'      : '/api/example',
        'file_name' : 'pay.py',
        'parameters': ['param1', 'param2'],
        "options": ['option1', 'option2', 'option3']
        }
}

@BP_ROUTER.route('/API')
def get_api():
    """Метод возвращает список всех API и параметров
    """
    return json.dumps(ROUTERS)
