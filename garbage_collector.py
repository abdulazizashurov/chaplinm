from telebot import TeleBot
import sqlite3

class Garbage_Collector():
    """Класс, собирающий мусор и очищяющий"""
    @staticmethod
    def add_garbage(user_id : str, msg_id : str) -> None:
        """Зафиксировать мусор"""
        with sqlite3.connect(f"db/garbare_collector.db", check_same_thread=False) as con:
            con.cursor().execute(f"INSERT INTO [garbage_collector] VALUES('{user_id}', '{msg_id}')")
    @staticmethod
    def add_garbage_commid(user_id : str, msg_id : str) -> None:
        """Зафиксировать мусор и сразу применяет"""
        with sqlite3.connect(f"db/garbare_collector.db", check_same_thread=False) as con:
            con.cursor().execute(f"INSERT INTO [garbage_collector] VALUES('{user_id}', '{msg_id}')")
    @staticmethod
    def clear_msg_from_base(id : str) -> None:
        """Удалить сообщения из базы"""
        with sqlite3.connect(f"db/garbare_collector.db", check_same_thread=False) as con:
            con.cursor().execute(f"DELETE FROM [garbage_collector] WHERE user_id='{id}'")
    @staticmethod
    def Clear(bot : TeleBot, id : str) -> None:
        """Очищяем экран"""
        with sqlite3.connect(f"db/garbare_collector.db", check_same_thread=False) as con:
            cur = con.cursor()
            for mid in cur.execute(f"SELECT msg_id FROM [garbage_collector] WHERE user_id='{id}'").fetchall():
                try:
                    bot.delete_message(id, mid[0])
                except:
                    continue
            cur.execute(f"DELETE FROM [garbage_collector] WHERE user_id='{id}'")