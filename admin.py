from discount_pizza import DiscountPizza
from gen_excell import GenExcell
from mailer import Mailer
from price_manager import PriceManager
from reserved import Reserved
from db_user import DBUser
from telebot import TeleBot
from configparser import ConfigParser
from telebot.types import Message
from garbage_collector import Garbage_Collector
from keyboard import Keyboard
from user import User
from utils import Utils
from threading import Thread
from locator import Locator
import sqlite3
import food
import os
import time


langer = ConfigParser()
langer.read("data/langs.ini", encoding="utf8")

def main_panel_admin(bot : TeleBot, user : User) -> None:
    """Вывести главную панель пользователя"""
    Locator.clear(user.id)
    Garbage_Collector.Clear(bot, user.id)
    kbrd = Keyboard.get_keyboard_admin_panel(user)
    Garbage_Collector.add_garbage(user.id, bot.send_message(user.id, f"{langer[user.lang]['hello']}", reply_markup=kbrd).message_id)
def set_discount_cost(bot : TeleBot, user : User, msg : Message) -> None:
    """Указать стоимость скидки"""
    Garbage_Collector.Clear(bot, user.id)
    kbrd = Keyboard.get_keyboard_cancel(user, "[set_discount_count]")
    Garbage_Collector.add_garbage(user.id, bot.send_message(user.id, f"{langer[user.lang]['input_discount_cost']}", reply_markup=kbrd).message_id)
    bot.register_next_step_handler(msg, lambda message : input_discount_cost(bot, message, user))
def try_action(cancel : str, text : str, funct, bot : TeleBot, user : User, msg : Message) -> None:
    """Функция повтора, в случае не верных данных"""
    kbrd = Keyboard.get_keyboard_cancel(user, cancel)
    Garbage_Collector.add_garbage(user.id, bot.send_message(user.id, f"{langer[user.lang][text]}", reply_markup=kbrd).message_id)
    bot.register_next_step_handler(msg, lambda message : funct(bot, message, user))        
def input_discount_cost(bot : TeleBot, msg : Message, user : User) -> None:
    """Получение скидки"""
    Garbage_Collector.Clear(bot, user.id)
    inputed = msg.text
    if inputed.isdigit():
        inputed = int(inputed)
        if inputed > 0:
            DiscountPizza.set_discount_cost(inputed)
            main_panel_admin(bot, user)
        else:
            try_action("[set_discount_count]", 'input_discount_cost', input_discount_cost, bot, user, msg) 
    else:
        try_action("[set_discount_count]", 'input_discount_cost', input_discount_cost, bot, user, msg)

def show_history_panel(bot : TeleBot, user : User) -> None:
    """Экспорт истории панель"""
    Garbage_Collector.Clear(bot, user.id)
    Reserved.set_reserved(user.id, 0, "*")
    Reserved.set_reserved(user.id, 1, "*")
    kbrd = Keyboard.get_keyboard_admin_history(user)
    Garbage_Collector.add_garbage(user.id, bot.send_message(user.id, f"{langer[user.lang]['select_history_pereod']}", reply_markup=kbrd).message_id)        
def show_history_by_date(bot : TeleBot, user : User) -> None:
    """Экспорт данных по дате"""
    date_from = Reserved.get_reserved(user.id, 0)
    date_to = Reserved.get_reserved(user.id, 1)
    text = f"{langer[user.lang]['date_from']} {date_from}\r\n"
    text += f"{langer[user.lang]['date_to']} {date_to}\r\n"
    Garbage_Collector.Clear(bot, user.id)
    kbrd = Keyboard.get_keyboard_admin_history_select_date(user)
    Garbage_Collector.add_garbage(user.id, bot.send_message(user.id, text, reply_markup=kbrd).message_id)            
def show_mailer_panel(bot : TeleBot, user : User) -> None:
    """Вывод панели рассылки"""
    Garbage_Collector.Clear(bot, user.id)
    kbrd = Keyboard.get_keyboard_admin_mailer(user)
    Garbage_Collector.add_garbage(user.id, bot.send_message(user.id, f"{langer[user.lang]['select_mailer_method']}", reply_markup=kbrd).message_id)    
def show_prices_manager(bot : TeleBot, user : User) -> None:
    """Панель управление ценами"""
    Garbage_Collector.Clear(bot, user.id)
    kbrd = Keyboard.get_keyboard_admin_price_managment(user)
    Garbage_Collector.add_garbage(user.id, bot.send_message(user.id, f"{langer[user.lang]['price_managment']}", reply_markup=kbrd).message_id)
def show_category_managment(bot : TeleBot, user : User) -> None:
    """Управление категориями"""
    Garbage_Collector.Clear(bot, user.id)
    kbrd = Keyboard.get_keyboard_admin_category_panel(user)
    Garbage_Collector.add_garbage(user.id, bot.send_message(user.id, f"{langer[user.lang]['selectCategoryAdmin']}", reply_markup=kbrd).message_id)
