from datetime import datetime
import pyodbc
from pydoc import ErrorDuringImport
import random

conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=SUNSHINE-IOKI\SQLEXPRESS;' 
                      'Database=Store_BD;'
                      'Trusted_Connection=yes;')

def CardAdd(usId, card, value):
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Card WHERE User_ID = ?', usId)
    result = cursor.fetchone()
    if (result is not None):
        cursor.execute('UPDATE Card set Card = ?, Card_Value = ? where User_ID = ?', card, value, usId)
        cursor.commit()
    else:
        cursor.execute('SELECT MAX(ID_Card) FROM Card')
        max_id = cursor.fetchone()[0]
        if max_id is None:
            new_id = 1
        else:
            new_id = max_id + 1
        cursor.execute('INSERT INTO Card (ID_Card, User_ID, Card, Card_Value) VALUES (?, ?, ?, ?)', new_id, usId, card, value)
        conn.commit()
    return value

def Card(usId):
    cursor = conn.cursor()
    cursor.execute('SELECT Card FROM Card WHERE User_ID = ?', usId)
    result = cursor.fetchone()[0]
    if (result is not None):
        print('Пользователь №' + f'{usId}' + ' Карта: ' + f'{result}')
    else: 
        print('Такого пользователя не существует, либо отсутствует карта лояльности.')

def History(usId):
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM History WHERE User_ID = ?', usId)
    if (cursor.fetchone() is not None):
        for row in cursor.fetchall():                
            print('Пользователь №' + f'{row[1]}' + ' Заказ: ' + f'{row[4]}' + ' Цена: ' + f'{row[3]}' + ' Дата: ' + f'{row[2]}')
    else: 
        print('Такого пользователя не существует, либо история покупок пуста.')

def Balance(usId):
    cursor = conn.cursor()
    cursor.execute('Select User_Balance from Users where ID_User = ?', usId)
    result = cursor.fetchone()[0]
    if (result is not None):          
        print('Ваш баланс: ' + f'{result}', end=' \n')
    else: 
        print('Ошибка. Такого пользователя не существует.')

def Salad(usId):
    cursor = conn.cursor()
    value = int()
    i = int(input('Введите количество блюд, которое хотите заказать: '))
    if (i != ''):
        historyrecepy = ['']
        historycost = []
        tarakan = int(random.randint(1, 10))
        usertarakan = int(random.randint(1, 10))
        if(tarakan == 5 and usertarakan == 5):
            historyrecepy.append('Таракан. \n')
            print('В ваше блюдо попал таракан, теперь у вас скидка 30 процентов!')
            skidka = 1
            value = 30
        if (i % 5 == 0):
            print('Вы получаете блюдо от шефа бесплатно!')
            i = i - 1
            historyrecepy.append('Подарочное блюдо от шефа. \n')
            cursor.execute('SELECT Ingredient_Name FROM Ingridients')
            for row in cursor.fetchall():
                cursor.execute('SELECT ID_Ingredient FROM Ingridients WHERE Ingredient_Name = ?', row[0])
                idquan = cursor.fetchone()[0]     
                cursor.execute('UPDATE Ingridients set Quantity = Quantity - 5 where ID_Ingredient = ?', idquan)
                cursor.commit()
        while (i != 0):
            historyrecepy.append('\nБлюдо №' + f'{i}' + ': ')
            print('Введите количество ингридиентов, которое хотите добавить в салат, либо введите "0", если хотите исключить ингридиент.')
            cursor.execute('SELECT Ingredient_Name FROM Ingridients')
            if (cursor.fetchone() is not None):
                for row in cursor.fetchall():                
                        print(row[0], end=' ')
                        saladquant = int(input())
                        if (saladquant > 0):
                            cursor.execute('SELECT ID_Ingredient FROM Ingridients WHERE Ingredient_Name = ?', row[0])
                            ingid = cursor.fetchone()[0]
                            cursor.execute('SELECT Quantity FROM Ingridients WHERE Ingredient_Name = ?', row[0])
                            ingquant = cursor.fetchone()[0]
                            cursor.execute('SELECT Cost FROM Ingridients WHERE Ingredient_Name = ?', row[0])
                            ingcost = cursor.fetchone()[0]
                            historycost.append(ingcost * saladquant)
                            if (ingquant >= saladquant):
                                cursor.execute('UPDATE Ingridients set Quantity = Quantity - ? where ID_Ingredient = ?', saladquant, ingid)
                                cursor.commit()
                                historyrecepy.append(f"{row[0]}" + f" {saladquant}" + " шт., ")
                            elif(ingquant < saladquant):
                                print('Данный товар отсутствует на складе в данном количестве, добавлено всё, что есть.')
                                cursor.execute('UPDATE Ingridients set Quantity = Quantity - ? where ID_Ingredient = ?', ingquant, ingid)
                                cursor.commit()
                                historyrecepy.append(f"{row[0]}" + f" {saladquant}" + " шт., ")
                        elif (saladquant == 0):
                            historyrecepy.append(" ")
                i = i - 1
        cursor.execute('SELECT * FROM History WHERE User_ID = ?', usId)
        cursor.execute('SELECT MAX(ID_History) FROM History')
        max_id = cursor.fetchone()[0]
        if max_id is None:
            new_id = 1
        else:
            new_id = max_id + 1
        date = datetime.now()
        rec = "".join(historyrecepy)
        cost = sum(historycost)
        if (cost > 1000 and cost < 2000):
            card = 'Бронзовая карта лояльности'
            value = value + 5
            CardAdd(usId, card, value)
        elif (cost > 2000 and cost < 3000):
            card = 'Серебряная карта лояльности'
            value = value + 10
            CardAdd(usId, card, value)
        elif (cost > 3000):
            card = 'Золотая карта лояльности'
            value = value + 15
            CardAdd(usId, card, value)
        if (value is not None or skidka == 1):
            cost = cost * (1 - (value/100))
        cursor.execute('Select User_Balance from Users where ID_User = ?', usId)
        result = cursor.fetchone()[0]
        if (result < cost):          
            print('Вы не можете купить данный товар, ваш баланс: ' + f'{result}', end=' \n')
            return
        cursor.execute('UPDATE Users set User_Balance = User_Balance - ? where ID_User = ?', cost, usId)
        cursor.commit()
        cursor.execute('INSERT INTO History (ID_History, User_ID, Date, Summ, Salad) VALUES (?, ?, ?, ?, ?)', new_id, usId, date, cost, rec)
        conn.commit()
        out_file = open(f'{datetime.now().day} ' + f'{datetime.now().hour} ' + f'{datetime.now().minute}' +' Чек' + '.txt', 'w')
        out_file.write('------====-----Цезарь-----====----\n')
        out_file.write('****Горячая линия 8-800-555-35-35****\n')
        out_file.write(f'\n{rec}\n')
        out_file.write('_______________________________________\n')
        out_file.write('Итоговая сумма: ' + f'{cost}' + ' руб.\n')
        out_file.write(f'{date}\n')
        out_file.close()
        print('Чек заполнен.')
    else:
        print('Некорректный ввод данных.')
        return

