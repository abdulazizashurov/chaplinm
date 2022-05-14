from discount_pizza import DiscountPizza
from locator import Locator
from order import Order
from price_manager import PriceManager
from payment import Payment
from reserved import Reserved
from db_user import DBUser
from telebot import TeleBot, util
from configparser import ConfigParser
from telebot import types
from telebot.types import Message
from garbage_collector import Garbage_Collector
from keyboard import Keyboard
from user import User
from utils import Utils
import time
import basket
import food
import config
import DBPizza


langer = ConfigParser()
langer.read("data/langs.ini", encoding="utf8")

def main_panel_user(bot : TeleBot, id : str, lang : str) -> None:
    """Вывести главную панель пользователя"""
    basket.clear_basket(id)
    
    Garbage_Collector.Clear(bot, id)
    kbrd = Keyboard.get_keyboard_user_menu(lang)
    text = f"{langer[lang]['hello']}\r\n"
    text += f"{langer[lang]['your_cashback_is']} {DBUser.get_cashback(id)} {langer[lang]['soum']}"
    Garbage_Collector.add_garbage(id, bot.send_message(id, text, reply_markup=kbrd).message_id)
def choise_dilivery(bot : TeleBot, user : User) -> None:
    """Выбор доставки"""
    Garbage_Collector.Clear(bot, user.id)
    if len(basket.get_foods_in_basket(user.id)) > 0:
        kbrd = Keyboard.get_keyboard_choise_dilivery(user)
        Garbage_Collector.add_garbage(user.id, bot.send_message(user.id, f"{langer[user.lang]['select_dilivery_method']}", reply_markup=kbrd).message_id)    
    else:
        Garbage_Collector.add_garbage(user.id, bot.send_message(user.id, f"{langer[user.lang]['no_selected_foods']}").message_id)    
        time.sleep(2)
        order_manager_user(bot, user)
def set_address_dilivery(msg : Message, bot : TeleBot, user : User) -> None:
    """Указания адреса доставки"""
    Garbage_Collector.Clear(bot, user.id)
    Reserved.set_reserved(user.id, 1, "Доставка")
    kbrd = types.ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
    kbrd.add(types.KeyboardButton(langer[user.lang]["send_location"], request_location=True))
    Garbage_Collector.add_garbage(user.id, bot.send_message(user.id, f"{langer[user.lang]['send_location']}", reply_markup=kbrd).message_id)    
    bot.register_next_step_handler(msg, lambda message : action_set_geolocation(user, bot, message) )    
def order_manager_user(bot : TeleBot, user : User) -> None:
    """Панель управления заказа"""
    Garbage_Collector.Clear(bot, user.id)
    kbrd = Keyboard.get_keyboard_order_manager(user)
    text = ""
    all_foods = basket.get_foods_in_basket(user.id)
    price = 0
    for af in all_foods:
        price += af["count"] * af["price"]
    text += f"{langer[user.lang]['amountFoods']} {len(all_foods)}\r\n"
    text += f"{langer[user.lang]['cost']} {Utils.to_razr(price)} {langer[user.lang]['soum']}"
    Garbage_Collector.add_garbage(user.id, bot.send_message(user.id, f"{text}", reply_markup=kbrd).message_id)
def show_about_us(bot : TeleBot, user : User) -> None:
    """Вывести информацию о нас"""
    Garbage_Collector.Clear(bot, user.id)
    kbrd = Keyboard.get_keyboard_user_panel(user)
    Garbage_Collector.add_garbage(user.id, bot.send_message(user.id, f"{langer[user.lang]['about_us']}", reply_markup=kbrd).message_id)    
def choise_category_user(bot : TeleBot, user : User) -> None:
    """выбор категории"""
    Garbage_Collector.Clear(bot, user.id)
    kbrd = Keyboard.get_keyboard_food_categories(user)
    Garbage_Collector.add_garbage(user.id, bot.send_message(user.id, f"{langer[user.lang]['selectCategory']}", reply_markup=kbrd).message_id)
