from utils import Utils
from reserved import Reserved
from keyboard import Keyboard
from garbage_collector import Garbage_Collector
from user import User
from telebot import types
from telebot import TeleBot
from telebot.types import Message
from configparser import ConfigParser
from locator import Locator
import basket
import DBPizza


langer = ConfigParser()
langer.read("data/langs.ini", encoding="utf8")


def show_pizza_list(bot : TeleBot, user : User) -> None:
    """Вывести список пиццы"""
    Garbage_Collector.Clear(bot, user.id)
    kbrd = types.InlineKeyboardMarkup()
    for pizza in DBPizza.get_pizza_list(user.lang):
        kbrd.add(types.InlineKeyboardButton(pizza['name'], callback_data=f"@#{pizza['uid']}"))
    kbrd.add(types.InlineKeyboardButton(langer[user.lang]['add_pizza'], callback_data=f"[add_pizza]"))
    kbrd.add(types.InlineKeyboardButton(langer[user.lang]['back'], callback_data=f"[foodManagment]"))
    Garbage_Collector.add_garbage_commid(user.id, bot.send_message(user.id, langer[user.lang]['pizza_managment'], reply_markup=kbrd).message_id)

def show_pizza_list_user(bot : TeleBot, user : User) -> None:
    """Вывести список пиццы"""
    Garbage_Collector.Clear(bot, user.id)
    kbrd = types.InlineKeyboardMarkup()
    existing = basket.get_foods_uid(user.id)
    btn = []
    z = 0
    for pizza in DBPizza.get_pizza_list(user.lang):
        if pizza['uid'] not in existing:
            if z == 1:
                btn.append(types.InlineKeyboardButton(pizza['name'], callback_data=f"@${pizza['uid']}"))
                kbrd.add(btn[0], btn[1])
                btn = []
                z = 0
            else:
                btn.append(types.InlineKeyboardButton(pizza['name'], callback_data=f"@${pizza['uid']}"))
                z +=1 
        else: existing[Utils.get_index(existing, pizza['uid'])]
    if z == 1 and len(btn) > 0:
        kbrd.add(btn[0])
    kbrd.add(types.InlineKeyboardButton(langer[user.lang]["pay"], callback_data="[pay]"))
    kbrd.add(types.InlineKeyboardButton(langer[user.lang]["basket_view"], callback_data="[basket_view]"))
    kbrd.add(types.InlineKeyboardButton(langer[user.lang]['back'], callback_data=f"[choiseCategory]"))
    Garbage_Collector.add_garbage_commid(user.id, bot.send_message(user.id, langer[user.lang]['pizza_managment'], reply_markup=kbrd).message_id)

def get_keyboard_count(user : User, food_uid : str, food_count : str) -> types.InlineKeyboardMarkup:
    """Получение количества блюда"""
    kbrd = types.InlineKeyboardMarkup(row_width=3)
    kbrd.add(types.InlineKeyboardButton("➖", callback_data=f"##{food_uid}"),
        types.InlineKeyboardButton(f"{food_count}", callback_data=f"#${food_uid}"),
        types.InlineKeyboardButton("➕", callback_data=f"#%{food_uid}"))
    kbrd.add(types.InlineKeyboardButton(langer[user.lang]["cancel"], callback_data=f"#^{food_uid}"),
        types.InlineKeyboardButton(langer[user.lang]["agree"], callback_data=f"[choiseCategory]"))
    return kbrd

def show_pizza_information_user(bot : TeleBot, user : User, pizza_uid : str) -> None:
    """Вывести информацию о пицце"""
    Garbage_Collector.Clear(bot, user.id)
    pizza = DBPizza.get_pizza_info(pizza_uid)
    if pizza["img"] != "":
        Garbage_Collector.add_garbage_commid(user.id, bot.send_photo(user.id, pizza["img"]).message_id)
    text = f"{langer[user.lang]['name']} {pizza['name'][user.lang]}\r\n"
    text += f"{langer[user.lang]['description']} {pizza['description'][user.lang]}\r\n"
    text += f"{langer[user.lang]['cost']} (25см): {pizza['cost']['small']}\r\n"
    text += f"{langer[user.lang]['cost']} (30см): {pizza['cost']['medium']}\r\n"
    text += f"{langer[user.lang]['cost']} (35см): {pizza['cost']['large']}\r\n"
    kbrd = types.InlineKeyboardMarkup(row_width=3)
    kbrd.add(types.InlineKeyboardButton("✅ 25", callback_data=f"[small]"),
            types.InlineKeyboardButton("✅ 30", callback_data=f"[medium]"),
            types.InlineKeyboardButton("✅ 35", callback_data=f"[large]")
        )
    kbrd.add(types.InlineKeyboardButton(langer[user.lang]['back'], callback_data=f"[select_pizza_user]"))
    Garbage_Collector.add_garbage_commid(user.id, bot.send_message(user.id, text, reply_markup=kbrd).message_id)

