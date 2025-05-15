from dataclasses import dataclass
import os
import csv
from telebot.types import User as TeleUser



@dataclass
class User:
    
    def __init__(self, data:dict):
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
        return f"{self.id} {self.name} ({self.subscription})"

class Users:
    filename: str
    def __init__(self, filename):
        self.filename = os.path.join(os.path.dirname(__file__), filename)
            
    def addUser(self, user:TeleUser) -> User:
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
    def delUser(self, user:TeleUser) -> User:
        pass

    def getUser(self, id:int) -> User:
        with open(self.filename, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if int(row['ID']) == id:
                    print(row)
                    return User(row)
        return None
    
    def isUser(self, id:int) -> bool:
        with open(self.filename, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if int(row['ID']) == id:
                    return True
        return False

if __name__ == "__main__":
    users = Users('users.csv')
    print(users.getUser(2))