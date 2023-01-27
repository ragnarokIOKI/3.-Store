result = 0
print("Введите количество введенных чисел:")
count = int(input())
while True:
    print("Введите операцию (*, /, -, +): ")
    operation = input()
    if operation == '*' or operation == '/' or operation == '+' or operation == '-':
        break
print("Введите число: ")
firstnumber = int(input())
for i in range(count - 1):
    print("Введите число: ")
    number = int(input())
    if operation == '+':
        if firstnumber != 0:
            result += firstnumber + number
        else:
            result += number
    elif operation == '-':
        if firstnumber != 0:
            result += firstnumber - number
        else:
            result -= number
    elif operation == '/':
        if number != 0:
            if firstnumber != 0:
                result += firstnumber / number
            else:
                result /= number
            if number == 0:
                print("На ноль делить нельзя!")
                if firstnumber != 0:
                    result += firstnumber / number
                else:
                    result /= number
    elif operation == '*':
        if firstnumber != 0:
            result += firstnumber * number
        else:
            result *= number
    else:
        print("Операция была введена неверно!")
    firstnumber = 0
print(f"Ответ: {result}")