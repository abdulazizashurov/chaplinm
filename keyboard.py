from locator import Locator
from utils import Utils
from user import User
from telebot import types
from configparser import ConfigParser
import config
import food
import basket
import DBPizza

from log import Log

langer = ConfigParser()
langer.read("data/langs.ini", encoding="utf8")
class Keyboard():
    """Класс, для получения различных кнопок"""
    ###АДМИН#####
    @staticmethod
    def get_keyboard_admin_panel(user : User) -> types.InlineKeyboardMarkup:
        global langer
        kbrd = types.InlineKeyboardMarkup()
        kbrd.add(types.InlineKeyboardButton(langer[user.lang]["foodManagment"], callback_data="[foodManagment]"))
        kbrd.add(types.InlineKeyboardButton(langer[user.lang]["price_managment"], callback_data="[price_managment]"))
        kbrd.add(types.InlineKeyboardButton(langer[user.lang]["users"], callback_data="[users]"))
        kbrd.add(types.InlineKeyboardButton(langer[user.lang]["users_detail"], callback_data="[users_detail]"))
        kbrd.add(types.InlineKeyboardButton(langer[user.lang]["user_who_not_buy"], callback_data="[user_who_not_buy]"))
        kbrd.add(types.InlineKeyboardButton(langer[user.lang]["set_discount_count"], callback_data="[set_discount_count]"))
        kbrd.add(types.InlineKeyboardButton(langer[user.lang]["mailer"], callback_data="[mailer]"))
        kbrd.add(types.InlineKeyboardButton(langer[user.lang]["history"], callback_data="[history]"))
        return kbrd
    @staticmethod
    def get_keyboard_admin_user_detail(user : User) -> None:
        """Получение клавиатуры для взаимодествия с пользователем"""
        kbrd = types.InlineKeyboardMarkup()
        kbrd.add(types.InlineKeyboardButton(langer[user.lang]["change_count_cashback"], callback_data="[change_count_cashback]"))
        kbrd.add(types.InlineKeyboardButton(langer[user.lang]["back"], callback_data="[main_panel_admin]"))
        return kbrd           
    @staticmethod
    def get_keyboard_admin_history(user : User) -> None:
        """Клавиатура для истории"""
        kbrd = types.InlineKeyboardMarkup()
        kbrd.add(types.InlineKeyboardButton(langer[user.lang]["history_all"], callback_data="[history_all]"))
        kbrd.add(types.InlineKeyboardButton(langer[user.lang]["history_date"], callback_data="[history_date]"))
        kbrd.add(types.InlineKeyboardButton(langer[user.lang]["back"], callback_data="[main_panel_admin]"))
        return kbrd   
    @staticmethod
    def get_keyboard_admin_history_select_date(user : User) -> None:
        """Клавиатура выбора даты"""
        kbrd = types.InlineKeyboardMarkup()
        kbrd.add(types.InlineKeyboardButton(langer[user.lang]["select_date_from"], callback_data="[select_date_from]"))
        kbrd.add(types.InlineKeyboardButton(langer[user.lang]["select_date_to"], callback_data="[select_date_to]"))
        kbrd.add(types.InlineKeyboardButton(langer[user.lang]["get_history"], callback_data="[get_history]"))
        kbrd.add(types.InlineKeyboardButton(langer[user.lang]["back"], callback_data="[history]"))
        return kbrd           
    @staticmethod
    def get_keyboard_admin_mailer(user : User) -> None:
        """Клавиатура для поссылки сообщения"""
        kbrd = types.InlineKeyboardMarkup()
        kbrd.add(types.InlineKeyboardButton(langer[user.lang]["send_mailer_just_text"], callback_data="[send_mailer_just_text]"))
        kbrd.add(types.InlineKeyboardButton(langer[user.lang]["send_mailer_image"], callback_data="[send_mailer_image]"))
        kbrd.add(types.InlineKeyboardButton(langer[user.lang]["back"], callback_data="[main_panel_admin]"))
        return kbrd        
    @staticmethod
    def get_keyboard_admin_price_managment(user : User) -> types.InlineKeyboardMarkup:
        kbrd = types.InlineKeyboardMarkup()
        kbrd.add(types.InlineKeyboardButton(langer[user.lang]["setCahbackPerOneBuy"], callback_data="[setCahbackPerOneBuy]"))
        kbrd.add(types.InlineKeyboardButton(langer[user.lang]["setCahbackPerMonth"], callback_data="[setCahbackPerMonth]"))
        kbrd.add(types.InlineKeyboardButton(langer[user.lang]["setRoadCost"], callback_data="[setRoadCost]"))
        kbrd.add(types.InlineKeyboardButton(langer[user.lang]["back"], callback_data="[main_panel_admin]"))
        return kbrd
    @staticmethod
    def get_keyboard_admin_category_panel(user : User) -> types.InlineKeyboardMarkup:
        global langer
        kbrd = types.InlineKeyboardMarkup()
        pizza = {
            "ru" : "🍕 Пицца",
            "uz" : "🍕 Пицца",
            "en" : "🍕 Pizza",
        }
        kbrd.add(types.InlineKeyboardButton(f"{pizza[user.lang]}", callback_data=f"[select_pizza]"))        
        for cfood in food.food_get_categories():
            kbrd.add(types.InlineKeyboardButton(cfood[user.lang], callback_data=f"!${cfood['uid']}"))
        kbrd.add(types.InlineKeyboardButton(langer[user.lang]["addCategoryAdmin"], callback_data="[addCategoryAdmin]"))
        kbrd.add(types.InlineKeyboardButton(langer[user.lang]["back"], callback_data="[main_panel_admin]"))
        return kbrd
    @staticmethod
    def get_keyboard_chanel(order_uid : str) -> types.InlineKeyboardButton:
        """Клавиатура, посылаемая на канал"""
        kbrd = types.InlineKeyboardMarkup()
        kbrd.add(types.InlineKeyboardButton("Отклонить", callback_data=f"!&{order_uid}"),
            types.InlineKeyboardButton("Принять", callback_data=f"!*{order_uid}"))
        return kbrd
    ###КЛИЕНТЫ###
    @staticmethod
    def get_keyboard_fillial_location(user : User) -> types.InlineKeyboardMarkup:
        """Получение клавиатуры локации"""
        kbrd = types.InlineKeyboardMarkup()
        for loc in config.LOCATION_NAME:
            kbrd.add(types.InlineKeyboardButton(config.LOCATION_NAME[loc], callback_data=f"!(1"))
        kbrd.add(types.InlineKeyboardButton(langer[user.lang]["back"], callback_data="[pay]"))      
        return kbrd
    @staticmethod
    def get_keyboard_select_language_begin_register() -> types.InlineKeyboardMarkup:
        kbrd = types.InlineKeyboardMarkup()
        for lang in config.LANGS:
            kbrd.add(types.InlineKeyboardButton(lang["text"], callback_data=f"[selected_lang_beg_reg]{lang['value']}"))
        return kbrd
    @staticmethod
    def get_keyboard_cancel(user : User, return_to : str) -> types.InlineKeyboardMarkup:
        """Кнопка отмены"""
        kbrd = types.InlineKeyboardMarkup()
        kbrd.add(types.InlineKeyboardButton(langer[user.lang]["cancel"], callback_data=f"!%{return_to}"))
        return kbrd        
    @staticmethod
    def get_keyboard_select_language() -> types.InlineKeyboardMarkup:
        kbrd = types.InlineKeyboardMarkup()
        for lang in config.LANGS:
            kbrd.add(types.InlineKeyboardButton(lang["text"], callback_data=f"[selected_lang]{lang['value']}"))
        return kbrd
    @staticmethod
    def get_keyboard_user_panel(user : User) -> types.InlineKeyboardMarkup:
        global langer
        kbrd = types.InlineKeyboardMarkup()
        kbrd.add(types.InlineKeyboardButton(langer[user.lang]["back"], callback_data="[back]"))
        return kbrd
    @staticmethod
    def get_keyboard_user_menu(lang : str) -> types.InlineKeyboardMarkup:
        """Пользовательское меню"""
        global langer
        kbrd = types.InlineKeyboardMarkup()
        kbrd.add(types.InlineKeyboardButton(langer[lang]["order"], callback_data="[order]"))
        kbrd.add(types.InlineKeyboardButton(langer[lang]["aboutus"], callback_data="[about_us]"))
        kbrd.add(types.InlineKeyboardButton(langer[lang]["settings"], callback_data="[settings]"))
        return kbrd
    @staticmethod
    def get_keyboard_user_settings(lang : str) -> types.InlineKeyboardMarkup:
        global langer
        kbrd = types.InlineKeyboardMarkup()
        kbrd.add(types.InlineKeyboardButton(langer[lang]["setName"], callback_data="[setName]"))
        kbrd.add(types.InlineKeyboardButton(langer[lang]["changeLanguage"], callback_data="[change_language]"))
        kbrd.add(types.InlineKeyboardButton(langer[lang]["setPhoneNumber"], callback_data="[setPhoneNumber]"))
        kbrd.add(types.InlineKeyboardButton(langer[lang]["back"], callback_data="[back]"))
        return kbrd
    @staticmethod
    def get_keyboard_show_food_list(user : User) -> types.InlineKeyboardMarkup:
        global langer
        kbrd = types.InlineKeyboardMarkup()
        existing = basket.get_foods_uid(user.id)
        locator = Locator.get_locator(user.id)
        btn = []
        z = 0
        if locator['subcategory_uid'] == '':
            for article in food.food_get_subcategory(locator['category_uid']):
                if article['uid'] not in existing:
                    if z == 1:
                        btn.append(types.InlineKeyboardButton(f"{article[user.lang]}", callback_data=f"@@{article['uid']}"))
                        kbrd.add(btn[0], btn[1])
                        btn = []
                        z = 0
                    else:
                        btn.append(types.InlineKeyboardButton(f"{article[user.lang]}", callback_data=f"@@{article['uid']}"))
                        z += 1
                del existing[Utils.get_index(existing, article['uid'])]
        for cfood in food.food_get_foods(locator["category_uid"], locator["subcategory_uid"]):
            if cfood['uid'] not in existing:
                if z == 1:
                    btn.append(types.InlineKeyboardButton(cfood[user.lang], callback_data=f"!@{cfood['uid']}"))
                    kbrd.add(btn[0], btn[1])
                    btn = []
                    z = 0
                else:
                    btn.append(types.InlineKeyboardButton(cfood[user.lang], callback_data=f"!@{cfood['uid']}"))
                    z += 1
            else: del existing[Utils.get_index(existing, cfood['uid'])]
        if z == 1 and len(btn) > 0:
            kbrd.add(btn[0])
        kbrd.add(types.InlineKeyboardButton(langer[user.lang]["set_comment"], callback_data="[set_comment]"))
        kbrd.add(types.InlineKeyboardButton(langer[user.lang]["pay"], callback_data="[pay]"))
        kbrd.add(types.InlineKeyboardButton(langer[user.lang]["basket_view"], callback_data="[basket_view]"))
        back = "[choiseCategory]" if locator['subcategory_uid'] == '' else "[return_category_user]"
        kbrd.add(types.InlineKeyboardButton(langer[user.lang]["back"], callback_data=back))
        return kbrd      
    @staticmethod
    def get_keyboard_admin_food_info_managment(user : User, category_uid : str, food_uid : str) -> None:
        """Изменение информации об продукте"""
        global langer
        kbrd = types.InlineKeyboardMarkup()

        kbrd.add(types.InlineKeyboardButton(langer[user.lang]["renameFoodRu"], callback_data="[renameFoodRu]"))
        kbrd.add(types.InlineKeyboardButton(langer[user.lang]["renameFoodUz"], callback_data="[renameFoodUz]"))
        kbrd.add(types.InlineKeyboardButton(langer[user.lang]["renameFoodEn"], callback_data="[renameFoodEn]"))
        kbrd.add(types.InlineKeyboardButton(langer[user.lang]["changeDescriptionRu"], callback_data="[changeDescriptionRu]"))
        kbrd.add(types.InlineKeyboardButton(langer[user.lang]["changeDescriptionUz"], callback_data="[changeDescriptionUz]"))
        kbrd.add(types.InlineKeyboardButton(langer[user.lang]["changeDescriptionEn"], callback_data="[changeDescriptionEn]"))
        kbrd.add(types.InlineKeyboardButton(langer[user.lang]["setPreview"], callback_data="[setPreview]"))
        kbrd.add(types.InlineKeyboardButton(langer[user.lang]["setCost"], callback_data="[setCost]"))
        kbrd.add(types.InlineKeyboardButton(langer[user.lang]["deleteFood"], callback_data="[deleteFood]"))
        kbrd.add(types.InlineKeyboardButton(langer[user.lang]["back"], callback_data="[show_foods_managment]"))
        return kbrd        
    @staticmethod
    def get_keyboard_admin_food_mangment(user : User) -> types.InlineKeyboardMarkup:
        global langer
        kbrd = types.InlineKeyboardMarkup()
        locator = Locator.get_locator(user.id)
        if locator['subcategory_uid'] == '':
            for article in food.food_get_subcategory(locator['category_uid']):
                kbrd.add(types.InlineKeyboardButton(f"{article[user.lang]}", callback_data=f"@!{article['uid']}"))
        for article in food.food_get_foods(locator['category_uid'], locator['subcategory_uid']):
            kbrd.add(types.InlineKeyboardButton(f"{article[user.lang]}", callback_data=f"!^{article['uid']}"))
        kbrd.add(types.InlineKeyboardButton(langer[user.lang]["addFood"], callback_data="[addFood]"))
        if locator['subcategory_uid'] == '':
            kbrd.add(types.InlineKeyboardButton(langer[user.lang]["add_subcategory"], callback_data="[add_subcategory]"))
        kbrd.add(types.InlineKeyboardButton(langer[user.lang]["rename_category_ru"], callback_data="[rename_category_ru]"))
        kbrd.add(types.InlineKeyboardButton(langer[user.lang]["rename_category_uz"], callback_data="[rename_category_uz]"))
        kbrd.add(types.InlineKeyboardButton(langer[user.lang]["rename_category_en"], callback_data="[rename_category_en]"))
        kbrd.add(types.InlineKeyboardButton(langer[user.lang]["deleteCategory"], callback_data="[deleteCategory]"))
        back = "[foodManagment]" if locator['subcategory_uid'] == '' else "[return_category]" #TODO this
        kbrd.add(types.InlineKeyboardButton(langer[user.lang]["back"], callback_data=back))
        return kbrd
    @staticmethod
    def get_keyboard_admin_food_mangment_in_subcategory(user : User) -> types.InlineKeyboardMarkup:
        locator = Locator.get_locator(user.id)
        kbrd = types.InlineKeyboardMarkup()
        for article in food.food_get_foods(locator['category_uid'], locator['subcategory_uid']):
            kbrd.add(types.InlineKeyboardButton(f"{article[user.lang]}", callback_data=f"!^{article['uid']}"))
        kbrd.add(types.InlineKeyboardButton(langer[user.lang]["addFood"], callback_data="[addFood]"))
        kbrd.add(types.InlineKeyboardButton(langer[user.lang]["rename_category_ru"], callback_data="[rename_category_ru]"))
        kbrd.add(types.InlineKeyboardButton(langer[user.lang]["rename_category_uz"], callback_data="[rename_category_uz]"))
        kbrd.add(types.InlineKeyboardButton(langer[user.lang]["rename_category_en"], callback_data="[rename_category_en]"))
        kbrd.add(types.InlineKeyboardButton(langer[user.lang]["deleteCategory"], callback_data="[deletesubCategory]"))
        kbrd.add(types.InlineKeyboardButton(langer[user.lang]["back"], callback_data="[foodsubManagment]"))
        return kbrd       
    @staticmethod
    def get_keyboard_yes_no(cmd : str, data : str, user : User) -> types.InlineKeyboardMarkup:
        kbrd = types.InlineKeyboardMarkup(row_width=2)
        kbrd.add(types.InlineKeyboardButton(langer[user.lang]["yes"], callback_data=f"{cmd[0]}{data}"),
                types.InlineKeyboardButton(langer[user.lang]["no"], callback_data=f"{cmd[1]}{data}"))
        return kbrd
    @staticmethod
    def get_keyboard_show_user_basket(user : User) -> types.InlineKeyboardMarkup:
        """Корзина клиента"""
        global langer
        kbrd = types.InlineKeyboardMarkup(row_width=3)
        cmd = ""
        del_cmd = ""
        articles = basket.get_foods_in_basket(user.id)
        for article in articles:
            if article['category_uid'] == "pizza":
                name = DBPizza.get_name(article['food_uid'])[user.lang]
                cmd = "@%"
                del_cmd = "@^"
            else:
                name = food.get_name(article['food_uid'])[user.lang]
                cmd = "!#"
                del_cmd = '!d'
            kbrd.add(
                types.InlineKeyboardButton("➖", callback_data=f"!-{article['food_uid']}"),
                types.InlineKeyboardButton(f"{name}: {article['count']}шт.", callback_data=f"{cmd}{article['food_uid']}"),
                types.InlineKeyboardButton("➕", callback_data=f"!+{article['food_uid']}"))
            kbrd.add(types.InlineKeyboardButton(f"❌ {name}", callback_data=f"{del_cmd}{article['food_uid']}"))
        if len(articles) > 0:
            kbrd.add(types.InlineKeyboardButton(langer[user.lang]["clearBasket"], callback_data="[clear_basket]"))
            kbrd.add(types.InlineKeyboardButton(langer[user.lang]["set_comment"], callback_data="[set_comment]"))
            kbrd.add(types.InlineKeyboardButton(langer[user.lang]["pay"], callback_data="[pay]"))
        kbrd.add(types.InlineKeyboardButton(langer[user.lang]["back"], callback_data="[order]"))
        return kbrd
    @staticmethod
    def get_keyboard_food_cart(user : User) -> types.InlineKeyboardMarkup:
        """Карта товара"""
        global langer
        kbrd = types.InlineKeyboardMarkup()
        kbrd.add(types.InlineKeyboardButton(langer[user.lang]["get"], callback_data="[get]"))
        kbrd.add(types.InlineKeyboardButton(langer[user.lang]["basket_view"], callback_data="[basket_view]"))
        kbrd.add(types.InlineKeyboardButton(langer[user.lang]["back"], callback_data="[choiseFood]"),
            types.InlineKeyboardButton(langer[user.lang]["pay"], callback_data="[pay]"))
        return kbrd
    @staticmethod
    def get_keyboard_count(user : User, food_uid : str, food_count : str) -> types.InlineKeyboardMarkup:
        """Получение количества блюда"""
        kbrd = types.InlineKeyboardMarkup(row_width=3)
        kbrd.add(types.InlineKeyboardButton("➖", callback_data=f"##{food_uid}"),
            types.InlineKeyboardButton(f"{food_count}", callback_data=f"#${food_uid}"),
            types.InlineKeyboardButton("➕", callback_data=f"#%{food_uid}"))
        kbrd.add(types.InlineKeyboardButton(langer[user.lang]["cancel"], callback_data=f"#^{food_uid}"),
            types.InlineKeyboardButton(langer[user.lang]["agree"], callback_data=f"[choiseCategory]"))
        return kbrd
    @staticmethod
    def get_keyboard_food_categories(user : User) -> types.InlineKeyboardMarkup:
        """Получить кнопки выбора категории"""
        global langer
        kbrd = types.InlineKeyboardMarkup(row_width=2)
        pizza = {
            "ru" : "🍕 Пицца",
            "uz" : "🍕 Пицца",
            "en" : "🍕 Pizza",
        }
        btn = []
        btn.append(types.InlineKeyboardButton(f"{pizza[user.lang]}", callback_data=f"[select_pizza_user]"))
        for cfood in food.food_get_categories():
            btn.append(types.InlineKeyboardButton(cfood[user.lang], callback_data=f"!!{cfood['uid']}"))
        kbrd.add(*btn)
        kbrd.add(types.InlineKeyboardButton(langer[user.lang]["set_comment"], callback_data="[set_comment]"))
        kbrd.add(types.InlineKeyboardButton(langer[user.lang]["pay"], callback_data="[pay]"))
        kbrd.add(types.InlineKeyboardButton(langer[user.lang]["basket_view"], callback_data="[basket_view]"))
        #kbrd.add(types.InlineKeyboardButton(langer[user.lang]["back"], callback_data="[order]"))
        kbrd.add(types.InlineKeyboardButton(langer[user.lang]["back"], callback_data="[back]"))
        return kbrd
    @staticmethod
    def get_keyboard_order_manager(user : User) -> types.InlineKeyboardMarkup:
        """Кнопки управления заказом"""
        global langer
        kbrd = types.InlineKeyboardMarkup()
        kbrd.add(types.InlineKeyboardButton(langer[user.lang]["choiseCategory"], callback_data="[choiseCategory]"))
        kbrd.add(types.InlineKeyboardButton(langer[user.lang]["basket_view"], callback_data="[basket_view]"))
        kbrd.add(types.InlineKeyboardButton(langer[user.lang]["set_comment"], callback_data="[set_comment]"))
        kbrd.add(types.InlineKeyboardButton(langer[user.lang]["pay"], callback_data="[pay]"))
        kbrd.add(types.InlineKeyboardButton(langer[user.lang]["back"], callback_data="[back]"))
        return kbrd
    @staticmethod
    def get_keyboard_choise_dilivery(user : User) -> types.InlineKeyboardMarkup:
        """Кнопки выбора доставки"""
        global langer
        kbrd = types.InlineKeyboardMarkup()
        kbrd.add(types.InlineKeyboardButton(langer[user.lang]["dilivery"], callback_data="[dilivery]"))
        kbrd.add(types.InlineKeyboardButton(langer[user.lang]["self_dilivery"], callback_data="[self_dilivery]"))
        kbrd.add(types.InlineKeyboardButton(langer[user.lang]["back"], callback_data="[order]"))
        return kbrd
    @staticmethod
    def get_keyboard_choise_payment(user : User) -> types.InlineKeyboardMarkup:
        """Кнопки выбора доставки"""
        global langer
        kbrd = types.InlineKeyboardMarkup()
        kbrd.add(types.InlineKeyboardButton(langer[user.lang]["money"], callback_data="[money]"))
        kbrd.add(types.InlineKeyboardButton("Click", callback_data="[click]"))
        #kbrd.add(types.InlineKeyboardButton("Payme", callback_data="[payme]"))
        kbrd.add(types.InlineKeyboardButton(langer[user.lang]["pay_to_cashback"], callback_data="[cashback]"))
        kbrd.add(types.InlineKeyboardButton(langer[user.lang]["back"], callback_data="[pay]"))
        return kbrd
    @staticmethod
    def get_keyboard_final_order_check(user : User) -> types.InlineKeyboardMarkup:
        """Кнопки завершения покупки"""
        kbrd = types.InlineKeyboardMarkup()
        kbrd.add(types.InlineKeyboardButton(langer[user.lang]["finish"], callback_data="[finish]"))
        kbrd.add(types.InlineKeyboardButton(langer[user.lang]["cancel"], callback_data="[order]"))
        return kbrd