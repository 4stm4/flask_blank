""" JSON валидатор с формированием ответа """
import json
import decimal
from json.decoder import JSONDecodeError
from .errors import ERR_LIST

class DatetimeEncoder(json.JSONEncoder):
    """ Распаковка даты и времени"""
    def default(self, obj): # pylint: disable=E0202
        try:
            return super(DatetimeEncoder, obj).default(obj)
        except TypeError:
            return str(obj)

def decimal_default(obj):
    """ Данные типа decimal """
    if isinstance(obj, decimal.Decimal):
        return float(obj)
    raise TypeError

def integer_default(obj):
    """ Данные типа int """
    if isinstance(obj, decimal.Decimal):
        return int(obj)
    raise TypeError


def message_form(json_: bool, success: bool, message: str, **kwargs):
    """ формирование ответа типа dict или json """
    type_data = None
    if 'default' in kwargs:
        type_data = kwargs.pop('default')
    result = dict(**{'success':success, 'message':message}, **kwargs)
    if json_:
        if type_data == 'int':
            return json.dumps(result, ensure_ascii=False, cls=DatetimeEncoder,
                              default=integer_default)
        if type_data == 'dec':
            return json.dumps(result, ensure_ascii=False, cls=DatetimeEncoder,
                              default=decimal_default)
        return json.dumps(result, ensure_ascii=False, cls=DatetimeEncoder)
    return result

def check_json(request_data, *args):
    """ Проверяем JSON на наличие параметров """
    try:
        data_dict = json.loads(request_data)
    except JSONDecodeError:
        return message_form(False, False, 'JSON error.')
    param_list = [par for par in args if par not in data_dict]
    if param_list:
        return message_form(False, False, ERR_LIST['no_params'].format(param_list))
    return message_form(False, True, '', result=tuple(data_dict[par] for par in args))

def check_options(request_data, default, *args):
    """ Проверяем JSON на наличие опций """
    try:
        data_dict = json.loads(request_data)
    except JSONDecodeError:
        return message_form(False, False, 'JSON error.')
    options_list = [par for par in args if par not in data_dict]
    for opt in options_list:
        data_dict[opt] = default
    return message_form(False, True, '', result=tuple(data_dict[par] for par in args))