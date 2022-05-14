import sqlite3
import food


def add_food(user_id : str, category_uid : str, food_uid : str, count : int, price : int) -> None:
    """Добавление товара в корзину"""
    with sqlite3.connect("db/basket.db", check_same_thread=False) as con:
        cur = con.cursor()
        if cur.execute(f"SELECT food_uid FROM [basket] WHERE food_uid='{food_uid}' AND user_id='{user_id}'").fetchone() == None:
            cur.execute(f"INSERT INTO [basket] VALUES('{user_id}', '{category_uid}', '{food_uid}', '{count}', '{price}')")

def clear_basket(user_id : str) -> None:
    """Очистить корзицу"""
    with sqlite3.connect("db/basket.db", check_same_thread=False) as con:
        con.execute(f"DELETE FROM [basket] WHERE user_id='{user_id}'")

def get_foods_in_basket(user_id : str) -> list:
    """Получить из корзины"""
    res = []
    with sqlite3.connect("db/basket.db", check_same_thread=False) as con:
        for row in con.execute(f"SELECT category_uid, food_uid, count, price FROM [basket] WHERE user_id='{user_id}'").fetchall():
            res.append({
                "category_uid" : row[0],
                "food_uid" : row[1],
                "count": row[2],
                "price" : row[3]
            })
    return res
def get_count(user_id : str, food_uid : str) -> int:
    """Получить кол-во"""
    with sqlite3.connect("db/basket.db", check_same_thread=False) as con:
        return con.execute(f"SELECT count FROM [basket] WHERE user_id='{user_id}' AND food_uid='{food_uid}'").fetchone()[0]
def set_new_count(user_id : str, food_uid : str, count : str) -> None:
    """Изменение кол-во"""
    with sqlite3.connect("db/basket.db", check_same_thread=False) as con:
        con.execute(f"UPDATE [basket] SET count='{count}' WHERE user_id='{user_id}' AND food_uid='{food_uid}'")
def delete_from_basket(user_id : str, food_uid : str) -> None:
    """Удаление из корзины"""
    with sqlite3.connect("db/basket.db", check_same_thread=False) as con:
        con.execute(f"DELETE FROM [basket] WHERE user_id='{user_id}' AND food_uid='{food_uid}'")    

def get_foods_uid(user_id : str) -> list:
    """Получить из корзины, только uid"""
    res = []
    with sqlite3.connect("db/basket.db", check_same_thread=False) as con:
        for row in con.execute(f"SELECT food_uid FROM [basket] WHERE user_id='{user_id}'").fetchall():
            res.append(row[0])
    return res