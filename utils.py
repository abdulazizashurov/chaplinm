from datetime import datetime
from price_manager import PriceManager
from geopy import distance
from telebot import types
class Utils():
    @staticmethod
    def get_date() -> str:
        """Получает дату в виде Американской системы"""
        month = f"0{datetime.now().month}" if datetime.now().month < 10 else f"{datetime.now().month}"
        day = f"0{datetime.now().day}" if datetime.now().day < 10 else f"{datetime.now().day}"
        return f"{datetime.now().year}-{month}-{day}"
    @staticmethod
    def get_index(arr : list, data : str) -> int:
        """Возвращает индекс из коллекции"""
        for i in range(len(arr)):
            if arr[i] == data: return i
        return -1
    @staticmethod
    def rec_three(num):
        return True if int(num) % 3 == 0 else False
    @staticmethod
    def to_razr(num):
        num = int(num)
        tmp = str(num)
        i = len(tmp)-1
        t = len(tmp)
        source = ""
        while i >= 0:
            source += tmp[i]       
            if Utils.rec_three(t - (i)) == True and i != 0:
                source += " "
            i-=1
        res = ""
        i = len(str(source))-1
        while i >= 0:
            res += source[i]
            i-=1
        return res
    @staticmethod
    def from_razr(text):
        return int(text.replace(" ", ""))
    @staticmethod
    def is_valid_number(number : str) -> bool:
        """Проверка на валидность номера телефона"""
        return number.isdigit() and int(number) > 998000000000 and len(number) == 12
    @staticmethod
    def get_number(number : str) -> str:
        """Удаляет лишние символы в номере телефона"""
        return number.replace(' ', '').replace('+', '').replace('(','').replace(')','').replace('-','')
    @staticmethod
    def calc_killometers(location_from, location_to : tuple) -> float:
        """Вычитывает километры между двумя локациями"""
        return distance.distance(location_from, location_to).kilometers
    @staticmethod
    def is_float(data : float) -> bool:
        """Проверка, является ли data float'ом"""
        try:
            float(data)
            return True
        except:
            return False
    @staticmethod
    def is_valid_date(str : str) -> bool:
        """Проверяет, строка правильная дата ли"""
        if str.count("-") == 2:
            nums = str.split("-")
            if nums[0].isdigit() and nums[1].isdigit() and nums[2].isdigit():
                year  = int(nums[0])
                month = int(nums[1])
                day   = int(nums[2])
                if year > 2020:
                    if month > 0 and month < 13:
                        if day > 0 and day <= 31:    
                            return True
        return False
    @staticmethod
    def get_soum_by_cashback(soum : int) -> float:
        cashback = PriceManager.get_cashback_per_buy()
        return float(soum) / 100.0 * cashback