import os
import csv

from telebot.types import User as TeleUser
from dataclasses import dataclass


@dataclass
class User:
    """
    Представляет пользователя.

    Атрибуты:
        id (int): Идентификатор пользователя.
        name (str): Имя пользователя.
        username (str): Никнейм пользователя в Telegram.
        subscription (bool): Статус подписки.
    """
    def __init__(self, data:dict):
        """
        Инициализирует пользователя из словаря.

        Args:
            data (dict): Словарь с ключами 'ID', 'NAME', 'USERNAME', 'SUBSCRIPTION'.

        Raises:
            ValueError: Если data равен None.
        """
        if data is None:
            raise ValueError("Data cannot be None")
        if 'ID' in data:
            self.id = int(data['ID'])
        if 'NAME' in data:
            self.name = data['NAME']
        if 'USERNAME' in data:
            self.username = data['USERNAME']
        if 'SUBSCRIPTION' in data:
            self.subscription = bool(data['SUBSCRIPTION'])
    id: int
    name: str
    username: str
    subscription: bool

    def __str__(self):
        """
        Возвращает строковое представление пользователя.

        Returns:
            str: Строка вида '<id> <name> (<subscription>)'.
        """
        return f"{self.id} {self.name} ({self.subscription})"

class Users:
    """
    Управление списком пользователей, хранящихся в CSV-файле.
    """
    filename: str
    def __init__(self, filename):
        """
        Инициализирует менеджер пользователей.

        Args:
            filename (str): Относительный путь к CSV-файлу.
        """
        self.filename = os.path.join(os.path.dirname(__file__), filename)
            
    def add_user(self, user:TeleUser) -> User:
        """
        Добавляет нового пользователя в CSV-файл.

        Args:
            user (TeleUser): Объект Telegram пользователя.

        Returns:
            User: Объект созданного пользователя.
        """
        with open(self.filename, 'a', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=['ID', 'NAME', 'USERNAME', 'SUBSCRIPTION'])
            writer.writerow({
                'ID': user.id,
                'NAME': user.first_name,
                'USERNAME': user.username,
                'SUBSCRIPTION': True
            })
        return User({
            'ID': user.id,
            'NAME': user.first_name,
            'USERNAME': user.username,
            'SUBSCRIPTION': True
        })
    
    def get_user(self, id:int) -> User:
        """
        Возвращает пользователя по его ID.

        Args:
            user_id (int): Идентификатор пользователя.

        Returns:
            Optional[User]: Объект пользователя или None, если не найден.
        """
        with open(self.filename, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if int(row['ID']) == id:
                    print(row)
                    return User(row)
        return None

    def get_status(self, id:int) -> User:
        """
        Проверяет статус подписки пользователя.

        Args:
            user_id (int): Идентификатор пользователя.

        Returns:
            bool: True, если подписан, иначе False.
        """
        with open(self.filename, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if int(row['ID']) == id:
                    if int(row['SUBSCRIPTION']) == True:
                        return True
                else:
                    return False
        return None
    
    def is_user(self, id:int) -> bool:
        """
        Проверяет, существует ли пользователь с данным ID.

        Args:
            user_id (int): Идентификатор пользователя.

        Returns:
            bool: True, если пользователь найден, иначе False.
        """
        with open(self.filename, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if int(row['ID']) == id:
                    return True
        return False

    def get_users(self) -> list[int]:
        """
        Возвращает список ID всех подписанных пользователей.

        Returns:
            List[int]: Список ID подписанных пользователей.
        """
        ids = []
        with open(self.filename, 'r', encoding='utf-8', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row.get('SUBSCRIPTION', '').strip().lower() == 'true':
                    ids.append(int(row['ID']))
        return ids

    def del_user(self, user_id: int) -> bool:
        """
        Отписывает пользователя, меняя статус SUBSCRIPTION на False.

        Args:
            user_id (int): Идентификатор пользователя.

        Returns:
            bool: True, если изменение было выполнено, иначе False.
        """
        updated = False
        rows = []
        with open(self.filename, 'r', encoding='utf-8', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if int(row['ID']) == user_id and row['SUBSCRIPTION']:
                    row['SUBSCRIPTION'] = False
                    updated = True
                    print(row)
                rows.append(row)

        if updated:
            with open(self.filename, 'w', encoding='utf-8', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=['ID', 'NAME', 'USERNAME', 'SUBSCRIPTION'])
                writer.writeheader()
                writer.writerows(rows)
        return updated

    def return_user(self, user_id: int) -> bool:
        """
        Восстанавливает подписку пользователя, ставя SUBSCRIPTION в True.

        Args:
            user_id (int): Идентификатор пользователя.

        Returns:
            bool: True, если подписка была восстановлена, иначе False.
        """
        updated = False
        rows = []
        with open(self.filename, 'r', encoding='utf-8', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if int(row['ID']) == user_id and row['SUBSCRIPTION'] != True:
                    row['SUBSCRIPTION'] = True
                    updated = True
                rows.append(row)

        if updated:
            with open(self.filename, 'w', encoding='utf-8', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=['ID', 'NAME', 'USERNAME', 'SUBSCRIPTION'])
                writer.writeheader()
                writer.writerows(rows)
        return updated


if __name__ == "__main__":
    users = Users('users.csv')
    print(users.get_user(2))
