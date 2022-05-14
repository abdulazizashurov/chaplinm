from db_user import DBUser
from utils import Utils

class User:
    id = None
    name = None
    username = None
    phone = None
    lang = None
    date_register = None
    date_last_action = None
    cashback = None
    buy_all = None
    buy_month = None
    count_buy = None
    def __init__(self, id : str, name : str, username : str, phone : str, 
                lang : str, date_register : str, date_last_action : str, cashback : float,
                buy_all : int, buy_month : int, count_buy : int) -> None:
        self.id = id
        self.name = name
        self.username = username
        self.phone = phone
        self.lang = lang
        self.date_register = date_register
        self.date_last_action = date_last_action
        self.cashback = cashback
        self.buy_all = buy_all
        self.buy_month = buy_month
        self.count_buy = count_buy
    @staticmethod
    def load_all_users() -> list:
        """загрузить всех пользователей"""
        res = []
        for row in DBUser.load_all_users():
            res.append({
                "id" : row[0],
                "lang" : row[4]
            })
        return res
    @staticmethod
    def load_user_from_id(id : int) -> object:
        """Загрузить пользователя через его id"""
        db_load = DBUser.load_full_data(id)
        name = db_load[1]
        username = db_load[2]
        phone = db_load[3]
        lang = db_load[4]
        date_registed = db_load[5]
        date_last_action = db_load[6]
        cashback = db_load[7]
        buy_all = db_load[8]
        buy_month = db_load[9]
        count_buy = db_load[10]
        return User(id, name, username, phone, lang, date_registed, date_last_action, cashback, buy_all, buy_month, count_buy)
    @staticmethod
    def load_user(user) -> object:
        """Загрузить пользователя из message"""
        lang = "ru"
        now = Utils.get_date()
        date_registed = now
        date_last_action = now
        phone = ""
        cashback = 0.0
        buy_all = 0
        buy_month = 0
        count_buy = 0
        if DBUser.existing_user(user.id):
            db_load = DBUser.load_data(user.id)
            if db_load != None:
                phone = db_load[0]
                lang = db_load[1]
                date_registed = db_load[2]
                date_last_action = Utils.get_date()
                cashback = db_load[4]
                buy_all = db_load[5]
                buy_month = db_load[6]
                count_buy = db_load[7]
        return User(user.id, user.first_name, user.username, phone, lang, date_registed, date_last_action, cashback, buy_all, buy_month, count_buy)
    def __str__(self) -> str:
        return f"User: {self.id}, {self.name}"