def dialog_add_subcategory(msg : Message, bot : TeleBot, user : User) -> None:
    """добавить субкатегорию"""
    Garbage_Collector.Clear(bot, user.id)
    kbrd = Keyboard.get_keyboard_cancel(user, "[show_foods_managment]")
    Garbage_Collector.add_garbage(user.id, bot.send_message(user.id, f"{langer[user.lang]['input_add_subcategory']}", reply_markup=kbrd).message_id)
    bot.register_next_step_handler(msg, lambda message : action_create_new_subcategory(bot, message, user)) 
def action_create_new_subcategory(bot : TeleBot, msg : Message, user : User) -> None:
    """Создание новой подкатегории"""
    category_uid = Locator.get_category(user.id)
    food.add_subcategory(category_uid, msg.text)
    show_foods_managment(bot, user)
def show_foods_managment(bot : TeleBot, user : User) -> None:
    """Управление блюдами"""
    Garbage_Collector.Clear(bot, user.id)
    kbrd = Keyboard.get_keyboard_admin_food_mangment(user)
    Garbage_Collector.add_garbage(user.id, bot.send_message(user.id, f"{langer[user.lang]['foodManagment']}", reply_markup=kbrd).message_id)    
def add_food(msg : Message, bot : TeleBot, user : User) -> None:
    """Добавить новое блюдо"""
    Garbage_Collector.Clear(bot, user.id)
    Garbage_Collector.add_garbage(user.id, bot.send_message(user.id, f"{langer[user.lang]['inputFoodName']}").message_id)
    bot.register_next_step_handler(msg, lambda message : action_create_new_food(bot, message, user))    
def add_category_panel(msg : Message, bot : TeleBot, user : User) -> None:
    """Создание новой категории"""
    Garbage_Collector.Clear(bot, user.id)
    Garbage_Collector.add_garbage(user.id, bot.send_message(user.id, f"{langer[user.lang]['inputCategoryNameAdmin']}").message_id)
    bot.register_next_step_handler(msg, lambda message : action_add_category(bot, message, user))    

def authrization_admin(msg : Message, bot : TeleBot, user : User) -> None:
    """Авторизация админа"""
    Garbage_Collector.Clear(bot, user.id)
    Garbage_Collector.add_garbage(user.id, bot.send_message(user.id, f"{langer[user.lang]['inputPswdForAdmin']}").message_id)
    bot.register_next_step_handler(msg, lambda message : action_check_admin_password(bot, message, user)) 

def show_food_info_managment(bot : TeleBot, user : User, category_uid : str, food_uid : str) -> None:
    """Управление товарами"""
    Garbage_Collector.Clear(bot, user.id)
    kbrd = Keyboard.get_keyboard_admin_food_info_managment(user, category_uid, food_uid)
    afood = food.get_food(category_uid, food_uid)
    text = ""
    text += f"{langer[user.lang]['name']} (ру) {afood['name_ru']}\r\n"
    text += f"{langer[user.lang]['name']} (уз) {afood['name_uz']}\r\n"
    text += f"{langer[user.lang]['name']} (ен) {afood['name_en']}\r\n"
    text += f"{langer[user.lang]['description']} (ру) {afood['description_ru']}\r\n"
    text += f"{langer[user.lang]['description']} (уз) {afood['description_uz']}\r\n"
    text += f"{langer[user.lang]['description']} (ен) {afood['description_en']}\r\n"
    text += f"{langer[user.lang]['cost']} {Utils.to_razr(afood['cost'])}\r\n"
    if afood['img'] == '':
        text += langer[user.lang]['no_preview']
    else:
        Garbage_Collector.add_garbage(user.id, bot.send_photo(user.id, afood['img']).message_id) 
    Garbage_Collector.add_garbage(user.id, bot.send_message(user.id, text, reply_markup=kbrd).message_id) 
def change_preview(msg : Message, bot : TeleBot, user : User) -> None:
    """Указать превью"""
    Garbage_Collector.Clear(bot, user.id)
    Garbage_Collector.add_garbage(user.id, bot.send_message(user.id, f"{langer[user.lang]['forSetPreview']}").message_id)
    bot.register_next_step_handler(msg, lambda message : action_set_preview(bot, message, user))   
def change_cost(msg : Message, bot : TeleBot, user : User) -> None:
    """Указать стоимость"""
    Garbage_Collector.Clear(bot, user.id)
    Garbage_Collector.add_garbage(user.id, bot.send_message(user.id, f"{langer[user.lang]['inputNewPrice']}").message_id)
    bot.register_next_step_handler(msg, lambda message : action_change_cost(bot, message, user))       
def change_food_name(msg : Message, bot : TeleBot, user : User, lang) -> None:
    """Изменить имя"""
    Garbage_Collector.Clear(bot, user.id)
    Garbage_Collector.add_garbage(user.id, bot.send_message(user.id, f"{langer[user.lang]['inputNewName']}").message_id)
    bot.register_next_step_handler(msg, lambda message : action_set_new_name(bot, message, user, lang))  
