
from keyboard import Keyboard
from locator import Locator
from utils import Utils
from order import Order
from history import History
from threading import Thread

from telebot.types import Message
from db_user import DBUser
from log import Log
from user import User
from garbage_collector import Garbage_Collector
from configparser import ConfigParser
from reserved import Reserved
import food
import telebot
import config
import user_panel
import admin
import basket
import menu_pizza
import DBPizza

bot = telebot.TeleBot(config.TELEGRAM_TOKEN)
_log_action = Log("log_action.txt")
lang = None
langer = ConfigParser()
langer.read("data/langs.ini", encoding="utf8")

_log_action.paste_separator()
_log_action.paste_data("Запуск бота")
@bot.message_handler(content_types=["text", "contact", "photo", "location", "successful_payment"])
def start(msg : Message):
    global langer
    user = User.load_user(msg.from_user)
    Locator.clear(user.id)
    if msg.content_type == "successful_payment":
        user_panel.buy(bot, User.load_user_from_id(msg.from_user.id), True, True, True, msg.successful_payment.invoice_payload)
    else:
        if msg.chat.type == "private":
            Garbage_Collector.add_garbage_commid(user.id, msg.message_id)
            r = DBUser.existing_user(user.id)
            if r == False:
                DBUser.add_user(user)
                user_panel.select_language_user_begin_register(bot, user)
            else:
                if DBUser.existing_phone_number(user.id):
                    if msg.text == "/adm_man": 
                        if admin.existing_admin(user.id): admin.main_panel_admin(bot, user)
                        else: admin.authrization_admin(msg, bot, user)
                    else: user_panel.main_panel_user(bot, user.id, user.lang)
                else: user_panel.select_language_user_begin_register(bot, user)
    DBUser.update_user(user.id, user.username, user.date_last_action)
@bot.pre_checkout_query_handler(func=lambda call: True)
def ex(call):
    bot.answer_pre_checkout_query(call.id, ok=True)
