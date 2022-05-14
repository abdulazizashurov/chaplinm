import sqlite3

class PriceManager():
    @staticmethod
    def set_cashback_per_buy(percent : float) -> None:
        """Установить кешбек за покупку"""
        with sqlite3.connect("db/admin.db", check_same_thread=False) as con:
            con.cursor().execute(f"UPDATE [prices] SET cashback='{percent}'")
    @staticmethod
    def get_cashback_per_buy() -> float:
        """Получить текущий кешбек за покупку"""
        with sqlite3.connect("db/admin.db", check_same_thread=False) as con:
            return con.cursor().execute(f"SELECT cashback FROM [prices]").fetchone()[0]
    @staticmethod
    def set_cashback_per_month(percent : float) -> None:
        """Установить кешбек за месяц"""
        with sqlite3.connect("db/admin.db", check_same_thread=False) as con:
            con.cursor().execute(f"UPDATE [prices] SET cashback_month='{percent}'")
    @staticmethod
    def get_cashback_per_month() -> float:
        """Получить текущий кешбек за месяц"""
        with sqlite3.connect("db/admin.db", check_same_thread=False) as con:
            return con.cursor().execute(f"SELECT cashback_month FROM [prices]").fetchone()[0]
    @staticmethod
    def set_road(percent : float) -> None:
        """Установить кешбек за месяц"""
        with sqlite3.connect("db/admin.db", check_same_thread=False) as con:
            con.cursor().execute(f"UPDATE [prices] SET road='{percent}'")
    @staticmethod
    def get_road() -> float:
        """Получить текущий кешбек за месяц"""
        with sqlite3.connect("db/admin.db", check_same_thread=False) as con:
            return con.cursor().execute(f"SELECT road FROM [prices]").fetchone()[0]