def show_select_food(bot : TeleBot, user : User) -> None:
    """Вывести список блюд"""
    Garbage_Collector.Clear(bot, user.id)
    kbrd = Keyboard.get_keyboard_show_food_list(user)  
    Garbage_Collector.add_garbage(user.id, bot.send_message(user.id, f"{langer[user.lang]['selectFood']}", reply_markup=kbrd).message_id)      
def show_food_info(bot :TeleBot, user : User, afood : dict) -> None:
    """вывести информацию о блюде"""
    Garbage_Collector.Clear(bot, user.id)
    text = ""
    text += f"{langer[user.lang]['name']} {afood[f'name_{user.lang}']}\r\n"
    text += f"{langer[user.lang]['description']} {afood[f'description_{user.lang}']}\r\n"
    text += f"{langer[user.lang]['cost']}: {Utils.to_razr(afood['cost'])}\r\n"
    if afood['img'] == '' or afood['img'] == ' ':
        text += langer[user.lang]['no_preview']
    else:
        Garbage_Collector.add_garbage(user.id, bot.send_photo(user.id, afood['img']).message_id) 
    kbrd = Keyboard.get_keyboard_food_cart(user)  
    Garbage_Collector.add_garbage(user.id, bot.send_message(user.id, text, reply_markup=kbrd).message_id)      
def select_language_user(bot : TeleBot, id : str, lang : str) -> None:
    """Выбор языка для пользователя"""
    Garbage_Collector.Clear(bot, id)
    kbrd = Keyboard.get_keyboard_select_language()
    Garbage_Collector.add_garbage_commid(id, bot.send_message(id, langer[lang]["selectLanguage"], reply_markup=kbrd).message_id)        
def select_language_user_begin_register(bot : TeleBot, user : User) -> None:
    """Выбор языка для пользователя"""
    Garbage_Collector.Clear(bot, user.id)
    kbrd = Keyboard.get_keyboard_select_language_begin_register()
    Garbage_Collector.add_garbage_commid(user.id, bot.send_message(user.id, langer[user.lang]["selectLanguage"], reply_markup=kbrd).message_id)    
def set_name_user_begin_register(msg : Message, bot : TeleBot, user : User) -> None:
    """Предварительная регистрация. Указание имени пользователя"""
    Garbage_Collector.Clear(bot, user.id)
    Garbage_Collector.add_garbage_commid(user.id, bot.send_message(user.id, langer[user.lang]["inputYourName"]).message_id)        
    bot.register_next_step_handler(msg, lambda message : set_name_user_begin_register_sub(user, bot, message))
def setting_panel_user(bot : TeleBot, id : str, lang : str) -> None:
    """Вывести панель  настроек пользователя"""
    Garbage_Collector.Clear(bot, id)
    kbrd = Keyboard.get_keyboard_user_settings(lang)
    Garbage_Collector.add_garbage_commid(id, bot.send_message(id, langer[lang]["selectWhatNeedToChange"], reply_markup=kbrd).message_id)
def set_phone_number_user(bot : TeleBot, user : User, message : Message, id : str, lang : str) -> None:
    """Указать номер телефона"""
    Garbage_Collector.Clear(bot, id)
    kbrd = types.ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
    kbrd.add(types.KeyboardButton(langer[lang]["send_phone_number"], request_contact=True))
    Garbage_Collector.add_garbage_commid(id, bot.send_message(id, langer[lang]["actionSetPhoneNumber"], reply_markup=kbrd).message_id)
    bot.register_next_step_handler(message, lambda msg : user_set_phone_number(user, bot, msg, False))
