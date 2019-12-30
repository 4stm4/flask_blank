""" Модуль с настройками Сервера ЛК """
from flask import Flask

APP = Flask(__name__)
with APP.app_context():
    APP.config.from_pyfile('../config.ini')
    LOGFL = APP.config['LOGFILE']
    PORT = APP.config['PORT']

    SERVER_DB_LK = {
        'host'   : APP.config['HOST_LK'],
        'user'   : APP.config['USER_LK'],
        'passwd' : APP.config['PSWD_LK'],
        'db'     : APP.config['DBASE_LK']
    }
