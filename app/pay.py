"""Модуль с API методами"""
from flask import Blueprint, request
from modules.router import ROUTERS
from .database.db import sql_handler
from .modules.json_valid import check_json, message_form
from .requests.rest import api_handler
from .modules.errors import ERR_LIST

BP_PAY = Blueprint('pay', __name__)

@BP_PAY.route(ROUTERS['example']['name'], methods=['POST'] )
def example():
    responce = check_json(request.data, *ROUTERS['example']['parameters'])
    if not responce['success']:
        return message_form(True, False, responce['message'])
    all_data = sql_handler('select_all', 'select_all_data',
                           (responce['result'],))
    if not all_data:
        return message_form(True, False, ERR_LIST['db_error'])
    return message_form(True, True, '', data=all_data)