def get_food_count(msg : Message, bot : TeleBot, user : User) -> None:
    """Узнать, сколько порций нужно"""
    Garbage_Collector.Clear(bot, user.id)
    start_count = "1"
    locator = Locator.get_locator(user.id)
    f = food.get_food(locator["category_uid"], locator["food_uid"])
    basket.add_food(user.id, locator["category_uid"], locator["food_uid"], start_count, f["cost"])
    kbrd = Keyboard.get_keyboard_count(user, f["uid"], start_count)
    Garbage_Collector.add_garbage_commid(user.id, bot.send_message(user.id, langer[user.lang]["inputCountFood"], reply_markup=kbrd).message_id)
def set_comment(bot : TeleBot, user : User, msg : Message) -> None:
    """Установить комментарий"""
    Garbage_Collector.Clear(bot, user.id)
    kbrd = Keyboard.get_keyboard_cancel(user, "[no_comment]")
    Garbage_Collector.add_garbage(user.id, bot.send_message(user.id, f"{langer[user.lang]['input_comment']}", reply_markup=kbrd).message_id)
    bot.register_next_step_handler(msg, lambda message : action_set_comment(bot, user, message))   

def action_set_comment(bot : TeleBot, user : User, msg : Message) -> None:
    """Сохранить комментарий"""
    if isinstance(msg, Message):
        Garbage_Collector.add_garbage(user.id, msg.message_id)
        text = msg.text
    else: text = msg
    Order.set_order_comment(user.id, text)
    choise_category_user(bot, user)
    

def show_basket_user(bot : TeleBot, user : User) -> None:
    """Отобразить корзину покупки"""
    Garbage_Collector.Clear(bot, user.id)
    kbrd = Keyboard.get_keyboard_show_user_basket(user)
    text = langer[user.lang]["selected"] + "\r\n"
    for article in basket.get_foods_in_basket(user.id):
        if article['category_uid'] == "pizza":
            name = DBPizza.get_name(article['food_uid'])[user.lang]
        else:
            name = food.get_name(article['food_uid'])[user.lang]
        text += f"{name}: {article['count']}x{Utils.to_razr(article['price'])}: {Utils.to_razr(int(article['count'])*int(article['price']))}\r\n"
    Garbage_Collector.add_garbage_commid(user.id, bot.send_message(user.id, text, reply_markup=kbrd).message_id)    
def change_count_food(msg : Message, bot : TeleBot, user : User) -> None:
    """Изменение кол-во выбранного"""
    Garbage_Collector.Clear(bot, user.id)
    kbrd = Keyboard.get_keyboard_cancel(user, "[basket_view]")
    Garbage_Collector.add_garbage(user.id, bot.send_message(user.id, f"{langer[user.lang]['changeCount']}", reply_markup=kbrd).message_id)
    bot.register_next_step_handler(msg, lambda message : set_new_count(user, bot, message))   
def set_name_user( msg : Message, bot : TeleBot, user : User) ->None:
    """Указать имя пользователя"""
    Garbage_Collector.Clear(bot, user.id)
    kbrd = Keyboard.get_keyboard_cancel(user, "[settings]")
    Garbage_Collector.add_garbage_commid(user.id, bot.send_message(user.id, langer[user.lang]["inputYourName"], reply_markup=kbrd).message_id)        
    bot.register_next_step_handler(msg, lambda message : user_set_name(user, bot, message))
def set_payment(bot : TeleBot, user : User) -> None:
    """Указать способ оплаты"""
    Garbage_Collector.Clear(bot, user.id)
    kbrd = Keyboard.get_keyboard_choise_payment(user)
    Garbage_Collector.add_garbage_commid(user.id, bot.send_message(user.id, langer[user.lang]["set_method_payment"], reply_markup=kbrd).message_id)    

