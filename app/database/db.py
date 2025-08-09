""" Модуль работы с базой данных """
import mysql.connector
from mysql.connector import MySQLConnection
from mysql.connector.cursor import MySQLCursorDict
from typing import Any, Optional, Union, List, Dict
from loguru import logger
from .queries import QUERIES
from ..config import SERVER_DB_LK

class StaticConnection():
    """ Соединение с БД """
    def __init__(self):
        self.conn: Optional[MySQLConnection] = None
    
    def get_connection(self) -> MySQLConnection:
        """ Подключение """
        if self.conn is None or not self.conn.is_connected():
            self.__connect()
        return self.conn
    
    def __connect(self) -> None:
        self.conn = mysql.connector.connect(**SERVER_DB_LK)
        self.conn.autocommit = False

CNN = StaticConnection()

def sql_handler(
    action: str, 
    query_name: str, 
    *args: Any
) -> Union[Dict[str, Any], List[Dict[str, Any]], int, None]:
    """ Обработчик SQL запросов """
    res = None
    cn = None
    cur = None
    
    try:
        cn = CNN.get_connection()
        cur = cn.cursor(dictionary=True, buffered=True)
        
        if args:
            cur.execute(QUERIES[query_name], args)
        else:
            cur.execute(QUERIES[query_name])
            
        if action == 'select_one':
            row = cur.fetchall()
            res = row[0] if row else None
        elif action == 'select_all':
            res = cur.fetchall()
        elif action in ('insert', 'update'):
            cn.commit()
            res = cur.lastrowid
            
    except mysql.connector.Error as err:
        logger.exception(f"SQL '{query_name}' error: {err}")
        if cn and action in ('insert', 'update'):
            cn.rollback()
    finally:
        if cur:
            cur.close()
    return res
