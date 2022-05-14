import sqlite3
import uuid

def set_preview(pizza_uid : str, img_url : str) -> None:
    """Установить превью для пиццы"""
    with sqlite3.connect("db/menu.db") as con:
        con.cursor().execute(f"UPDATE [menu_pizza] SET img='{img_url}' WHERE uid='{pizza_uid}'")
def get_pizza_price(pizza_uid : str, cost_type : str) -> int:
    """Получить стоимость пиццы"""
    with sqlite3.connect("db/menu.db") as con:
        return con.cursor().execute(f"SELECT cost_{cost_type} FROM [menu_pizza] WHERE uid='{pizza_uid}'").fetchone()[0]

def set_pizza_name(pizza_uid : str, name : str, lang : str) -> None:
    """Установить превью для пиццы"""
    with sqlite3.connect("db/menu.db") as con:
        name = name.replace("'", '~')
        con.cursor().execute(f"UPDATE [menu_pizza] SET name_{lang}='{name}' WHERE uid='{pizza_uid}'")
def set_pizza_description(pizza_uid : str, description : str, lang : str) -> None:
    """Установить превью для пиццы"""
    with sqlite3.connect("db/menu.db") as con:
        description = description.replace("'", '~')
        con.cursor().execute(f"UPDATE [menu_pizza] SET description_{lang}='{description}' WHERE uid='{pizza_uid}'")        

def set_pizza_cost(pizza_uid : str, cost : str, type : str) -> None:
    """Установить превью для пиццы"""
    with sqlite3.connect("db/menu.db") as con:
        con.cursor().execute(f"UPDATE [menu_pizza] SET cost_{type}='{cost}' WHERE uid='{pizza_uid}'")   

def delete_pizza(pizza_uid) -> None:
    """Удалить пиццу"""
    with sqlite3.connect("db/menu.db") as con:
        con.cursor().execute(f"DELETE FROM [menu_pizza] WHERE uid='{pizza_uid}'")   

def get_name(food_uid : str) -> dict or None:
    """Получить имя пиццы через uid"""
    with sqlite3.connect("db/menu.db", check_same_thread=False) as con:
        r = con.cursor().execute(f"SELECT name_ru, name_uz, name_en FROM [menu_pizza] WHERE uid='{food_uid}'").fetchone()
        if r != None:
            return {
                "ru" : r[0].replace('~', "'"),
                "uz" : r[1].replace('~', "'"),
                "en" : r[2].replace('~', "'"),
            }
        return None

def get_pizza_list(lang : str) -> list:
    """Получить список пиццы"""
    res = []
    with sqlite3.connect("db/menu.db") as con:
        for pizza in con.cursor().execute(f"SELECT uid, name_{lang} FROM [menu_pizza]").fetchall():
            res.append({
                "uid" : pizza[0],
                "name" : pizza[1].replace('~', "'"),
            })
    return res
def get_pizza_size_type(pizza_uid : str, cost : int) -> str:
    """Получить тип пиццы"""
    with sqlite3.connect("db/menu.db") as con:
        res = con.cursor().execute(f"SELECT cost_small, cost_medium, cost_large FROM [menu_pizza] WHERE uid='{pizza_uid}'").fetchone()
        if res[0] == cost: return "small"
        if res[1] == cost: return "medium"
        else: return "large"
def get_pizza_info(uid : str) -> dict:
    """получить инфопмацию о пицце"""
    with sqlite3.connect("db/menu.db") as con:
        r = con.cursor().execute(f"SELECT * FROM [menu_pizza] WHERE uid='{uid}' ").fetchone()
        return {
            "img" : r[4],
            "uid" : r[0],
            "name" : {
                "ru" : r[1].replace('~', "'"),
                "uz" : r[2].replace('~', "'"),
                "en" : r[3].replace('~', "'"),
            },
            "description" : {
                "ru" : r[5].replace('~', "'"),
                "uz" : r[6].replace('~', "'"),
                "en" : r[7].replace('~', "'"),
            },
            "cost" : {
                "small" : r[8],
                "medium" : r[9],
                "large" : r[10],
            }
        }

def add_pizza(name : str) -> None:
    with sqlite3.connect("db/menu.db") as con:
        name = name.replace("'", '~')
        name = name.replace('"', '~')
        con.cursor().execute(f"INSERT INTO [menu_pizza] VALUES('{uuid.uuid4()}', '{name}', '{name}', '{name}', '', 'Нет описание', 'Tavsif yoq', 'No description', '0', '0', '0')")
