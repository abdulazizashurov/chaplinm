import sqlite3
from utils import Utils
from user import User
class History():
    @staticmethod
    def add_history(order_number : int, client_id : str, name : str, cost : int, order : str, payment_method : str, dilivery_method : str) -> None:
        """запись данных в историю"""
        with sqlite3.connect("db/history.db", check_same_thread=False) as con:
            if isinstance(order, str):
                order = order.replace("'", '`')
                order = order.replace('"', '`')
            con.cursor().execute(f"INSERT INTO [history] VALUES('{order_number}', '{client_id}', '{name}', '{Utils.get_date()}', '{cost}', '{order}', '{payment_method}', '{dilivery_method}')")
    @staticmethod
    def get_histories(date_from : str, date_to : str) -> None:
        """Экспорт истории покупок"""
        sql = "SELECT name, [order], date, cost, payment_method, dilivery_method FROM [history]"
        use_filial = False
        if date_from != '*' or date_to != '*':
            sql += " WHERE"
        if date_from != "*" and date_to != '*':
            sql += " AND " if use_filial else " "
            sql += f" date >= '{date_from}' AND date <= '{date_to}'"
        elif date_from != '*' and date_to == '*':
            sql += " AND " if use_filial else " " 
            sql += f" date >= '{date_from}' "
        elif date_from == '*' and date_to != '*':
            sql += " AND " if use_filial else " " 
            sql += f" date <= '{date_to}' "
        with sqlite3.connect("db/history.db") as con:
            return con.cursor().execute(sql).fetchall()