from telebot import TeleBot
import sqlite3

class Mailer():
    """Класс, для рассылки сообщений"""
    @staticmethod
    def send_message(bot : TeleBot, chat_id : str, message_text : str) -> None:
        """Посылка сообщения"""
        try:
            bot.send_message(chat_id, message_text)
        except:
            return False
    @staticmethod
    def send_image(bot : TeleBot, chat_id : str, img_id : str, title : str) -> None:
        """Посылка изображение сообщение"""
        try:
            bot.send_photo(chat_id, img_id, caption=title)
        except:
            return False
    @staticmethod
    def set_img_name(lang : str, img_name : str) -> None:
        with sqlite3.connect("db/mailer_image.db", check_same_thread=False) as con:
            img_name = img_name.replace('\'', '~')
            con.cursor().execute(f"UPDATE [mailer_image] SET {lang}='{img_name}'")
    @staticmethod
    def set_img_title(lang : str, img_title : str) -> None:
        with sqlite3.connect("db/mailer_image.db", check_same_thread=False) as con:
            img_title = img_title.replace('"', '~')
            img_title = img_title.replace("'", '~')
            con.cursor().execute(f"UPDATE [mailer_image] SET title_{lang}='{img_title}'")
    @staticmethod
    def get_data() -> dict:
        """Получить письмо"""
        with sqlite3.connect("db/mailer_image.db", check_same_thread=False) as con:
            res = con.cursor().execute(f"SELECT * FROM [mailer_image]").fetchone()
            return {
                "img" : {
                    "ru" : res[0].replace('~', "`"),
                    "uz" : res[2].replace('~', "`"),
                    "en" : res[4].replace('~', "`"),
                },
                "description" : {
                    "ru" : res[1].replace('~', "`"),
                    "uz" : res[3].replace('~', "`"),
                    "en" : res[5].replace('~', "`"),
                }
            }