import sqlite3
import uuid

def food_get_categories() -> list:
    """Получить список категорий"""
    res = []
    with sqlite3.connect("db/menu.db", check_same_thread=False) as con:
        r = con.cursor().execute(f"SELECT * FROM [category]").fetchall()
        for row in r:
            res.append({
                "uid" : row[0],
                "ru" : row[1].replace('~', "'"),
                "uz" : row[2].replace('~', "'"),
                "en" : row[3].replace('~', "'"),
            })
    return res

def set_new_name(lang : str, new_name : str, category_uid : str, food_uid) -> None:
    """Изменить имя"""
    with sqlite3.connect("db/menu.db", check_same_thread=False) as con:
        new_name = new_name.replace("'", '~')
        con.cursor().execute(f"UPDATE [menu] SET name_{lang}='{new_name}' WHERE category_uid='{category_uid}' AND uid='{food_uid}'")

def set_new_description(lang : str, new_name : str, category_uid : str, food_uid) -> None:
    """Изменить имя"""
    with sqlite3.connect("db/menu.db", check_same_thread=False) as con:
        new_name = new_name.replace("'", '~')
        con.cursor().execute(f"UPDATE [menu] SET description_{lang}='{new_name}' WHERE category_uid='{category_uid}' AND uid='{food_uid}'")

def set_cost(category_uid : str, food_uid : str, cost : str) -> None:
    with sqlite3.connect("db/menu.db", check_same_thread=False) as con:
        con.cursor().execute(f"UPDATE [menu] SET cost='{cost}' WHERE category_uid='{category_uid}' AND uid='{food_uid}'")        
def set_preview(category_uid : str, food_uid : str, img : str) -> None:
    """Установить превью"""
    with sqlite3.connect("db/menu.db", check_same_thread=False) as con:
        con.cursor().execute(f"UPDATE [menu] SET img='{img}' WHERE category_uid='{category_uid}' AND uid='{food_uid}'")    

def add_food(category_uid : str, subcategory_uid : str, food_name) -> None:
    """Добавить новое блюдо"""
    with sqlite3.connect("db/menu.db", check_same_thread=False) as con:
        food_name = food_name.replace("'", '~')
        food_name = food_name.replace('"', '~')
        con.cursor().execute(f"INSERT INTO [menu] VALUES('{category_uid}', '{subcategory_uid}', '{uuid.uuid4()}', '', '{food_name}', '{food_name}', '{food_name}', '', '', '', '0')")

def get_price(category_uid : str, food_uid : str) -> int:
    """Получить стоимость продукта"""
    with sqlite3.connect("db/menu.db", check_same_thread=False) as con:
        return con.cursor().execute(f"SELECT cost FROM [menu] WHERE category_uid='{category_uid}' AND uid='{food_uid}'").fetchone()[0]
def food_get_subcategory(category_uid : str) -> list:
    """Получить под категории"""
    res = []
    with sqlite3.connect("db/menu.db", check_same_thread=False) as con:
        for row in con.cursor().execute(f"SELECT uid, name_ru, name_uz, name_en FROM [subcategory] WHERE category_parent_uid='{category_uid}'").fetchall():
            res.append({
                "uid": row[0],
                "ru" : row[1].replace('~', "'"),
                "uz" : row[2].replace('~', "'"),
                "en" : row[3].replace('~', "'"),
            })
    return res    
def food_get_foods(category_uid : str, subcategory_uid : str) -> list:
    """Получить все категории"""
    res = []
    with sqlite3.connect("db/menu.db", check_same_thread=False) as con:
        for row in con.cursor().execute(f"SELECT uid, name_ru, name_uz, name_en FROM [menu] WHERE category_uid='{category_uid}' AND subcategory_uid='{subcategory_uid}'").fetchall():
            res.append({
                "uid": row[0],
                "ru" : row[1].replace('~', "'"),
                "uz" : row[2].replace('~', "'"),
                "en" : row[3].replace('~', "'"),
            })
    return res

