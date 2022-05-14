import sqlite3

class Reserved():
    """Класс по работе с временными данными"""
    @staticmethod
    def set_reserved(user_id : str, col_id : str, val : str) -> None:
        """Устанавливаем временную информацию"""
        with sqlite3.connect("db/reserved.db", check_same_thread=False) as con:
            cur = con.cursor()
            if isinstance(val, str) :
                val = val.replace("'", '`')
                val = val.replace('"', '`')
            if cur.execute(f"SELECT user_id FROM [reserved] WHERE user_id='{user_id}'").fetchone() == None:
                count_rows = 6
                text = ""
                for i in range(count_rows):                    
                    text += f"'{val}'" if i == col_id else "''"
                    text += ', ' if i < (count_rows-1) else ''
                cur.execute(f"INSERT INTO [reserved] VALUES('{user_id}', {text})")
            else:
                cur.execute(f"UPDATE [reserved] SET col_{col_id}='{val}' WHERE user_id='{user_id}'")
    def get_reserved(user_id : str, col_id : str) -> str:
        """Получить значение ресерведа"""
        with sqlite3.connect("db/reserved.db", check_same_thread=False) as con:
            return con.execute(f"SELECT col_{col_id} FROM [reserved] WHERE user_id='{user_id}'").fetchone()[0]
    def delete_reserver(user_id : str) -> None:
        """Удалить ресервед пользователя"""
        with sqlite3.connect("db/reserved.db", check_same_thread=False) as con:
            con.execute(f"DELETE FROM [reserved] WHERE user_id='{user_id}'")
