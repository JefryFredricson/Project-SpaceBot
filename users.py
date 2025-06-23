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
    
    def getUser(self, id:int) -> User:
        with open(self.filename, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if int(row['ID']) == id:
                    print(row)
                    return User(row)
        return None

    def getStatus(self, id:int) -> User:
        with open(self.filename, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if int(row['ID']) == id:
                    if int(row['SUBSCRIPTION']) == True:
                        return True
                else:
                    return False
        return None
    
    def isUser(self, id:int) -> bool:
        with open(self.filename, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if int(row['ID']) == id:
                    return True
        return False

    def getUsers(self) -> list[int]:
        ids = []
        with open(self.filename, 'r', encoding='utf-8', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row.get('SUBSCRIPTION', '').strip().lower() == 'true':
                    ids.append(int(row['ID']))
        return ids

    def delUser(self, user_id: int) -> bool:
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

    def returnUser(self, user_id: int) -> bool:
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
    print(users.getUser(2))