def change_food_description(msg : Message, bot : TeleBot, user : User, lang : str) -> None:
    """Изменить описание"""
    Garbage_Collector.Clear(bot, user.id)
    Garbage_Collector.add_garbage(user.id, bot.send_message(user.id, f"{langer[user.lang]['inputNewDescription']}").message_id)
    bot.register_next_step_handler(msg, lambda message : action_set_new_description(bot, message, user, lang))      
def change_cashback_per_buy(msg : Message, bot : TeleBot, user : User) -> None:
    """Изменения стоимости cashback за покупку"""
    Garbage_Collector.Clear(bot, user.id)
    kbrd = Keyboard.get_keyboard_cancel(user, "[price_managment]")
    Garbage_Collector.add_garbage(user.id, bot.send_message(user.id, f"{langer[user.lang]['new_cashback_buy']}", reply_markup=kbrd).message_id)
    bot.register_next_step_handler(msg, lambda message : action_set_new_cashback_per_buy(bot, message, user))      
def change_cashback_per_month(msg : Message, bot : TeleBot, user : User) -> None:
    """Изменения стоимости cashback за покупку"""
    Garbage_Collector.Clear(bot, user.id)
    kbrd = Keyboard.get_keyboard_cancel(user, "[price_managment]")
    Garbage_Collector.add_garbage(user.id, bot.send_message(user.id, f"{langer[user.lang]['new_cashback_buy']}", reply_markup=kbrd).message_id)
    bot.register_next_step_handler(msg, lambda message : action_set_new_cashback_per_month(bot, message, user))      
def change_road_price(msg : Message, bot : TeleBot, user : User) -> None:
    """Изменения стоимости cashback за покупку"""
    Garbage_Collector.Clear(bot, user.id)
    kbrd = Keyboard.get_keyboard_cancel(user, "[price_managment]")
    Garbage_Collector.add_garbage(user.id, bot.send_message(user.id, f"{langer[user.lang]['new_road_price']}", reply_markup=kbrd).message_id)
    bot.register_next_step_handler(msg, lambda message : action_set_new_road_price(bot, message, user))      
def show_dialog_input_text_ru_just_text(msg : Message, bot : TeleBot, user : User) -> None:
    """Ввести сообщение на русском языке"""
    Garbage_Collector.Clear(bot, user.id)
    kbrd = Keyboard.get_keyboard_cancel(user, "[mailer]")
    Garbage_Collector.add_garbage(user.id, bot.send_message(user.id, f"{langer[user.lang]['input_message_text_for_russian_auditory']}", reply_markup=kbrd).message_id)
    bot.register_next_step_handler(msg, lambda message : action_input_text_message_ru(bot, message, user))          
def show_dialog_input_text_uz_just_text(msg : Message, bot : TeleBot, user : User) -> None:
    """Ввести сообщение на русском языке"""
    Garbage_Collector.Clear(bot, user.id)
    kbrd = Keyboard.get_keyboard_cancel(user, "[mailer]")
    Garbage_Collector.add_garbage(user.id, bot.send_message(user.id, f"{langer[user.lang]['input_message_text_for_uzbek_auditory']}", reply_markup=kbrd).message_id)
    bot.register_next_step_handler(msg, lambda message : action_input_text_message_uz(bot, message, user))  
def show_dialog_input_text_en_just_text(msg : Message, bot : TeleBot, user : User) -> None:
    """Ввести сообщение на русском языке"""
    Garbage_Collector.Clear(bot, user.id)
    kbrd = Keyboard.get_keyboard_cancel(user, "[mailer]")
    Garbage_Collector.add_garbage(user.id, bot.send_message(user.id, f"{langer[user.lang]['input_message_text_for_english_auditory']}", reply_markup=kbrd).message_id)
    bot.register_next_step_handler(msg, lambda message : action_input_text_message_en(bot, message, user))
def show_dialog_input_image_ru(msg : Message, bot : TeleBot, user : User) -> None:
    """Получить картинку для русской аудитории"""
    Garbage_Collector.Clear(bot, user.id)
    kbrd = Keyboard.get_keyboard_cancel(user, "[mailer]")
    Garbage_Collector.add_garbage(user.id, bot.send_message(user.id, f"{langer[user.lang]['input_message_img_for_russian_auditory']}", reply_markup=kbrd).message_id)
    bot.register_next_step_handler(msg, lambda message : action_input_image_message_ru(bot, message, user))   
def show_dialog_input_image_ru_title(msg : Message, bot : TeleBot, user : User) -> None:
    """Получить картинку для русской аудитории"""
    Garbage_Collector.Clear(bot, user.id)
    kbrd = Keyboard.get_keyboard_cancel(user, "[mailer]")
    Garbage_Collector.add_garbage(user.id, bot.send_message(user.id, f"{langer[user.lang]['input_message_img_for_russian_auditory_title']}", reply_markup=kbrd).message_id)
    bot.register_next_step_handler(msg, lambda message : action_input_image_message_ru_title(bot, message, user)) 