def User(idUs):
    i = -1
    while (i < 0):
        i = i - 1
        chooseUser = int(input("Выберите операцию: \n 1. Заказать блюда \n 2. Посмотреть историю покупок \n 3. Посмотреть баланс \n 4. Посмотреть карты лояльности \n 5. Выйти из системы \n"))
        if (chooseUser == 1):
            if (idUs != ''):
                Salad(idUs)
            else:
                print('Некорректный ввод данных.')
                return
        elif (chooseUser == 2):
            if (idUs != ''):
                History(idUs)
            else:
                print('Некорректный ввод данных.')
                return
        elif(chooseUser == 3):
            if (idUs != ''):
                Balance(idUs)
            else:
                print('Некорректный ввод данных.')
                return
        elif (chooseUser == 4):
            if (idUs != ''):
                Card(idUs)
            else:
                print('Некорректный ввод данных.')
                return
        elif (chooseUser == 5):
            i = 0
            AuthReg()
        elif (chooseUser > 5 or chooseUser == 0):
            print("Такой операции нет")

def AddPrice(ingname):
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Ingridients WHERE Ingredient_Name = ?', ingname)
    if cursor.fetchone() is not None:
        costAdd = int(input('Какова новая цена продукта?'))
        cursor.execute('SELECT ID_Ingredient FROM Ingridients WHERE Ingredient_Name = ?', ingname)
        ingid = cursor.fetchone()[0]
        cursor.execute('UPDATE Ingridients set Cost = ? where ID_Ingredient = ?', costAdd, ingid)
        cursor.commit()
        print('Изменение успешно.')
    else:
        print('Такого продукта не существует.')

def AddQuantity(ingname):
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Ingridients WHERE Ingredient_Name = ?', ingname)
    if cursor.fetchone() is not None:
        quantityAdd = int(input('Сколько вы закупили?'))
        cursor.execute('SELECT Cost FROM Ingridients WHERE Ingredient_Name = ?', ingname)
        price = cursor.fetchone()[0]
        cursor.execute('SELECT ID_Ingredient FROM Ingridients WHERE Ingredient_Name = ?', ingname)
        ingid = cursor.fetchone()[0]
        ingcost = int(quantityAdd * price)
        cursor.execute('UPDATE Ingridients set Quantity = Quantity + ? where ID_Ingredient = ?', quantityAdd, ingid)
        cursor.commit()
        cursor.execute('UPDATE Users set User_Balance = User_Balance - ? where ID_User = 1', ingcost)
        cursor.commit()
        print('Пополнение успешно.')
        print ("С вашего счёта списано: "+f"{ingcost}"+" рублей.")
    else:
        print('Такого продукта не существует.')