def calc_final_cost(user : User) -> dict:
    """Функция расчета стоимости"""
    min_cost_per_two_km = 0

    db = basket.get_foods_in_basket(user.id)
    num = Order.get_active_number()
    total_price = 0
    total_price_without_diliviery = 0
    cost_for_dilivery = 0
    total_cost_for_food = 0
    data = ""
    real_discount = DiscountPizza.get_discount_cost()
    minus_cost = real_discount
    used_discount = False
    for b in db:
        price = b['count'] * b['price']
        total_price += price
        if b['category_uid'] == "pizza":
            if DiscountPizza.is_done_user(user.id) == False and minus_cost > 0 and DBUser.get_count_buy(user.id) == 0:
                total_price -= minus_cost
                price -= minus_cost
                minus_cost = 0
                used_discount = True
                Reserved.set_reserved(user.id, 5, "y")
            name = DBPizza.get_name(b['food_uid'])[user.lang] + f" ({DBPizza.get_pizza_size_type(b['food_uid'], b['price'])})"
        else:
            name = food.get_name(b['food_uid'])[user.lang]
        data += f"{langer[user.lang]['food']} {name}\r\n{langer[user.lang]['pieces']} {b['count']}\r\n{langer[user.lang]['total_cost']} {Utils.to_razr(price)} {langer[user.lang]['soum']}\r\n"
        if b['category_uid'] == "pizza" and used_discount == True:
            used_discount = False
            data += f"({langer[user.lang]['discount']} -{real_discount})\r\n"
    data += f"{langer[user.lang]['total_cost_for_food']} {Utils.to_razr(total_price)}\r\n"
    total_cost_for_food = total_price
    location = Reserved.get_reserved(user.id, 2)
    total_price_without_diliviery = total_price
    cost_for_road = 0
    cost_for_dilivery = 0
    if location == "no":
        data += f"{langer[user.lang]['total_cost']} {Utils.to_razr(total_price)}"
    else:
        location = location.split(':')
        if len(config.LOCATION_NAME) > 1:
            one_location = round(Utils.calc_killometers(config.MY_LOCATION_1, (location[0], location[1])))
            two_location = round(Utils.calc_killometers(config.MY_LOCATION_2, (location[0], location[1])))
            if one_location > two_location:
                killometers = round(Utils.calc_killometers(config.MY_LOCATION_2, (location[0], location[1])))
            else:
                killometers = round(Utils.calc_killometers(config.MY_LOCATION_1, (location[0], location[1])))
        else:
            killometers = round(Utils.calc_killometers(config.MY_LOCATION_1, (location[0], location[1])))
        cost_per_killometer = PriceManager.get_road()
        if killometers > 5:
            price = killometers * cost_per_killometer
        else:
            price = min_cost_per_two_km
        cost_for_road = price
        cost_for_dilivery = price
        total_price += price
        data += f"{langer[user.lang]['cost_for_dilivery']} {Utils.to_razr(price)}\r\n"
        data += f"{langer[user.lang]['total_cost_with_dilivery']} {Utils.to_razr(total_price)}"
    location = "no" if location == "no" else f"{location[0]}:{location[1]}"
    return {
        "order_number" : num,
        "data" : data,
        "total_cost" : total_price,
        "cost_for_dilivery" : cost_for_dilivery,
        "cost_for_road" : cost_for_road,
        "total_price_without_diliviery" : total_price_without_diliviery,
        "total_cost_for_food" : total_cost_for_food,
        "location" : location
    }

def final_order_check(bot : TeleBot, user : User, paymen_method : str) -> None:
    """Чек подтверждения заказа"""
    Garbage_Collector.Clear(bot, user.id)
    dilivery_method = Reserved.get_reserved(user.id, 1)
    filial = Reserved.get_reserved(user.id, 4)
    Reserved.set_reserved(user.id, 3, paymen_method)    
    prices = calc_final_cost(user)
    comment = Order.get_order_comment(user.id)
    Order.delete_comment(user.id)
    #TODO пересмотреть, два аргумента указывается один и тот же значение prices["total_price_without_diliviery"]
    Order.add_order(prices["data"], user.id, user.name, prices["total_price_without_diliviery"], prices["data"],
            paymen_method, dilivery_method, filial, prices["total_price_without_diliviery"], prices["location"], comment)
    Order.inc_active_number()
    Reserved.set_reserved(user.id, 4, prices["cost_for_road"])
    kbrd = Keyboard.get_keyboard_final_order_check(user)
    bot.send_message(user.id, prices["data"])
    Garbage_Collector.add_garbage_commid(user.id, bot.send_message(user.id, langer[user.lang]["continue"], reply_markup=kbrd).message_id)