def show_dialog_input_image_uz(msg : Message, bot : TeleBot, user : User) -> None:
    """Получить картинку для русской аудитории"""
    Garbage_Collector.Clear(bot, user.id)
    kbrd = Keyboard.get_keyboard_cancel(user, "[mailer]")
    Garbage_Collector.add_garbage(user.id, bot.send_message(user.id, f"{langer[user.lang]['input_message_img_for_uzbek_auditory']}", reply_markup=kbrd).message_id)
    bot.register_next_step_handler(msg, lambda message : action_input_image_message_uz(bot, message, user))  
def show_dialog_input_image_uz_title(msg : Message, bot : TeleBot, user : User) -> None:
    """Получить картинку для русской аудитории"""
    Garbage_Collector.Clear(bot, user.id)
    kbrd = Keyboard.get_keyboard_cancel(user, "[mailer]")
    Garbage_Collector.add_garbage(user.id, bot.send_message(user.id, f"{langer[user.lang]['input_message_img_for_uzbek_auditory_title']}", reply_markup=kbrd).message_id)
    bot.register_next_step_handler(msg, lambda message : action_input_image_message_uz_title(bot, message, user))     

def show_dialog_input_image_en(msg : Message, bot : TeleBot, user : User) -> None:
    """Получить картинку для русской аудитории"""
    Garbage_Collector.Clear(bot, user.id)
    kbrd = Keyboard.get_keyboard_cancel(user, "[mailer]")
    Garbage_Collector.add_garbage(user.id, bot.send_message(user.id, f"{langer[user.lang]['input_message_img_for_english_auditory']}", reply_markup=kbrd).message_id)
    bot.register_next_step_handler(msg, lambda message : action_input_image_message_en(bot, message, user))   
def show_dialog_input_image_en_title(msg : Message, bot : TeleBot, user : User) -> None:
    """Получить картинку для русской аудитории"""
    Garbage_Collector.Clear(bot, user.id)
    kbrd = Keyboard.get_keyboard_cancel(user, "[mailer]")
    Garbage_Collector.add_garbage(user.id, bot.send_message(user.id, f"{langer[user.lang]['input_message_img_for_english_auditory_title']}", reply_markup=kbrd).message_id)
    bot.register_next_step_handler(msg, lambda message : action_input_image_message_en_title(bot, message, user)) 


def show_dialog_set_date_from(msg : Message, bot : TeleBot, user : User) -> None:
    """Ввести начальную дату"""
    Garbage_Collector.Clear(bot, user.id)
    kbrd = Keyboard.get_keyboard_cancel(user, "[history_date]")
    Garbage_Collector.add_garbage(user.id, bot.send_message(user.id, f"{langer[user.lang]['input_date_from']}", reply_markup=kbrd).message_id)
    bot.register_next_step_handler(msg, lambda message : action_set_date_from(bot, message, user))       
def show_dialog_set_date_to(msg : Message, bot : TeleBot, user : User) -> None:
    """Ввести начальную дату"""
    Garbage_Collector.Clear(bot, user.id)
    kbrd = Keyboard.get_keyboard_cancel(user, "[history_date]")
    Garbage_Collector.add_garbage(user.id, bot.send_message(user.id, f"{langer[user.lang]['input_date_from']}", reply_markup=kbrd).message_id)
    bot.register_next_step_handler(msg, lambda message : action_set_date_to(bot, message, user))  
def show_dialog_history_by_date(bot : TeleBot, user : User) -> None:
    """Получить историю по дате"""
    action_history_all(bot, user)
def show_rename_category(msg : Message, bot : TeleBot, user : User, lang : str) -> None:
    """Ввести новое имя категории"""
    Garbage_Collector.Clear(bot, user.id)
    kbrd = Keyboard.get_keyboard_cancel(user, "[choiseCategory]")
    Garbage_Collector.add_garbage(user.id, bot.send_message(user.id, f"{langer[user.lang]['input_new_category_name']}", reply_markup=kbrd).message_id)
    bot.register_next_step_handler(msg, lambda message : action_set_new_name_category(bot, message, user, lang))  
def show_dialog_user_detail(msg : Message, bot : TeleBot, user : User) -> None:
    """Информация о пользователе"""
    Garbage_Collector.Clear(bot, user.id)
    kbrd = Keyboard.get_keyboard_cancel(user, "[main_panel_admin]")
    Garbage_Collector.add_garbage(user.id, bot.send_message(user.id, f"{langer[user.lang]['input_user_phone']}", reply_markup=kbrd).message_id)
    bot.register_next_step_handler(msg, lambda message : action_get_phone_number(bot, message, user))
def dialog_set_cashback_count(msg : Message, bot : TeleBot, user : User) -> None:
    """Установить кешбек пользователю"""
    Garbage_Collector.Clear(bot, user.id)
    kbrd = Keyboard.get_keyboard_cancel(user, "[main_panel_admin]")
    Garbage_Collector.add_garbage(user.id, bot.send_message(user.id, f"{langer[user.lang]['input_cashback']}", reply_markup=kbrd).message_id)
    bot.register_next_step_handler(msg, lambda message : action_set_cashback(bot, message, user))    