@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    user = User.load_user(call.from_user)
    if call.data.startswith("[selected_lang_beg_reg]"): 
        user.lang = call.data.replace("[selected_lang_beg_reg]", "")
        DBUser.change_language(user.id, user.lang)
        user_panel.set_name_user_begin_register(call.message, bot, user)
    elif DBUser.existing_user(user.id) == False:
        DBUser.add_user(user)
        user_panel.select_language_user_begin_register(bot, user)
    elif DBUser.existing_phone_number(user.id) == False:
        user_panel.select_language_user_begin_register(bot, user)
    elif call.data.startswith("[selected_lang]"):
        user.lang = call.data.replace("[selected_lang]", "")
        DBUser.change_language(user.id, user.lang)
        user_panel.main_panel_user(bot, user.id, user.lang)
    elif call.data == "[back]": user_panel.main_panel_user(bot, user.id, user.lang)
    elif call.data == "[users_detail]": admin.action_get_users_list(bot, user)
    elif call.data == "[user_who_not_buy]": admin.action_get_users_list_who_not_buy(bot, user)
    elif call.data == "[change_language]": user_panel.select_language_user(bot, user.id, user.lang)
    #elif call.data == "[order]": user_panel.order_manager_user(bot, user)
    elif call.data == "[order]": user_panel.choise_category_user(bot, user)
    elif call.data == "[no_comment]": user_panel.action_set_comment(bot, user, "[no_comment]")
    elif call.data == "[pay]": user_panel.choise_dilivery(bot, user)
    elif call.data == "[set_comment]": user_panel.set_comment(bot, user, call.message)
    elif call.data == "[choiseCategory]": user_panel.choise_category_user(bot, user)
    elif call.data == "[settings]": user_panel.setting_panel_user(bot, user.id, user.lang)
    elif call.data == "[setName]": user_panel.set_name_user(call.message, bot, user)
    elif call.data == "[setPhoneNumber]": user_panel.set_phone_number_user(bot, user, call.message, user.id, user.lang)
    elif call.data == "[foodManagment]": admin.show_category_managment(bot, user)
    elif call.data == "[dilivery]": user_panel.set_address_dilivery(call.message, bot, user)
    elif call.data == "[self_dilivery]": user_panel.self_dilivery(bot, user)
    elif call.data == "[click]": user_panel.final_order_check(bot, user, "click")
    elif call.data == "[payme]": user_panel.final_order_check(bot, user, "payme")
    elif call.data == "[money]": user_panel.final_order_check(bot, user, "money")
    elif call.data == "[cashback]": user_panel.final_order_check(bot, user, "cashback")
    elif call.data == "[finish]": user_panel.final_order(bot, user)
    elif call.data == "[addFood]": admin.add_food(call.message, bot, user)
    elif call.data == "[about_us]": user_panel.show_about_us(bot, user)
    elif call.data == "[deleteCategory]": admin.show_yes_no_buttons(bot, user, ['@&', '@*'], "")
    elif call.data == "[renameFoodRu]": admin.change_food_name(call.message, bot, user, "ru")
    elif call.data == "[renameFoodUz]": admin.change_food_name(call.message, bot, user, "uz")
    elif call.data == "[renameFoodEn]": admin.change_food_name(call.message, bot, user, "en")
    elif call.data == "[changeDescriptionRu]": admin.change_food_description(call.message, bot, user, "ru")
    elif call.data == "[changeDescriptionUz]": admin.change_food_description(call.message, bot, user, "uz")
    elif call.data == "[changeDescriptionEn]": admin.change_food_description(call.message, bot, user, "en")
    elif call.data == "[setPreview]": admin.change_preview(call.message, bot, user)
    elif call.data == "[setCost]": admin.change_cost(call.message, bot, user)
    elif call.data == "[deleteFood]": admin.show_yes_no_buttons(bot, user, ['@(', '@)'], "")
    elif call.data == "[addCategoryAdmin]": admin.add_category_panel(call.message, bot, user)
    elif call.data == "[main_panel_admin]": admin.main_panel_admin(bot, user)
    elif call.data == "[basket_view]": user_panel.show_basket_user(bot, user)
    elif call.data == "[price_managment]": admin.show_prices_manager(bot, user)
    elif call.data == "[setCahbackPerOneBuy]": admin.change_cashback_per_buy(call.message, bot, user)
    elif call.data == "[setCahbackPerMonth]": admin.change_cashback_per_month(call.message, bot, user)
    elif call.data == "[setRoadCost]": admin.change_road_price(call.message, bot, user)
    elif call.data == "[get]": user_panel.get_food_count(call.message, bot, user)
    elif call.data == "[set_discount_count]": admin.set_discount_cost(bot, user, call.message)
    elif call.data == "[show_article_info]": 
        locator = Locator.get_locator(user.id)
        user_panel.show_food_info(bot, user, food.get_food(locator["category_uid"], locator["food_uid"]))
    elif call.data == "[clear_basket]": user_panel.action_clear_basket(bot, user)
    elif call.data == "[show_foods_managment]": admin.show_foods_managment(bot, user)
    elif call.data == "[choiseFood]": user_panel.show_select_food(bot, user)
    elif call.data == "[mailer]": admin.show_mailer_panel(bot, user)
    elif call.data == "[send_mailer_just_text]": admin.show_dialog_input_text_ru_just_text(call.message, bot, user)
    elif call.data == "[send_mailer_image]": admin.show_dialog_input_image_ru(call.message, bot, user)
    elif call.data == "[history]": admin.show_history_panel(bot, user)
    elif call.data == "[history_all]": admin.action_history_all(bot, user)
    elif call.data == "[history_date]": admin.show_history_by_date(bot, user)
    elif call.data == "[select_date_from]": admin.show_dialog_set_date_from(call.message, bot, user)
    elif call.data == "[select_date_to]": admin.show_dialog_set_date_to(call.message, bot, user)
    elif call.data == "[get_history]": admin.show_dialog_history_by_date(bot, user)
    elif call.data == "[rename_category_ru]": admin.show_rename_category(call.message, bot, user, "ru")
    elif call.data == "[rename_category_uz]": admin.show_rename_category(call.message, bot, user, "uz")
    elif call.data == "[rename_category_en]": admin.show_rename_category(call.message, bot, user, "en")
    elif call.data == "[users]": admin.show_dialog_user_detail(call.message, bot, user)
    elif call.data == "[add_subcategory]": admin.dialog_add_subcategory(call.message, bot, user)
    elif call.data == "[change_count_cashback]": admin.dialog_set_cashback_count(call.message, bot, user) ###
    elif call.data == "[select_pizza]": menu_pizza.show_pizza_list(bot, user)
    elif call.data == "[add_pizza]": menu_pizza.input_pizza_name(bot, user, call.message)
    elif call.data == "[pizza_set_preview]":  menu_pizza.input_pizza_preview(bot, user, call.message)
    elif call.data == "[show_pizza_detail]": menu_pizza.show_pizza_information(bot, user, Locator.get_food(user.id))
    elif call.data == "[pizza_set_ru_name]": menu_pizza.input_pizza_new_name(bot, user, call.message, "ru")
    elif call.data == "[pizza_set_uz_name]": menu_pizza.input_pizza_new_name(bot, user, call.message, "uz")
    elif call.data == "[pizza_set_en_name]": menu_pizza.input_pizza_new_name(bot, user, call.message, "en")
    elif call.data == "[pizza_set_ru_description]": menu_pizza.input_pizza_new_description(bot, user, call.message, "ru")
    elif call.data == "[pizza_set_uz_description]": menu_pizza.input_pizza_new_description(bot, user, call.message, "uz")
    elif call.data == "[pizza_set_en_description]": menu_pizza.input_pizza_new_description(bot, user, call.message, "en")
    elif call.data == "[pizza_set_small_cost]": menu_pizza.input_pizza_new_cost(bot, user, call.message, "small")
    elif call.data == "[pizza_set_medium_cost]": menu_pizza.input_pizza_new_cost(bot, user, call.message, "medium")
    elif call.data == "[pizza_set_large_cost]": menu_pizza.input_pizza_new_cost(bot, user, call.message, "large")
    elif call.data == "[pizza_delete]": 
        admin.show_yes_no_buttons(bot, user, ['#!', '#@'], "")
    elif call.data == "[select_pizza_user]": menu_pizza.show_pizza_list_user(bot, user)
    elif call.data == "[small]": menu_pizza.show_get(bot, user, "small", call.message)
    elif call.data == "[medium]": menu_pizza.show_get(bot, user, "medium", call.message)
    elif call.data == "[large]": menu_pizza.show_get(bot, user, "large", call.message)
    elif call.data == "[show_pizza_information_user]": menu_pizza.show_pizza_information_user(bot, user, Locator.get_food(user.id))
    elif call.data == "[return_category_user]": 
        Locator.set_subcategory(user.id, '')
        user_panel.show_select_food(bot, user)
    elif call.data == "[return_category]": 
        Locator.set_subcategory(user.id, '')
        admin.show_foods_managment(bot, user)
    else:
        if call.data[0] == '!':
            if call.data[1] == '!': #выбор категории
                category_uid = call.data.replace('!!', '') 
                Locator.set_category(user.id, category_uid)
                user_panel.show_select_food(bot, user)
            elif call.data[1] == '@': #выбор блюда
                food_uid = call.data.replace('!@', '')
                Locator.set_food(user.id, food_uid)
                user_panel.show_food_info(bot, user, food.get_food(Locator.get_category(user.id), food_uid))
            elif call.data[1] == '#': user_panel.change_count_food(call.message, bot, user)
            elif call.data[1] == '$': 
                category_uid = call.data.replace('!$', '') #выбор категории
                Locator.set_category(user.id, category_uid)
                admin.show_foods_managment(bot, user)
            elif call.data[1] == '^': #Детали блюда
                food_uid = call.data.replace('!^', '') #выбор блюда
                Locator.set_food(user.id, food_uid)
                admin.show_food_info_managment(bot, user, Locator.get_category(user.id), food_uid)
            elif call.data[1] == '%': #Отмена, возврат
                call.data = call.data.replace('!%', '')
                bot.clear_step_handler_by_chat_id(chat_id=call.message.chat.id)
                callback_worker(call)
            elif call.data[1] == '&': #Отклонить заявку
                order_uid = call.data.replace('!&', '')
                Order.set_order_status(bot, order_uid, "❌ Заказ отклонен")
                Order.clear_order(order_uid)
            elif call.data[1] == '*': #Принять заявку
                order_uid = call.data.replace('!*', '')
                order = Order.get_data(order_uid)
                us = User.load_user_from_id(order[5])
                if order[2] == "cashback":
                    us.cashback -= order[0]
                else:
                    us.cashback += Utils.get_soum_by_cashback(order[0])
                DBUser.set_cashback(us.id, us.cashback)
                Order.set_order_status(bot, order_uid, "✅ Заказ принят")
                History.add_history(order[4], order[5], order[6], order[0], order[1], order[2], order[3])
                Order.clear_order(order_uid)
            elif call.data[1] == '(': #Принять филиал
                filial = call.data.replace('!(', '')
                Reserved.set_reserved(user.id, 4, config.LOCATION_NAME[filial])
                user_panel.set_payment(bot, user)
            elif call.data[1] == '-': #Минус блюдо:
                uid = call.data.replace("!-", "")
                Garbage_Collector.Clear(bot, user.id)
                count = basket.get_count(user.id, uid)
                if count > 1:
                    count -= 1
                basket.set_new_count(user.id, uid, count)
                user_panel.show_basket_user(bot, user)
            elif call.data[1] == '+': #Плюс блюдо:
                uid = call.data.replace("!+", "")
                Garbage_Collector.Clear(bot, user.id)
                basket.set_new_count(user.id, uid, basket.get_count(user.id, uid)+1)
                user_panel.show_basket_user(bot, user)
            elif call.data[1] == 'd': #Удалить с корзины:
                uid = call.data.replace("!d", "")
                Garbage_Collector.Clear(bot, user.id)
                basket.delete_from_basket(user.id, uid)
                user_panel.show_basket_user(bot, user)
        elif call.data[0] == '@':
            if call.data[1] == '!': #Выбор подкатегории для админа
                Locator.set_subcategory(user.id, call.data.replace('@!', ''))
                admin.show_foods_managment(bot, user)
            elif call.data[1] == '@': #выбор подкатегории для клиента
                Locator.set_subcategory(user.id, call.data.replace('@@', ''))
                user_panel.show_select_food(bot, user)
            elif call.data[1] == '#': #Выбор пиццы:
                pizza = call.data.replace("@#", "")
                Locator.set_food(user.id, pizza)
                menu_pizza.show_pizza_information(bot, user, pizza)
            elif call.data[1] == '$': #Выбор пиццы пользователем
                pizza = call.data.replace("@$", "")
                Locator.set_food(user.id, pizza)
                menu_pizza.show_pizza_information_user(bot, user, pizza)
            elif call.data[1] == '%': #ввод нового кол-во
                Locator.set_food(user.id, call.data.replace("@%", ""))
                user_panel.change_count_food(call.message, bot, user) 
            elif call.data[1] == '^': #Удалить из корзины пиццу
                pizza = call.data.replace("@^", "")
                basket.delete_from_basket(user.id, pizza)
                user_panel.show_basket_user(bot, user)
            elif call.data[1] == '&': admin.action_category(bot, user) #Да, удалить категорию
            elif call.data[1] == '*': admin.show_category_managment(bot, user) #Нет, не удалять категорию
            elif call.data[1] == '(': admin.action_delete_food(bot, user) #Да, удалить блюдл
            elif call.data[1] == ')': #Нет, не удалять блюдо
                locator = Locator.get_locator(user.id)
                admin.show_food_info_managment(bot, user, locator["category_uid"], locator["food_uid"])
        elif call.data[0] == '#':
            if call.data[1] == '!': #Да, удалить пиццу
                DBPizza.delete_pizza(Locator.get_food(user.id))
                menu_pizza.show_pizza_list(bot, user)
            elif call.data[1] == '@': menu_pizza.show_pizza_information(bot, user, Locator.get_food(user.id)) #Нет, не удалять пиццу
            elif call.data[1] == '#': #- блюдл
                Garbage_Collector.Clear(bot, user.id)
                uid = call.data.replace("##", "")
                count = basket.get_count(user.id, uid) - 1
                if count <= 0: count = 1
                basket.set_new_count(user.id, uid, count)
                kbrd = Keyboard.get_keyboard_count(user, uid, count)
                Garbage_Collector.add_garbage_commid(user.id, bot.send_message(user.id, langer[user.lang]["inputCountFood"], reply_markup=kbrd).message_id)                
            elif call.data[1] == '$': # вручную ввести кол-во
                Garbage_Collector.Clear(bot, user.id)
                uid = call.data.replace("#$", "")
                kbrd = Keyboard.get_keyboard_cancel(user, "[get]")
                Garbage_Collector.add_garbage_commid(user.id, bot.send_message(user.id, langer[user.lang]["inputCountFood"], reply_markup=kbrd).message_id)
                bot.register_next_step_handler(call.message, lambda message : user_panel.action_change_count_food(user, bot, message))
            elif call.data[1] == '%': # + блюдл
                Garbage_Collector.Clear(bot, user.id)
                uid = call.data.replace("#%", "")
                count = basket.get_count(user.id, uid) + 1
                basket.set_new_count(user.id, uid, count)
                kbrd = Keyboard.get_keyboard_count(user, uid, count)
                Garbage_Collector.add_garbage_commid(user.id, bot.send_message(user.id, langer[user.lang]["inputCountFood"], reply_markup=kbrd).message_id)
            elif call.data[1] == '^': #отменить
                Garbage_Collector.Clear(bot, user.id)
                uid = call.data.replace("#^", "")
                basket.delete_from_basket(user.id, uid)
                user_panel.choise_category_user(bot, user)
bot.polling(none_stop=True, interval=0)