def delete_food(category_uid : str, food_uid : str) -> None:
    """Удаления блюда"""
    with sqlite3.connect("db/menu.db", check_same_thread=False) as con:
        con.cursor().execute(f"DELETE FROM [menu] WHERE category_uid='{category_uid}' AND uid='{food_uid}'")    

def delete_category(category_uid : str, subcategory_uid : str) -> None:
    """Удаления блюда"""
    with sqlite3.connect("db/menu.db", check_same_thread=False) as con:
        cur = con.cursor()
        table = "category" if subcategory_uid == '' else "subcategory"
        uid = category_uid if subcategory_uid == '' else subcategory_uid
        cur.execute(f"DELETE FROM [{table}] WHERE uid='{uid}'")
        cur.execute(f"DELETE FROM [menu] WHERE {table}_uid='{uid}'")

def get_food(category_uid : str, food_uid : str) -> dict:
    """Получаем информацию о продукте"""
    with sqlite3.connect("db/menu.db", check_same_thread=False) as con:
        f = con.cursor().execute(f"SELECT * FROM [menu] WHERE category_uid='{category_uid}' AND uid='{food_uid}'").fetchone()
        return {
            "category_uid" : f[0],
            "subcategory_uid" : f[1],
            "uid" : f[2],
            "img" : f[3],
            "name_ru" : f[4].replace('~', "'"),
            "name_uz" : f[5].replace('~', "'"),
            "name_en" : f[6].replace('~', "'"),
            "description_ru" : f[7].replace('~', "'"),
            "description_uz" : f[8].replace('~', "'"),
            "description_en" : f[9].replace('~', "'"),
            "cost" : f[10],
        }
def get_name(food_uid : str) -> str:
    """Получить имя блюда через uid"""
    with sqlite3.connect("db/menu.db", check_same_thread=False) as con:
        r = con.cursor().execute(f"SELECT name_ru, name_uz, name_en FROM [menu] WHERE uid='{food_uid}'").fetchone()
        if r != None:
            return {
                "ru" : r[0].replace('~', "'"),
                "uz" : r[1].replace('~', "'"),
                "en" : r[2].replace('~', "'"),
            }
        return None

def existing_category(category_name : str) -> bool:
    """Есть ли такая категория"""
    with sqlite3.connect("db/menu.db", check_same_thread=False) as con:
        cur = con.cursor()
        category_name = category_name.replace("'", '~')
        r1 = cur.execute(f"SELECT name_ru FROM [category] WHERE name_ru='{category_name}'").fetchone()
        r2 = cur.execute(f"SELECT name_uz FROM [category] WHERE name_uz='{category_name}'").fetchone()
        r3 = cur.execute(f"SELECT name_en FROM [category] WHERE name_en='{category_name}'").fetchone()
        return True if (r1 != None or r2 != None or r3 != None) else False

def add_category(category_name : str) -> None:
    """Создание категории"""
    with sqlite3.connect("db/menu.db", check_same_thread=False) as con:
        category_name = category_name.replace("'", '~')
        category_name = category_name.replace('"', '~')
        con.cursor().execute(f"INSERT INTO [category] VALUES('{uuid.uuid4()}', '{category_name}', '{category_name}', '{category_name}')")
def add_subcategory(category_uid : str, subcategory_name : str) -> None:
    """Создание категории"""
    with sqlite3.connect("db/menu.db", check_same_thread=False) as con:
        subcategory_name = subcategory_name.replace("'", '~')
        subcategory_name = subcategory_name.replace('"', '~')
        con.cursor().execute(f"INSERT INTO [subcategory] VALUES('{uuid.uuid4()}', '{category_uid}', '{subcategory_name}', '{subcategory_name}', '{subcategory_name}')")       

def rename_category(category_uid : str, subcategory_uid : str, category_name : str, lang : str) -> None:
    """Переименновать имя категории"""
    with sqlite3.connect("db/menu.db", check_same_thread=False) as con:
        category_name = category_name.replace("'", '~')
        table = "category" if subcategory_uid == '' else "subcategory"
        uid = category_uid if subcategory_uid == '' else subcategory_uid
        con.cursor().execute(f"UPDATE [{table}] SET name_{lang}='{category_name}' WHERE uid='{uid}'")