def show_get(bot : TeleBot, user : User, cost_type : str, msg : Message) -> None:
    """Вывести кнопку "купить"""""
    Garbage_Collector.Clear(bot, user.id)
    Reserved.set_reserved(user.id, 0, cost_type)
    start_cout = 1
    locator = Locator.get_locator(user.id)
    food_uid = locator["food_uid"]
    f = DBPizza.get_pizza_price(food_uid, cost_type)
    basket.add_food(user.id, "pizza", food_uid, start_cout, f)
    kbrd = get_keyboard_count(user, food_uid, start_cout)
    Garbage_Collector.add_garbage_commid(user.id, bot.send_message(user.id, langer[user.lang]['inputCountFood'], reply_markup=kbrd).message_id)
    

def set_pizza_count(bot : TeleBot, user : User) -> None:
    """Указать кол-во пиццы"""
    kbrd = get_keyboard_count(user, )

def action_set_pizza_count(bot : TeleBot, user : User, msg : Message) -> None:
    """Указать кол-во порций"""
    Garbage_Collector.add_garbage_commid(user.id, msg.message_id)
    if msg.text.isdigit() and int(msg.text) > 0:
        pizza_uid = Locator.get_food(user.id)
        basket.add_food(user.id, "pizza", pizza_uid, msg.text, DBPizza.get_pizza_price(pizza_uid, Reserved.get_reserved(user.id, 0)))
        show_pizza_list_user(bot, user)
    else:
        kbrd = Keyboard.get_keyboard_cancel("[show_pizza_information_user]")
        Garbage_Collector.add_garbage_commid(user.id, bot.send_message(user.id, langer[user.lang]['inputCountFood']).message_id)
        bot.register_next_step_handler(msg, lambda message : action_set_pizza_count(bot, user, message))

def show_pizza_information(bot : TeleBot, user : User, pizza_uid : str) -> None:
    """Вывести информацию о пицце"""
    Garbage_Collector.Clear(bot, user.id)
    pizza = DBPizza.get_pizza_info(pizza_uid)
    if pizza["img"] != "":
        Garbage_Collector.add_garbage_commid(user.id, bot.send_photo(user.id, pizza["img"]).message_id)
    text = f"Имя (ру): {pizza['name']['ru']}\r\n"
    text += f"Имя (уз): {pizza['name']['uz']}\r\n"
    text += f"Имя (ен): {pizza['name']['en']}\r\n"
    text += f"Описание (ру): {pizza['description']['ru']}\r\n"
    text += f"Описание (уз): {pizza['description']['uz']}\r\n"
    text += f"Описание (ен): {pizza['description']['en']}\r\n"
    text += f"Стоимость (мал): {pizza['cost']['small']}\r\n"
    text += f"Стоимость (сред): {pizza['cost']['medium']}\r\n"
    text += f"Стоимость (бол): {pizza['cost']['large']}\r\n"
    kbrd = types.InlineKeyboardMarkup()
    kbrd.add(types.InlineKeyboardButton(langer[user.lang]['setPreview'], callback_data=f"[pizza_set_preview]"))
    kbrd.add(types.InlineKeyboardButton(langer[user.lang]['renameFoodRu'], callback_data=f"[pizza_set_ru_name]"))
    kbrd.add(types.InlineKeyboardButton(langer[user.lang]['renameFoodUz'], callback_data=f"[pizza_set_uz_name]"))
    kbrd.add(types.InlineKeyboardButton(langer[user.lang]['renameFoodEn'], callback_data=f"[pizza_set_en_name]"))
    kbrd.add(types.InlineKeyboardButton(langer[user.lang]['changeDescriptionRu'], callback_data=f"[pizza_set_ru_description]"))
    kbrd.add(types.InlineKeyboardButton(langer[user.lang]['changeDescriptionUz'], callback_data=f"[pizza_set_uz_description]"))
    kbrd.add(types.InlineKeyboardButton(langer[user.lang]['changeDescriptionEn'], callback_data=f"[pizza_set_en_description]"))
    kbrd.add(types.InlineKeyboardButton(langer[user.lang]['pizza_set_small_size'], callback_data=f"[pizza_set_small_cost]"))
    kbrd.add(types.InlineKeyboardButton(langer[user.lang]['pizza_set_medium_size'], callback_data=f"[pizza_set_medium_cost]"))
    kbrd.add(types.InlineKeyboardButton(langer[user.lang]['pizza_set_large_size'], callback_data=f"[pizza_set_large_cost]"))
    kbrd.add(types.InlineKeyboardButton(langer[user.lang]['deleteFood'], callback_data=f"[pizza_delete]"))
    kbrd.add(types.InlineKeyboardButton(langer[user.lang]['back'], callback_data=f"[select_pizza]"))
    Garbage_Collector.add_garbage_commid(user.id, bot.send_message(user.id, text, reply_markup=kbrd).message_id)