def show_user_detail(bot : TeleBot, user : User, phone_number : str) -> None:
    """вывести информацию о пользователе"""
    Garbage_Collector.Clear(bot, user.id)
    ui = DBUser.get_user_by_phone_number(phone_number)
    if ui != False:
        Reserved.set_reserved(user.id, 0, ui["id"])
        Reserved.set_reserved(user.id, 1, phone_number)
        text  = f"{langer[user.lang]['name']} {ui['name']}\r\n"
        text += f"{langer[user.lang]['username']} @{ui['username']}\r\n"
        text += f"{langer[user.lang]['phone_number']} {ui['phone']}\r\n"
        text += f"{langer[user.lang]['lang']} {ui['lang']}\r\n"
        text += f"{langer[user.lang]['date_register']} {ui['date_register']}\r\n"
        text += f"{langer[user.lang]['date_last_action']} {ui['date_last_action']}\r\n"
        text += f"{langer[user.lang]['cashback']} {ui['cashback']}\r\n"
        text += f"{langer[user.lang]['buy_all']} {ui['buy_all']}\r\n"
        text += f"{langer[user.lang]['buy_month']} {ui['buy_month']}\r\n"
        kbrd = Keyboard.get_keyboard_admin_user_detail(user)
    else:
        text = langer[user.lang]['user_not_found']
        kbrd = Keyboard.get_keyboard_cancel(user, "[main_panel_admin]")
    Garbage_Collector.add_garbage(user.id, bot.send_message(user.id, text, reply_markup=kbrd).message_id)
###actions
def action_set_cashback(bot : TeleBot, msg : Message,  user : User) -> None:
    """Установить кол-во кешбек"""
    Garbage_Collector.add_garbage(user.id, msg.message_id)
    if msg.text.isdigit():
        DBUser.set_cashback(Reserved.get_reserved(user.id, 0), msg.text)
    show_user_detail(bot, user, Reserved.get_reserved(user.id, 1))
    
def action_get_users_list_who_not_buy(bot : TeleBot,  user : User) -> None:
    """Получить excel пользователей кто не покупал"""
    file_name = f"{user.id}.xlsx"
    GenExcell.gen_users_list_Who_not_buy(file_name)
    with open(file_name, "rb") as f:
        bot.send_document(user.id, f)
    os.remove(file_name)
    main_panel_admin(bot, user)    
def action_get_users_list(bot : TeleBot,  user : User) -> None:
    """Получить excel пользователей"""
    file_name = f"{user.id}.xlsx"
    GenExcell.gen_users_list(file_name)
    with open(file_name, "rb") as f:
        bot.send_document(user.id, f)
    os.remove(file_name)
    main_panel_admin(bot, user)

def action_get_phone_number(bot : TeleBot, msg : Message, user : User) -> None:
    """Получить пользователя по номеру телефона"""
    Garbage_Collector.add_garbage(user.id, msg.message_id)
    if Utils.is_valid_number(msg.text):
        show_user_detail(bot, user, msg.text)
    else:
        kbrd = Keyboard.get_keyboard_cancel(user, "[main_panel_admin]")
        Garbage_Collector.add_garbage(user.id, bot.send_message(user.id, f"{langer[user.lang]['invalid_phone_number']}", reply_markup=kbrd).message_id)
        bot.register_next_step_handler(msg, lambda message : action_get_phone_number(bot, message, user))        

def action_set_new_name_category(bot : TeleBot, msg : Message, user : User, lang : str) -> None:
    """Переименновать категорию"""
    Garbage_Collector.add_garbage(user.id, msg.message_id)
    Garbage_Collector.Clear(bot, user.id)    
    if len(msg.text) < 28:
        locator = Locator.get_locator(user.id)
        food.rename_category(locator['category_uid'], locator['subcategory_uid'], msg.text, lang)
        show_category_managment(bot, user)
    else:
        kbrd = Keyboard.get_keyboard_cancel(user, "[choiseCategory]")
        Garbage_Collector.add_garbage(user.id, bot.send_message(user.id, f"{langer[user.lang]['limit_text']}", reply_markup=kbrd).message_id)
        bot.register_next_step_handler(msg, lambda message : action_set_new_name_category(bot, message, user))
def action_set_date_from(bot : TeleBot, msg : Message, user : User) -> None:
    """Ввести начальную дату"""
    Garbage_Collector.add_garbage(user.id, msg.message_id)
    Garbage_Collector.Clear(bot, user.id)
    date = msg.text
    if date == '*' or Utils.is_valid_date(date):
        Reserved.set_reserved(user.id, 0, msg.text)
        show_history_by_date(bot, user)
    else:
        kbrd = Keyboard.get_keyboard_cancel(user, "[history_date]")
        Garbage_Collector.add_garbage(user.id, bot.send_message(user.id, f"{langer[user.lang]['invalid_date']}", reply_markup=kbrd).message_id)
        bot.register_next_step_handler(msg, lambda message : action_set_date_from(bot, message, user))  
