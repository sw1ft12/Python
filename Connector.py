import requests
from bs4 import BeautifulSoup

from app import User, check_password_hash


class Conntector:
    def __init__(self, adress, port):
        self.url = f"{adress}:{port}"
        self.isAuthenticated = False
        self.session = requests.session()

    def createAd(self, title, text):
        if self.isAuthenticated:
            data = {
                'title': title,
                'text': text
            }
            self.session.post(f"{self.url}/create-ad", data=data)
        else:
            print('Не авторизован')

    def deleteAd(self, id):
        if self.isAuthenticated:
            self.session.post(f"{self.url}/ads/{id}/delete")
        else:
            print("Не авторизован")

    def showAds(self):
        res = requests.get(f"{self.url}/ads").text
        soup = BeautifulSoup(res, 'lxml')
        blockTitle = soup.find_all('div', id='title')
        blockDate = soup.find_all('div', id='date')
        print('Название', ' ', 'Дата публикации')
        for i, j in zip(blockTitle, blockDate):
            print(i.find("h2").get_text(), ' ', j.find("b").get_text(), end='\n')

    def login(self, username, password):
        if self.isAuthenticated:
            print("Уже авторизован")
            return
        data = {
            'username': username,
            'password': password
        }
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            self.session.post(f"{self.url}/login", data=data)
            self.isAuthenticated = True
        else:
            print("Пользователь не найден")

    def register(self, username, password, password2):
        data = {
            'username': username,
            'password': password,
            'password2': password2
        }
        requests.post(f"{self.url}/register", data=data)

    def logout(self):
        if self.isAuthenticated:
            self.session.get(f"{self.url}/logout")
            self.isAuthenticated = False
        else:
            print('Не авторизован')


con = Conntector("http://localhost", 5000)
while True:
    command = input()
    if command == 'login':
        print('Введите имя пользователя')
        username = input()
        print('Введите пароль')
        password = input()
        con.login(username, password)

    elif command == 'register':
        print('Введите имя пользователя')
        username = input()
        print('Введите пароль')
        password = input()
        print('Введите пароль еще раз')
        password2 = input()
        con.register(username, password, password2)

    elif command == 'create ad':
        print('Введите название')
        title = input()
        print('Введите описание')
        text = input()
        con.createAd(title, text)

    elif command == 'logout':
        con.logout()

    elif command == 'show ads':
        con.showAds()
    else:
        print('Неизвестная команда')