def final_order(bot : TeleBot, user : User) -> None:
    """Финал заказа"""
    payment_method = Reserved.get_reserved(user.id, 3)
    Garbage_Collector.Clear(bot, user.id)
    uid = Order.get_order_uid(user.id)
    if payment_method == "click" or payment_method == "payme":        
        Payment.set_payment(bot, user, payment_method, uid)
    elif payment_method == "cashback":
        prices = calc_final_cost(user)
        if user.cashback > prices["total_cost"]:
            buy(bot, user, False, False, False, uid)
        else:
            bot.send_message(user.id, langer[user.lang]["not_enough_cashback"])
            time.sleep(2)
            order_manager_user(bot, user)
    else: 
        uid = Order.get_order_uid(user.id)
        buy(bot, user, True, True, True, uid)
def select_filial(bot : TeleBot, user : User) -> None:
    """Выбрать филиал"""
    Garbage_Collector.Clear(bot, user.id)
    kbrd = Keyboard.get_keyboard_fillial_location(user)
    Garbage_Collector.add_garbage_commid(user.id, bot.send_message(user.id, langer[user.lang]["select_fillial"], reply_markup=kbrd).message_id)
def self_dilivery(bot : TeleBot, user : User) -> None:
    """Пользователь сам заберет заказ"""
    Reserved.set_reserved(user.id, 1, "Самовывоз")
    Reserved.set_reserved(user.id, 2, "no")
    select_filial(bot, user)
#actions
def buy(bot : TeleBot, user : User, up_buy_all : bool, up_buy_month : bool, up_cashback : bool, order_uid : str) -> None:
    """Финал заказа"""
    if DiscountPizza.is_done_user(user.id) == False:
        DiscountPizza.done_user_id(user.id)
    order = Order.get_order(order_uid)
    text = ""
    text += f"Пользователь: {user.name}\r\n"
    text += f"Номер телефона: +{user.phone}\r\n"
    text += f"Юзернейм: @{user.username}\r\n"
    text += f"Язык: {user.lang}\r\n"
    text += f"Тип оплаты: {order[2]}\r\n"
    text += f"Тип доставки: {order[3]}\r\n"
    text += f"филиал: {order[5]}\r\n"
    text += f"Заказ: {order[1]}\r\n"
    text += f"Коментарий: {order[7]}\r\n"
    kbrd = Keyboard.get_keyboard_chanel(order_uid)
    location = order[6]
    if location != "no":
        location = location.split(':')
        bot.send_location(config.CHANEL, location[0], location[1])
    r = bot.send_message(config.CHANEL, text, reply_markup=kbrd)
    Order.add_message(order_uid, r.message_id, text)
    basket.clear_basket(user.id)
    cost = order[4]
    user.buy_all += cost
    user.buy_month += cost    
    if up_buy_all: DBUser.set_buy_all(user.id, user.buy_all)
    if up_buy_month: DBUser.set_buy_month(user.id, user.buy_month)
    DBUser.up_count_buy(user.id)
    main_panel_user(bot, user.id, user.lang)
def action_set_geolocation(user : User, bot : TeleBot, msg : Message) -> None:
    Garbage_Collector.add_garbage_commid(user.id, msg.message_id)
    if msg.content_type == "location":
        Reserved.set_reserved(user.id, 2, f"{msg.location.latitude}:{msg.location.longitude}")
        if len(config.LOCATION_NAME) > 1:
            loc_one = Utils.calc_killometers(config.MY_LOCATION_1, (msg.location.latitude, msg.location.longitude))
            loc_two = Utils.calc_killometers(config.MY_LOCATION_2, (msg.location.latitude, msg.location.longitude))
            if loc_one < loc_two:
                Reserved.set_reserved(user.id, 4, config.LOCATION_NAME["1"])
            else:
                Reserved.set_reserved(user.id, 4, config.LOCATION_NAME["2"])
        else: 
            Reserved.set_reserved(user.id, 4, config.LOCATION_NAME["1"])
        set_payment(bot, user)
    else: order_manager_user(bot, user)