def action_set_date_to(bot : TeleBot, msg : Message, user : User) -> None:
    """Ввести начальную дату"""
    Garbage_Collector.add_garbage(user.id, msg.message_id)
    Garbage_Collector.Clear(bot, user.id)
    date = msg.text
    if date == '*' or Utils.is_valid_date(date):
        Reserved.set_reserved(user.id, 1, msg.text)
        show_history_by_date(bot, user)
    else:
        kbrd = Keyboard.get_keyboard_cancel(user, "[history_date]")
        Garbage_Collector.add_garbage(user.id, bot.send_message(user.id, f"{langer[user.lang]['invalid_date']}", reply_markup=kbrd).message_id)
        bot.register_next_step_handler(msg, lambda message : action_set_date_to(bot, message, user))  

def action_history_all(bot : TeleBot, user : User) -> None:
    """Экспорт всей истории"""
    Garbage_Collector.Clear(bot, user.id)
    file_name = f"{user.id}.xlsx"
    GenExcell.gen_history(file_name, Reserved.get_reserved(user.id, 0), Reserved.get_reserved(user.id, 1))
    with open(file_name, "rb") as f:
        bot.send_document(user.id, f)
    os.remove(file_name)
    main_panel_admin(bot, user)

def action_input_image_message_ru(bot : TeleBot, msg : Message, user : User) -> None:
    """Получить и сохранить картинку для русской аудитории"""
    Garbage_Collector.add_garbage(user.id, msg.message_id)
    Garbage_Collector.Clear(bot, user.id)
    if msg.content_type == "photo":
        Mailer.set_img_name("ru", msg.photo[len(msg.photo)-1].file_id)
        show_dialog_input_image_ru_title(msg, bot, user)
    else:
        kbrd = Keyboard.get_keyboard_cancel(user, "[mailer]")
        Garbage_Collector.add_garbage(user.id, bot.send_message(user.id, f"{langer[user.lang]['need_input_photo']}", reply_markup=kbrd).message_id)
        bot.register_next_step_handler(msg, lambda message : action_input_image_message_ru(bot, message, user))
def action_input_image_message_uz(bot : TeleBot, msg : Message, user : User) -> None:
    """Получить и сохранить картинку для узбекской аудитории"""
    Garbage_Collector.add_garbage(user.id, msg.message_id)
    Garbage_Collector.Clear(bot, user.id)
    if msg.content_type == "photo":
        Mailer.set_img_name("uz", msg.photo[len(msg.photo)-1].file_id)
        show_dialog_input_image_uz_title(msg, bot, user)
    else:
        kbrd = Keyboard.get_keyboard_cancel(user, "[mailer]")
        Garbage_Collector.add_garbage(user.id, bot.send_message(user.id, f"{langer[user.lang]['need_input_photo']}", reply_markup=kbrd).message_id)
        bot.register_next_step_handler(msg, lambda message : action_input_image_message_uz(bot, message, user))
def action_input_image_message_en(bot : TeleBot, msg : Message, user : User) -> None:
    """Получить и сохранить картинку для английской аудитории"""
    Garbage_Collector.add_garbage(user.id, msg.message_id)
    Garbage_Collector.Clear(bot, user.id)
    if msg.content_type == "photo":
        Mailer.set_img_name("en", msg.photo[len(msg.photo)-1].file_id)
        show_dialog_input_image_en_title(msg, bot, user)
    else:
        kbrd = Keyboard.get_keyboard_cancel(user, "[mailer]")
        Garbage_Collector.add_garbage(user.id, bot.send_message(user.id, f"{langer[user.lang]['need_input_photo']}", reply_markup=kbrd).message_id)
        bot.register_next_step_handler(msg, lambda message : action_input_image_message_en(bot, message, user))

def action_input_image_message_ru_title(bot : TeleBot, msg : Message, user : User) -> None:
    """Получить и сохранить текст для картинки для русской аудитории"""
    Garbage_Collector.add_garbage(user.id, msg.message_id)
    Garbage_Collector.Clear(bot, user.id)
    Mailer.set_img_title("ru", msg.text)
    show_dialog_input_image_uz(msg, bot, user)
def action_input_image_message_uz_title(bot : TeleBot, msg : Message, user : User) -> None:
    """Получить и сохранить текст для картинки для узбексой аудитории"""
    Garbage_Collector.add_garbage(user.id, msg.message_id)
    Garbage_Collector.Clear(bot, user.id)
    Mailer.set_img_title("uz", msg.text)
    show_dialog_input_image_en(msg, bot, user)
