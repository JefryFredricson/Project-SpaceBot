# NASA project
import requests

class NASA_pic:
    def __init__(self, date):  # <-- Добавлен параметр даты
        self.appid = "ieF88kdVvaGmzuMt0aLBCN6kVZ2J0ZVystXhgBrt"
        self.url = f"https://api.nasa.gov/planetary/apod?api_key={self.appid}&date={date}"  # <-- Используем переданную дату
        
        # Выполнение запроса и обработка данных
        self.response = requests.get(self.url)
        self.posts = self.response.json()
        # print(self.posts)

        # Проверка статуса ответа
        if self.response.status_code == 200:
            self._process_success_response()
        else:
            print(f"Error {self.response.status_code}")
    
    def _process_success_response(self):
        """Обработка успешного ответа от сервера"""
        self.date = self.posts["date"]  # <-- Раскомментирована строка
        self.expl = self.posts["explanation"]
        self.title = self.posts["title"]
        self.pic1 = self.posts["hdurl"]
        self.pic2 = self.posts["url"]

        # Вывод информации
        self._print_results()
    
    def _print_results(self):
        """Форматированный вывод результатов"""
        print("\nAstronomy Picture of the Day (APOD) from NASA website\n")
        print(f"Title: {self.title}\n")
        print(f"Date: {self.date}\n")  # <-- Теперь используется корректная дата
        print(f"Explanation:\n\t{self.expl}\n")

# Создание экземпляра класса для выполнения кода
if __name__ == "__main__":
    date_input = input("Введите дату в формате YYYY-MM-DD: ")  # <-- Простой ввод даты
    nasa = NASA_pic(date_input)  # <-- Передаем дату в конструктор