from reserved import Reserved
from garbage_collector import Garbage_Collector
import sqlite3

class DBUser():
    @staticmethod
    def add_user(user) -> None:
        """Если пользователь нет, то добавляет в базу или же изменяет данные о нём"""
        with sqlite3.connect(f"db/users.db", check_same_thread=False) as con:
            user.name = user.name.replace("'", "`")
            user.name = user.name.replace('"', "`")
            con.cursor().execute(f"INSERT INTO users VALUES('{user.id}', '{user.name}', '{user.username}', '{user.phone}', '{user.lang}', '{user.date_register}', '{user.date_last_action}', '{user.cashback}', '0', '0', '0')")
    @staticmethod
    def delete_user(user_id : int) -> None:
        """Удалить пользователя по id"""
        with sqlite3.connect(f"db/users.db", check_same_thread=False) as con:
            con.cursor().execute(f"DELETE FROM users WHERE id='{user_id}'")
            Garbage_Collector.clear_msg_from_base(user_id)
            Reserved.delete_reserver(user_id)
            #TODO не удаляю из комментов, потому что будет циклический импорт
            #TODO вероятно, надо удалить из order, basket
    @staticmethod
    def load_all_users() -> list:
        """Получить всех пользователей"""
        with sqlite3.connect(f"db/users.db", check_same_thread=False) as con:
            return con.cursor().execute(f"SELECT * FROM [users]").fetchall()
    @staticmethod
    def load_full_data(id : str) -> list:
        """Возвращает язык пользователя"""
        with sqlite3.connect(f"db/users.db", check_same_thread=False) as con:
            return con.cursor().execute(f"SELECT * FROM users WHERE id='{id}'").fetchone()
    @staticmethod
    def load_data(id : str) -> list:
        """Возвращает язык пользователя"""
        with sqlite3.connect(f"db/users.db", check_same_thread=False) as con:
            return con.cursor().execute(f"SELECT phone, lang, date_registed, date_last_action, cashback, buy_all, buy_month, count_buy FROM users WHERE id='{id}'").fetchone()
    @staticmethod
    def change_user_phone_number(id : str, phone : str) -> None:
        """Указать номер телефона пользователя"""
        with sqlite3.connect(f"db/users.db", check_same_thread=False) as con:
            con.cursor().execute(f"UPDATE users SET phone='{phone}' WHERE id='{id}'")
    @staticmethod
    def change_user_name(id : str, name : str) -> None:
        """Указать имя клиента"""
        if isinstance(name, str):
            name = name.replace('"', '`')
            name = name.replace("'", '`')
        with sqlite3.connect(f"db/users.db", check_same_thread=False) as con:
            con.cursor().execute(f"UPDATE users SET name='{name}' WHERE id='{id}'")
    @staticmethod
    def change_language(id : str, lang : str) -> None:
        with sqlite3.connect(f"db/users.db", check_same_thread=False) as con:
            con.cursor().execute(f"UPDATE users SET lang='{lang}' WHERE id='{id}'")
    @staticmethod
    def get_count_buy(user_id : str) -> None:
        """Получить кол-во покупок"""
        with sqlite3.connect(f"db/users.db", check_same_thread=False) as con:
            r = con.cursor().execute(f"SELECT count_buy FROM [users] WHERE id='{user_id}'").fetchone()
            return 0 if r == None else r[0]
    @staticmethod
    def up_count_buy(user_id : str) -> None:
        """увеличение кол-во покупок"""
        with sqlite3.connect(f"db/users.db", check_same_thread=False) as con:
            con.cursor().execute(f"UPDATE [users] SET count_buy=(SELECT count_buy FROM [users] WHERE id='{user_id}')+1 WHERE id='{user_id}'")        
    @staticmethod
    def existing_phone_number(id : str) -> bool:
        """Проверяет, есть ли такой пользователь"""
        with sqlite3.connect(f"db/users.db", check_same_thread=False) as con:
            return True if con.cursor().execute(f"SELECT phone FROM users WHERE id='{id}'").fetchone()[0] != '' else False            
    @staticmethod
    def existing_user(id : str) -> bool:
        """Проверяет, есть ли такой пользователь"""
        with sqlite3.connect(f"db/users.db", check_same_thread=False) as con:
            return True if con.cursor().execute(f"SELECT id FROM users WHERE id='{id}'").fetchone() != None else False
    @staticmethod
    def update_user(user_id : str, username : str, last_date : str) -> None:
        """Обновление данные о пользователе"""
        with sqlite3.connect(f"db/users.db", check_same_thread=False) as con:
            if isinstance(username, str):
                username = username.replace('"', '`')
                username = username.replace("'", '`')
            con.cursor().execute(f"UPDATE users SET username='{username}', date_last_action='{last_date}' WHERE id='{user_id}'")
    @staticmethod
    def get_cashback(user_id : str) -> float:
        """Получить кешбек"""
        with sqlite3.connect(f"db/users.db", check_same_thread=False) as con:
            return con.cursor().execute(f"SELECT cashback FROM [users] WHERE id='{user_id}'").fetchone()[0]
    @staticmethod
    def set_cashback(user_id : str, cashback : float) -> None:
        """Изменение кол-во кешбека"""
        with sqlite3.connect(f"db/users.db", check_same_thread=False) as con:
            con.cursor().execute(f"UPDATE users SET cashback='{cashback}' WHERE id='{user_id}'")
    @staticmethod
    def set_buy_all(user_id : str, buy_all : float) -> None:
        """Изменение кол-во кешбека"""
        with sqlite3.connect(f"db/users.db", check_same_thread=False) as con:
            con.cursor().execute(f"UPDATE users SET buy_all='{buy_all}' WHERE id='{user_id}'")
    @staticmethod
    def set_buy_month(user_id : str, buy_month : float) -> None:
        """Изменение кол-во кешбека"""
        with sqlite3.connect(f"db/users.db", check_same_thread=False) as con:
            con.cursor().execute(f"UPDATE users SET buy_month='{buy_month}' WHERE id='{user_id}'")
    @staticmethod
    def get_user_by_phone_number(user_phone_number : str) -> dict or bool:
        """Получить информацию о пользователе по его номера телефона"""
        with sqlite3.connect(f"db/users.db", check_same_thread=False) as con:
            row = con.cursor().execute(f"SELECT name, username, phone, lang, date_registed, date_last_action, cashback, buy_all, buy_month, count_buy, id FROM [users] WHERE phone='{user_phone_number}'").fetchone()
            if row != None:
                return {
                    "name" : row[0],
                    "username" : row[1],
                    "phone" : row[2],
                    "lang" : row[3],
                    "date_register" : row[4],
                    "date_last_action" : row[5],
                    "cashback" : row[6],
                    "buy_all" : row[7],
                    "buy_month" : row[8],
                    "count_buy" : row[9],
                    "id" : row[10],
                }
            return False