def set_new_count(user : User, bot : TeleBot, msg : Message) -> None:
    """Изменение кол-во выбранного"""
    Garbage_Collector.add_garbage_commid(user.id, msg.message_id)
    if msg.text.isdigit() and int(msg.text) > 0: 
        basket.set_new_count(user.id, Locator.get_food(user.id), msg.text)
    show_basket_user(bot, user)
def action_clear_basket(bot : TeleBot, user : User) -> None:
    """Очищаем корзину"""
    basket.clear_basket(user.id)
    order_manager_user(bot, user)
def set_count_food(user : User, bot : TeleBot, msg : Message) -> None:
    """Записать кол-во порций"""
    Garbage_Collector.add_garbage_commid(user.id, msg.message_id)
    locator = Locator.get_locator(user.id)
    category_uid = locator["category_uid"]
    food_uid = locator["food_uid"]
    if msg.text.isdigit() and int(msg.text) > 0:
        basket.add_food(user.id, category_uid, food_uid, msg.text, food.get_price(category_uid, food_uid))
        choise_category_user(bot, user)
    else: 
        get_food_count(msg, bot, user)
def action_change_count_food(user : User, bot : TeleBot, msg : Message) -> None:
    """Записать кол-во порций"""
    Garbage_Collector.add_garbage_commid(user.id, msg.message_id)
    locator = Locator.get_locator(user.id)
    food_uid = locator["food_uid"]
    if msg.text.isdigit() and int(msg.text) > 0:
        basket.set_new_count(user.id, food_uid, msg.text)
        choise_category_user(bot, user)
    else: 
        get_food_count(msg, bot, user)
def user_set_phone_number(user : User, bot : TeleBot, msg : Message, first : bool) -> None:
    """Пользователь указал номер телефона"""
    Garbage_Collector.add_garbage_commid(user.id, msg.message_id)
    number = ""
    change = True
    if msg.content_type == "contact":
        number = Utils.get_number(msg.contact.phone_number)
    else:
        numbera = Utils.get_number(msg.text)
        if Utils.is_valid_number(numbera):
            number = numbera
        else: change = False
    if change: DBUser.change_user_phone_number(user.id, number)
    else:
        Garbage_Collector.add_garbage_commid(user.id, bot.send_message(user.id, langer[user.lang]["actionSetPhoneNumber"]).message_id)        
        bot.register_next_step_handler(msg, lambda message : user_set_phone_number(user, bot, message, first))
    if change:
        if first:
            main_panel_user(bot, user.id, user.lang)
        else:
            setting_panel_user(bot, user.id, user.lang)    
def set_name_user_begin_register_sub(user : User, bot : TeleBot, msg : Message) -> None:
    """Записать имя пользователя в базу"""
    Garbage_Collector.add_garbage_commid(user.id, msg.message_id)
    DBUser.change_user_name(user.id, msg.text)
    Garbage_Collector.Clear(bot, user.id)
    kbrd = types.ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
    kbrd.add(types.KeyboardButton(langer[user.lang]["send_phone_number"], request_contact=True))
    Garbage_Collector.add_garbage_commid(user.id, bot.send_message(user.id, langer[user.lang]["actionSetPhoneNumber"], reply_markup=kbrd).message_id)        
    bot.register_next_step_handler(msg, lambda message : user_set_phone_number(user, bot, message, True))
def user_set_name(user : User, bot : TeleBot, message : Message) -> None:
    """Записать новое имя пользователя"""
    Garbage_Collector.add_garbage_commid(user.id, message.message_id)
    DBUser.change_user_name(user.id, message.text)
    setting_panel_user(bot, user.id, user.lang)