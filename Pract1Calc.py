print("Калькулятор")
print("\n Выберите операцию: \n 1. Сложение \n 2. Вычитание \n 3. Умножение \n 4. Деление")
a = int(input())
y = int(0)
print ("\nВведите количество чисел для операции: " )
x = int(input())
print("Введите число: ")
c = int(input())
while x > 1:
    if a == 1: 
        print("Введите число: ")
        b = int(input())
        y = b + c
        c = y
        x -=1
    if a == 2:
        print("Введите число: ")
        b = int(input())
        y = c - b
        c = y
        x -=1
    if a == 3:
        print("Введите число: ")
        b = int(input())
        y = b * c
        c = y
        x -=1
    if a == 4:
        print("Введите число: ")
        b = int(input())
        if (b == 0):
            print ("Операция невозможна")
            break
        else:
            y = c / b
            c = y
            x -=1
print("\nРезультат: ")
print(f"{y}")