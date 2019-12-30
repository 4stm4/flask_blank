"""Обработчик request запросов"""
import json
from json.decoder import JSONDecodeError
from loguru import logger
from requests import post, get
from ..modules.json_valid import message_form
from .urls import URLS

def api_handler(action: str, url: str, *args, **kwargs):
    """ Метод обработки request запросов
    """
    if args:
        query = URLS[url] % args[0]
    else:
        query = URLS[url]
    if kwargs:
        data = kwargs.get('data', '{}')
    else:
        data = {}
    if action == 'get':
        responce = get(query, data=data)
    if action == 'post':
        responce = post(query, data=data)
    if  responce.status_code != 200:
        logger.critical('URL: {}. ERROR: {}'.format(query, responce.status_code))
        return message_form(False, False, 'URL: {}. ERROR: {}'.format(query, responce.status_code))
    try:
        data = json.loads(responce.text)
    except JSONDecodeError:
        return message_form(False, False, 'JSON error.')
    return message_form(False, True, '', result=data)
