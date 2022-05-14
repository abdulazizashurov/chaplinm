from db_user import DBUser
from discount_pizza import DiscountPizza
from order import Order
from reserved import Reserved
from telebot import TeleBot
from telebot.types import LabeledPrice
from user import User
from configparser import ConfigParser
import config
import basket
import food
import DBPizza

langer = ConfigParser()
langer.read("data/langs.ini", encoding="utf8")

class Payment():
    @staticmethod
    def set_payment(bot : TeleBot, user : User, payment_method : str, order_uid : str) -> None:
        """Выводим чек для оплаты"""
        r = []
        for db in basket.get_foods_in_basket(user.id):
            price = db['count'] * db['price']
            if db['category_uid'] == "pizza":
                name = DBPizza.get_name(db['food_uid'])[user.lang]
                if Reserved.get_reserved(user.id, 5) == 'y' and DBUser.get_count_buy(user.id) == 0:
                    price -= DiscountPizza.get_discount_cost()
                    Reserved.set_reserved(user.id, 5, "n")
            else:
                name = food.get_name(db['food_uid'])[user.lang]            
            r.append(LabeledPrice(label=name, amount=int(f"{price}00")))
        road = int(Reserved.get_reserved(user.id, 4))
        if road > 0:
            r.append(LabeledPrice(label=langer[user.lang]['dilivery'], amount=int(f"{road}00")))

        r = bot.send_invoice(user.id, title=langer[user.lang]['invoiceForOrder'], description=langer[user.lang]['orderFromChaplinBot'],
            provider_token=config.PAYMENT[payment_method], currency="UZS",
            prices = r,
            start_parameter="request", invoice_payload=order_uid, is_flexible=False)
        Order.set_payment_message_id(user.id, r.message_id)