def input_pizza_name(bot : TeleBot, user : User, msg : Message) -> None:
    """Ожидаение ввода имени пиццы"""
    Garbage_Collector.add_garbage_commid(user.id, msg.message_id)
    Garbage_Collector.Clear(bot, user.id)
    kbrd = Keyboard.get_keyboard_cancel(user, "[select_pizza]")
    Garbage_Collector.add_garbage_commid(user.id, bot.send_message(user.id, langer[user.lang]['input_pizza_name'], reply_markup=kbrd).message_id)
    bot.register_next_step_handler(msg, lambda message : action_input_pizza_name(bot, user, message))

def input_pizza_preview(bot : TeleBot, user : User, msg : Message) -> None:
    """Ожидаение получения превью пиццы"""
    Garbage_Collector.add_garbage_commid(user.id, msg.message_id)
    Garbage_Collector.Clear(bot, user.id)
    kbrd = Keyboard.get_keyboard_cancel(user, "[show_pizza_detail]")
    Garbage_Collector.add_garbage_commid(user.id, bot.send_message(user.id, langer[user.lang]['input_pizza_preview'], reply_markup=kbrd).message_id)
    bot.register_next_step_handler(msg, lambda message : action_input_pizza_preview(bot, user, message))    

def input_pizza_new_name(bot : TeleBot, user : User, msg : Message, lang : str) -> None:
    """Ожидаение получения превью пиццы"""
    Garbage_Collector.add_garbage_commid(user.id, msg.message_id)
    Garbage_Collector.Clear(bot, user.id)
    kbrd = Keyboard.get_keyboard_cancel(user, "[show_pizza_detail]")
    Garbage_Collector.add_garbage_commid(user.id, bot.send_message(user.id, langer[user.lang]['input_pizza_new_name'], reply_markup=kbrd).message_id)
    bot.register_next_step_handler(msg, lambda message : action_input_new_name(bot, user, message, lang))  

def input_pizza_new_description(bot : TeleBot, user : User, msg : Message, lang : str) -> None:
    """Ожидаение получения превью пиццы"""
    Garbage_Collector.add_garbage_commid(user.id, msg.message_id)
    Garbage_Collector.Clear(bot, user.id)
    kbrd = Keyboard.get_keyboard_cancel(user, "[show_pizza_detail]")
    Garbage_Collector.add_garbage_commid(user.id, bot.send_message(user.id, langer[user.lang]['input_pizza_new_description'], reply_markup=kbrd).message_id)
    bot.register_next_step_handler(msg, lambda message : action_input_new_description(bot, user, message, lang))  

def input_pizza_new_cost(bot : TeleBot, user : User, msg : Message, type : str) -> None:
    """Ожидаение получения превью пиццы"""
    Garbage_Collector.add_garbage_commid(user.id, msg.message_id)
    Garbage_Collector.Clear(bot, user.id)
    kbrd = Keyboard.get_keyboard_cancel(user, "[show_pizza_detail]")
    Garbage_Collector.add_garbage_commid(user.id, bot.send_message(user.id, langer[user.lang]['input_pizza_new_cost'], reply_markup=kbrd).message_id)
    bot.register_next_step_handler(msg, lambda message : action_input_new_cost(bot, user, message, type))  

def action_input_new_cost(bot : TeleBot, user : User, msg : Message, type : str) -> None:
    """Указать новое имя"""
    Garbage_Collector.add_garbage_commid(user.id, msg.message_id)
    food_uid = Locator.get_food(user.id)
    if msg.text.isdigit():        
        DBPizza.set_pizza_cost(food_uid, msg.text, type)
    show_pizza_information(bot, user, food_uid)

def action_input_new_description(bot : TeleBot, user : User, msg : Message, lang : str) -> None:
    """Указать новое имя"""
    Garbage_Collector.add_garbage_commid(user.id, msg.message_id)
    food_uid = Locator.get_food(user.id)
    DBPizza.set_pizza_description(food_uid, msg.text, lang)
    show_pizza_information(bot, user, food_uid)

def action_input_new_name(bot : TeleBot, user : User, msg : Message, lang : str) -> None:
    """Указать новое имя"""
    Garbage_Collector.add_garbage_commid(user.id, msg.message_id)
    food_uid = Locator.get_food(user.id)
    DBPizza.set_pizza_name(food_uid, msg.text, lang)
    show_pizza_information(bot, user, food_uid)

def action_input_pizza_name(bot : TeleBot, user : User, msg : Message) ->None:
    """Получение имени пиццы"""
    Garbage_Collector.add_garbage(user.id, msg.message_id)
    DBPizza.add_pizza(msg.text)
    show_pizza_list(bot, user)

def action_input_pizza_preview(bot : TeleBot, user : User, msg : Message) ->None:
    """Получение превью пиццы"""
    Garbage_Collector.add_garbage(user.id, msg.message_id)
    food_uid = Locator.get_food(user.id)  
    if msg.content_type == "photo":
        DBPizza.set_preview(food_uid, msg.photo[len(msg.photo)-1].file_id)
    show_pizza_information(bot, user, food_uid)