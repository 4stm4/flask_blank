""" Модуль работы с базой данных """
import mysql.connector
from loguru import logger
from .queries import QUERIES
from ..config import SERVER_DB_LK

class StaticConenction():
    """ Соединение с БД
    """
    def __init__(self):
        self.conn = None
    def getConnection(self):
        """ Подключение """
        if self.conn is None or not self.conn.is_connected():
            self.__connect()
        return self.conn
    def __connect(self):
        self.conn = mysql.connector.connect(**SERVER_DB_LK)

CNN = StaticConenction()

def sql_handler(action: str, query_name: str, *args):
    """ Обработчик SQL запросов
    """
    res = None
    if args:
        query = QUERIES[query_name] % args[0]
    else:
        query = QUERIES[query_name]
    try:
        cn = CNN.getConnection()
        cur = cn.cursor(dictionary=True, buffered=True)
        cur.execute(query)
        if action == 'select_one':
            row = cur.fetchall()
            if row:
                res = row[0]
        if action == 'select_all':
            res = cur.fetchall()
        if action in ('insert','update'):
            cn.commit()
            res = cur.lastrowid
    except mysql.connector.Error as err:
        logger.exception("SQL '{}' error: {}".format(query_name, err))
    finally:
        if cur:
            cur.close()
        if cn:
            cn.close()
    return res