def AddIngridient(ingname, quantity, price):
    cursor = conn.cursor()
    ingcost = int(price*quantity)
    cursor.execute('SELECT * FROM Ingridients WHERE Ingredient_Name = ?', ingname)
    if cursor.fetchone() is not None:
        choose = int(input('Такой продукт уже существует. Желаете пополнить склад (1 - Да, 2 - Нет)?'))
        if (choose == 1):
            AddQuantity(ingname)
        elif (choose == 2):
            print("Введите значения заново.")
            return
    cursor.execute('SELECT MAX(ID_Ingredient) FROM Ingridients')
    max_id = cursor.fetchone()[0]
    if max_id is None:
        new_id = 1
    else:
        new_id = max_id + 1
        cursor.execute('INSERT INTO Ingridients (ID_Ingredient, Ingredient_Name, Quantity, Cost)  VALUES (?, ?, ?, ?)', new_id, ingname, quantity, price)
        conn.commit()
        cursor.execute('UPDATE Users set User_Balance = User_Balance - ? where ID_User = 1', ingcost)
        cursor.commit()
        print('Добавление успешно.')
        print ("С вашего счёта списано: "+f"{ingcost}"+" рублей.")

def Admin():
    i = -1
    while (i < 0):
        i = i - 1
        chooseAdm = int(input("\n Выберите операцию: \n 1. Просмотреть склад \n 2. Пополнить склад \n 3. Добавить новый ингридиент \n 4. Изменить цену ингридиента  \n 5. Список покупок пользователя \n 6. Посмотреть баланс \n 7. Выйти из системы \n"))
        if (chooseAdm == 1):
            cursor = conn.cursor()
            cursor.execute('SELECT Ingredient_Name, Quantity, Cost FROM Ingridients')
            for row in cursor.fetchall():                
                print('Название: ' + f'{row[0]}' + ' Количество: ' + f'{row[1]}' + ' Цена: ' + f'{row[2]}')
        elif (chooseAdm == 2):
            ingname1 = str(input("Введите название ингридиента: "))
            if (ingname1 != ''):
                AddQuantity(ingname1)
            else:
                print('Некорректный ввод данных.')
                return
        elif (chooseAdm == 3):
            ingname2 = str(input("Введите название ингридиента: "))
            quantity = int(input("Введите количество: "))
            price = int(input("Введите цену за штуку: "))
            if (ingname2 != '' or quantity != '' or price != ''):
                AddIngridient(ingname2,quantity,price)
            else:
                print('Некорректный ввод данных.')
                return
        elif (chooseAdm == 4):
            ingname3 = str(input("Введите название ингридиента: "))
            if (ingname3 != ''):
                AddPrice(ingname3)
            else:
                print('Некорректный ввод данных.')
                return
        elif (chooseAdm == 5):
            usId = str(input("Введите ID пользователя: "))
            if (usId != ''):
                History(usId)
            else:
                print('Некорректный ввод данных.')
                return
        elif (chooseAdm == 6):
            Balance('1')
        elif (chooseAdm == 7):
            AuthReg()
            i = 0
        elif (chooseAdm >= 8 or chooseAdm == 0):
            print("Такой операции нет")

def Registration(phone_number):
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Users WHERE User_Phone = ?', phone_number)
    if cursor.fetchone() is not None:
        print('Этот номер телефона уже зарегистрирован.')
        return
    cursor.execute('SELECT MAX(ID_User) FROM Users')
    max_id = cursor.fetchone()[0]
    if max_id is None:
        new_id = 1
    else:
        new_id = max_id + 1
    balance = int(random.randint(500, 3000))
    role = 'Пользователь'
    cursor.execute('INSERT INTO Users (ID_User, User_Phone, User_Balance, User_Role) VALUES (?, ?, ?, ?)', new_id, phone_number, balance, role)
    conn.commit()
    print('Регистрация прошла успешно.')
    User(new_id)
    
def LogIn(phone_number):
    cursor = conn.cursor()
    cursor.execute('SELECT ID_User FROM Users WHERE User_Phone = ?', phone_number)
    result = cursor.fetchone()
    if result is None:
        print('Вы ещё не зарегистрированы в системе.')
        return None
    else:
        user_id = result[0]
        print('Авторизация прошла успешно. ID пользователя:', user_id)
        balance = int(random.randint(500, 3000))
        print('Вам начислено: ', balance)
        cursor.execute('UPDATE Users set User_Balance = User_Balance + ? where ID_User = ?', balance, user_id)
        cursor.commit()
        if (user_id == 1):
            Admin()
        else:
            User(user_id)

def AuthReg():
    print('Добро пожаловать в ресторан имени салата Цезаря!')
    action = input('Выберите действие \n 1. Регистрация \n 2. Авторизация \n ')
    if action == '1':
        phone_number = input('Введите номер телефона: ')
        if (phone_number != ''):
            Registration(phone_number)
        else:
            print('Некорректный ввод данных.')
            return
    elif action == '2':
        phone_number = input('Введите номер телефона: ')
        if (phone_number != ''):
            LogIn(phone_number)
        else:
            print('Некорректный ввод данных.')
            return

try:
  cursor = conn.cursor()
except pyodbc.Error as err:
  if err.errno == ErrorDuringImport.ER_ACCESS_DENIED_ERROR:
    print("Something is wrong with your user name or password")
  elif err.errno == ErrorDuringImport.ER_BAD_DB_ERROR:
    print("Database does not exist")
  else:
    print(err)
else:
    AuthReg()
    
    