def action_input_image_message_en_title(bot : TeleBot, msg : Message, user : User) -> None:
    """Получить и сохранить текст для картинки для английской аудитории"""
    Garbage_Collector.add_garbage(user.id, msg.message_id)
    Garbage_Collector.Clear(bot, user.id)
    Mailer.set_img_title("en", msg.text)
    data = Mailer.get_data()
    r = bot.send_message(user.id, f"{langer[user.lang]['current_user_for_send_mail']} 0")
    Thread(target=sub_send_mail_image, args=(bot, data, user, r.message_id,)).start()
    show_mailer_panel(bot, user) 

def sub_send_mail_image(bot : TeleBot, data : dict, user : User, message_id : str) -> None:
    """Подфункция отправки рассылки в потоке"""
    limit_user = 20
    current = 0
    count = 0
    for duser in User.load_all_users():
        if current > limit_user:
            time.sleep(1)
            current = 0
        while True:
            try:
                res = Mailer.send_image(bot, duser['id'], data["img"][duser['lang']], data["description"][duser['lang']])
                if res == False:
                    DBUser.delete_user(duser['id'])
                count += 1
                bot.edit_message_text(f"{langer[user.lang]['current_user_for_send_mail']} {count}", user.id, message_id)
                break
            except:
                time.sleep(2)
        current += 1

def action_input_text_message_ru(bot : TeleBot, msg : Message, user : User) -> None:
    """Ввести сообщение для русской аудитории"""
    Garbage_Collector.add_garbage(user.id, msg.message_id)
    Garbage_Collector.Clear(bot, user.id)
    Reserved.set_reserved(user.id, 0, msg.text)
    show_dialog_input_text_uz_just_text(msg, bot, user)
def action_input_text_message_en(bot : TeleBot, msg : Message, user : User) -> None:
    """Ввести сообщение для англ аудитории"""
    Garbage_Collector.add_garbage(user.id, msg.message_id)
    Garbage_Collector.Clear(bot, user.id)
    text = {
        "ru" : Reserved.get_reserved(user.id, 0),
        "uz" : Reserved.get_reserved(user.id, 1),
        "en" : msg.text,
    }
    r = bot.send_message(user.id, f"{langer[user.lang]['current_user_for_send_mail']} 0")
    Thread(target=sub_send_mail_message, args=(bot, text, user, r.message_id,)).start()
    show_mailer_panel(bot, user)    
def action_input_text_message_uz(bot : TeleBot, msg : Message, user : User) -> None:
    """Ввести сообщение для узб аудитории"""
    Garbage_Collector.add_garbage(user.id, msg.message_id)
    Garbage_Collector.Clear(bot, user.id)
    Reserved.set_reserved(user.id, 1, msg.text)
    show_dialog_input_text_en_just_text(msg, bot, user)

def sub_send_mail_message(bot : TeleBot, text : dict, user : User, message_id : str) -> None:
    """Подфункция отправки рассылки в потоке"""
    limit_user = 20
    current = 0
    count = 0
    for duser in User.load_all_users():
        if current > limit_user:
            time.sleep(2)
            current = 0
        while True:
            try:
                res = Mailer.send_message(bot, duser['id'], text[duser['lang']])
                if res == False:
                    DBUser.delete_user(duser['id'])
                count += 1
                bot.edit_message_text(f"{langer[user.lang]['current_user_for_send_mail']} {count}", user.id, message_id)
                break
            except:
                time.sleep(2)
        current += 1
    
def show_yes_no_buttons(bot : TeleBot, user : User, cmd : str, data : str) -> None:
    """вывести кнопки да нет, для удаления. cmd массив из двух параметров комманда для "да" и для "нет"""""
    Garbage_Collector.Clear(bot, user.id,)
    kbrd = Keyboard.get_keyboard_yes_no(cmd, data, user)
    Garbage_Collector.add_garbage_commid(user.id, bot.send_message(user.id, langer[user.lang]["continue"], reply_markup=kbrd).message_id)

def action_set_new_road_price(bot : TeleBot, msg : Message, user : User) -> None:
    Garbage_Collector.add_garbage(user.id, msg.message_id)
    Garbage_Collector.Clear(bot, user.id)
    cost = msg.text
    if cost.isdigit():
        PriceManager.set_road(cost)
    show_prices_manager(bot, user)
def action_set_new_cashback_per_buy(bot : TeleBot, msg : Message, user : User) -> None:
    Garbage_Collector.add_garbage(user.id, msg.message_id)
    Garbage_Collector.Clear(bot, user.id)
    percent = msg.text
    if Utils.is_float(percent):
        PriceManager.set_cashback_per_buy(percent)
    show_prices_manager(bot, user)
def action_set_new_cashback_per_month(bot : TeleBot, msg : Message, user : User) -> None:
    Garbage_Collector.add_garbage(user.id, msg.message_id)
    Garbage_Collector.Clear(bot, user.id)
    percent = msg.text
    if Utils.is_float(percent):
        PriceManager.set_cashback_per_month(percent)
    show_prices_manager(bot, user)
def action_category(bot : TeleBot, user : User) -> None:
    """Удаление категории"""
    Garbage_Collector.Clear(bot, user.id)
    locator = Locator.get_locator(user.id)
    food.delete_category(locator['category_uid'], locator['subcategory_uid'])    
    show_category_managment(bot, user)
