import sqlite3

class Locator():
    @staticmethod
    def clear(user_id : int) -> None:
        """Очистить локатор"""
        with sqlite3.connect("db/users.db", check_same_thread=False) as con:
            cur = con.cursor()
            if cur.execute(f"SELECT user_id FROM [locator] WHERE user_id = '{user_id}'").fetchone() == None:
                cur.execute(f"INSERT INTO [locator] VALUES('{user_id}', '', '', '')")
            else:
                cur.execute(f"UPDATE [locator] SET category_uid='', subcategory_uid='', food_uid='' WHERE user_id='{user_id}'")
    @staticmethod
    def set_category(user_id : str, category_uid : str) -> None:
        """Указать категорию"""
        with sqlite3.connect("db/users.db", check_same_thread=False) as con:
            cur = con.cursor()
            cur.execute(f"UPDATE [locator] SET category_uid='{category_uid}' WHERE user_id='{user_id}'")
            cur.execute(f"UPDATE [locator] SET subcategory_uid='' WHERE user_id='{user_id}'")            
    @staticmethod
    def set_subcategory(user_id : str, category_uid : str) -> None:
        """Указать подкатегорию"""
        with sqlite3.connect("db/users.db", check_same_thread=False) as con:
            con.cursor().execute(f"UPDATE [locator] SET subcategory_uid='{category_uid}' WHERE user_id='{user_id}'")
    @staticmethod
    def set_food(user_id : str, category_uid : str) -> None:
        """Указать блюдо"""
        with sqlite3.connect("db/users.db", check_same_thread=False) as con:
            con.cursor().execute(f"UPDATE [locator] SET food_uid='{category_uid}' WHERE user_id='{user_id}'")
    @staticmethod
    def get_locator(user_id : str) -> None:
        """Указать блюдо"""
        with sqlite3.connect("db/users.db", check_same_thread=False) as con:
            res = con.cursor().execute(f"SELECT * FROM [locator] WHERE user_id='{user_id}'").fetchone()
            return {
                "category_uid" : res[1],
                "subcategory_uid" : res[2],
                "food_uid" : res[3],
            }
    @staticmethod
    def get_category(user_id : str) -> None:
        """Получить категорию"""
        with sqlite3.connect("db/users.db", check_same_thread=False) as con:
            return con.cursor().execute(f"SELECT category_uid FROM [locator] WHERE user_id='{user_id}'").fetchone()[0]
    @staticmethod
    def get_subcategory(user_id : str) -> None:
        """Получить подкатегорию"""
        with sqlite3.connect("db/users.db", check_same_thread=False) as con:
            return con.cursor().execute(f"SELECT subcategory_uid FROM [locator] WHERE user_id='{user_id}'").fetchone()[0]
    @staticmethod
    def get_food(user_id : str) -> None:
        """Получить блюдо"""
        with sqlite3.connect("db/users.db", check_same_thread=False) as con:
            return con.cursor().execute(f"SELECT food_uid FROM [locator] WHERE user_id='{user_id}'").fetchone()[0]