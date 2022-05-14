import sqlite3

from telebot import TeleBot
from utils import Utils
import uuid
import config

class Order():
    @staticmethod
    def add_order(order_number : int, user_id : str, user_name : str, cost : int, order : str, 
            payment_method : str, dilivery_method : str, filial : int, cost_withoud_dilivery : int, 
            location : str, comment : str) -> None:
        """запись данных в заказы"""
        with sqlite3.connect("db/order.db", check_same_thread=False) as con:
            comment = comment.replace("'", "`")
            order = order.replace("'", "`")
            user_name = user_name.replace("'", "`")
            comment = comment.replace('"', "`")
            order = order.replace('"', "`")
            user_name = user_name.replace('"', "`")   
            con.cursor().execute(f"INSERT INTO [order] VALUES('{uuid.uuid4()}', '{order_number}', '{user_id}', '{user_name}', '{Utils.get_date()}', '{cost}', '{order}', '{payment_method}', '{dilivery_method}', ' ', '{filial}', '{cost_withoud_dilivery}', '{location}', '{comment}')")
    @staticmethod
    def clear_order(order_uid : str) -> None:
        """Удаление данные о заказов"""
        with sqlite3.connect("db/order.db", check_same_thread=False) as con:
            con.cursor().execute(f"DELETE FROM [order] WHERE order_uid='{order_uid}'")
    @staticmethod
    def set_payment_message_id(user_id : str, payment_message_id : str) -> None:
        """Установить id сообщения оплаты"""
        with sqlite3.connect("db/order.db", check_same_thread=False) as con:
            con.cursor().execute(f"UPDATE [order] SET payment_message_id='{payment_message_id}' WHERE user_id='{user_id}'")
    @staticmethod
    def get_order(user_id : str) -> dict:
        """Получаем номер заказа"""
        with sqlite3.connect("db/order.db", check_same_thread=False) as con:
            return con.cursor().execute(f"SELECT order_number, order_text, payment_method, dilivery_method, cost_without_dilivery, fillial, location, comment FROM [order] WHERE order_uid='{user_id}' ").fetchone()
    @staticmethod
    def get_active_number() -> int:
        """Получение активного номера"""
        with sqlite3.connect("db/order.db", check_same_thread=False) as con:
            return con.cursor().execute(f"SELECT order_number FROM [number]").fetchone()[0]
    @staticmethod
    def inc_active_number() -> None:
        """Увеличение номера заказа"""
        with sqlite3.connect("db/order.db", check_same_thread=False) as con:
            con.cursor().execute("UPDATE [number] SET order_number=(SELECT order_number FROM [number])+1")
    @staticmethod
    def get_order_uid(user_id : str) -> None:
        """Получить номер ордена"""
        with sqlite3.connect("db/order.db", check_same_thread=False) as con:
            return con.cursor().execute(f"SELECT order_uid FROM [order] WHERE user_id='{user_id}' AND rowid=(SELECT MAX(rowid) FROM [order])").fetchone()[0]
    @staticmethod
    def get_data(user_id : str) -> None:
        """Получить данные заказа"""
        with sqlite3.connect("db/order.db", check_same_thread=False) as con:
            return con.cursor().execute(f"SELECT cost, order_text, payment_method, dilivery_method, order_number, user_id, name FROM [order] WHERE order_uid='{user_id}'").fetchone()
    @staticmethod
    def get_user_id(order_uid : str) -> None:
        with sqlite3.connect("db/order.db", check_same_thread=False) as con:
            return con.cursor().execute(f"SELECT user_id FROM [order] WHERE order_uid='{order_uid}'").fetchone()[0]
    @staticmethod
    def add_message(user_id : str, message_id : str, message_text : str) -> None:
        """Добавление id сообщения, для его удаления"""
        with sqlite3.connect("db/order.db", check_same_thread=False) as con:
            message_text = message_text.replace("'", "`")
            message_text = message_text.replace('"', "`")
            con.cursor().execute(f"INSERT INTO [messages_id] VALUES('{user_id}', '{message_id}', '{message_text}')")
    @staticmethod
    def get_message_data(order_uid : str) -> str:
        """Получить ид сообщения"""
        with sqlite3.connect("db/order.db", check_same_thread=False) as con:
            return con.cursor().execute(f"SELECT message_id, message_text FROM [messages_id] WHERE order_uid='{order_uid}'").fetchone()
    @staticmethod
    def clear_message_id(order_uid : str) -> None:
        """удаление сообщения"""
        with sqlite3.connect("db/order.db", check_same_thread=False) as con:
            con.cursor().execute(f"DELETE FROM [messages_id] WHERE order_uid='{order_uid}'")
    @staticmethod
    def set_order_status(bot : TeleBot, order_uid : str, status : str) -> None:
        """Установить статус заказа"""
        data = Order.get_message_data(order_uid)
        bot.edit_message_text(f'{data[1]}\r\n{status}', config.CHANEL, data[0], reply_markup=None)
        Order.clear_message_id(order_uid)
    @staticmethod
    def set_order_comment(user_id : str, comment : str) -> None:
        """Установить комментарий"""
        if len(comment) > 1024:
            comment = comment[0:1024]
        comment = comment.replace("'", '~')
        comment = comment.replace('"', '~')
        with sqlite3.connect("db/order.db", check_same_thread=False) as con:
            cur = con.cursor()
            if cur.execute(f"SELECT user_id FROM  [order_comment] WHERE user_id='{user_id}'").fetchone() == None:
                cur.execute(f"INSERT INTO [order_comment] VALUES('{user_id}', '{comment}')")
            else:
                cur.execute(f"UPDATE [order_comment] SET comment='{comment}' WHERE user_id='{user_id}'")
    @staticmethod
    def get_order_comment(user_id) -> str:
        """Получить комментарий"""
        with sqlite3.connect("db/order.db", check_same_thread=False) as con:
            r = con.cursor().execute(f"SELECT comment FROM [order_comment] WHERE user_id='{user_id}'").fetchone()
            return r[0].replace("~", "'") if r != None else "[no_comment]"
    @staticmethod
    def delete_comment(user_id) -> str:
        """Удалить комментарий"""
        with sqlite3.connect("db/order.db", check_same_thread=False) as con:
            con.cursor().execute(f"DELETE FROM [order_comment] WHERE user_id='{user_id}'")