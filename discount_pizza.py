import sqlite3

class DiscountPizza():
    """Класс по управлении скидки на пиццу"""
    @staticmethod 
    def set_discount_cost(cost : int) -> None:
        """Установить стоимость скидки"""
        with sqlite3.connect(f"db/discounts.db", check_same_thread=False) as con:
            con.cursor().execute(f"UPDATE discount_pizza_cost SET cost='{cost}'")   
    @staticmethod
    def get_discount_cost() -> int:
        """Получить текущую стоимость"""
        with sqlite3.connect(f"db/discounts.db", check_same_thread=False) as con:
            return con.cursor().execute(f"SELECT cost FROM discount_pizza_cost").fetchone()[0]
    @staticmethod
    def done_user_id(user_id : int) -> None:
        """Отмечаем, что пользователь уже приобрел скидку"""
        with sqlite3.connect(f"db/discounts.db", check_same_thread=False) as con:
            con.cursor().execute(f"INSERT INTO discount_pizza VALUES('{user_id}')")
    @staticmethod
    def is_done_user(user_id : int) -> bool:
        """Проверка, пользователь пользовался ли скидкой"""
        with sqlite3.connect(f"db/discounts.db", check_same_thread=False) as con:
            return True if con.cursor().execute(f"SELECT user_id FROM discount_pizza WHERE user_id='{user_id}'").fetchone() != None else False