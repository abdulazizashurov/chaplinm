from datetime import datetime
import os

class Log():
    file = ""
    f = None
    def __init__(self, file) -> None:
        self.file = file
        if os.path.exists("log") == False:
            os.mkdir("log")
        self.f = open(f"log/{file}", "at", encoding="utf8")
    def paste_separator(self) -> None:
        """Записывает разделитель в файл"""
        self.f.write("-------------------\n")
        self.commit()
    def paste_data(self, data) -> None:
        """Записывает информацию"""
        self.f.write(f"{datetime.now()}: {data}\n")
        self.commit()
    def paste_datas(self, datas) -> None:
        """Записывает информации"""
        self.f.write(f"{datetime.now()}:\n")
        for data in datas:
            self.f.write(f"\t{data}\n")
        self.commit()
    def commit(self) -> None:
        """Применить запись"""
        self.f.flush()