def action_delete_food(bot : TeleBot, user : User) -> None:
    """Удаление блюда"""
    Garbage_Collector.Clear(bot, user.id)
    category_uid = Locator.get_category(user.id)
    food_uid = Locator.get_food(user.id)
    food.delete_food(category_uid, food_uid)    
    show_foods_managment(bot, user)

def action_change_cost(bot : TeleBot, msg : Message, user : User) -> None:
    """Установить превью"""
    Garbage_Collector.add_garbage(user.id, msg.message_id)
    category_uid = Locator.get_category(user.id)
    food_uid = Locator.get_food(user.id)
    if msg.text.isdigit() and int(msg.text) > 0:
        food.set_cost(category_uid, food_uid, msg.text)
    show_food_info_managment(bot, user, category_uid, food_uid) 
def action_set_preview(bot : TeleBot, msg : Message, user : User) -> None:
    """Установить превью"""
    Garbage_Collector.add_garbage(user.id, msg.message_id)
    category_uid = Locator.get_category(user.id)
    food_uid = Locator.get_food(user.id)  
    if msg.text != "0":
        if msg.content_type == "photo":
            food.set_preview(category_uid, food_uid, msg.photo[len(msg.photo)-1].file_id)
    show_food_info_managment(bot, user, category_uid, food_uid) 
def action_set_new_description(bot : TeleBot, msg : Message, user : User, lang : str) -> None:
    Garbage_Collector.add_garbage(user.id, msg.message_id)
    category_uid = Locator.get_category(user.id)
    food_uid = Locator.get_food(user.id)
    if msg.text != "0":
        food.set_new_description(lang, msg.text, category_uid, food_uid)
    show_food_info_managment(bot, user, category_uid, food_uid)  
def action_set_new_name(bot : TeleBot, msg : Message, user : User, lang : str) -> None:
    Garbage_Collector.add_garbage(user.id, msg.message_id)
    if len(msg.text) < 28:
        category_uid = Locator.get_category(user.id)
        food_uid = Locator.get_food(user.id)
        if msg.text != "0":
            food.set_new_name(lang, msg.text, category_uid, food_uid)
        show_food_info_managment(bot, user, category_uid, food_uid)
    else:
        kbrd = Keyboard.get_keyboard_cancel(user, "[foodManagment]")
        Garbage_Collector.add_garbage(user.id, bot.send_message(user.id, f"{langer[user.lang]['limit_text']}", reply_markup=kbrd).message_id)
        bot.register_next_step_handler(msg, lambda message : action_set_new_name(bot, message, user))
        

def action_create_new_food(bot : TeleBot, msg : Message, user : User) -> None:
    """Создать новое блюдо"""
    Garbage_Collector.add_garbage(user.id, msg.message_id)
    locator = Locator.get_locator(user.id)
    if msg.text != "0":        
        food.add_food(locator['category_uid'], locator['subcategory_uid'], msg.text)
    show_foods_managment(bot, user)

def existing_admin(id : str) -> bool:
    with sqlite3.connect("db/admin.db") as con:
        return True if con.cursor().execute(f"SELECT id FROM ids WHERE id='{id}'").fetchone() != None else False

def valid_admin_password(pswd : str) -> bool:
    ### получить пароль
    real_pswd = "2992"
    return pswd == real_pswd

def action_add_category(bot : TeleBot, msg : Message, user : User) -> None:
    """Создание новой категории"""
    Garbage_Collector.add_garbage(user.id, msg.message_id)
    if msg.text != "0":
        if food.existing_category(msg.text) == False:
            food.add_category(msg.text)
            show_category_managment(bot, user)
        else: 
            Garbage_Collector.add_garbage(user.id, bot.send_message(user.id, f"{langer[user.lang]['existingCategoryAdmin']}").message_id)
            bot.register_next_step_handler(msg, lambda message : action_add_category(bot, message, user))   
    else: show_category_managment(bot, user)
def action_check_admin_password(bot : TeleBot, msg : Message, user : User) -> None:
    """Проверка пароля"""
    Garbage_Collector.add_garbage(user.id, msg.message_id)
    Garbage_Collector.Clear(bot, user.id)
    if msg.text != "0":
        if valid_admin_password(msg.text): 
            ###Проверить на валидность
            bot.set_my_commands([{
                "command" : "/adm_man",
                "description" : "Админка"
            }])
            remember_admin(user.id)
            main_panel_admin(bot, user)
        else:
            Garbage_Collector.add_garbage(user.id, bot.send_message(user.id, langer[user.lang]['invalidPassword']).message_id)
            bot.register_next_step_handler(msg, lambda message : action_check_admin_password(bot, message, user))
    else: Garbage_Collector.Clear(bot, user.id)

def remember_admin(user_id : str) -> None:
    """Запоминаем id админа"""
    with sqlite3.connect("db/admin.db") as con:
        con.cursor().execute(f"INSERT INTO ids VALUES('{user_id}')")