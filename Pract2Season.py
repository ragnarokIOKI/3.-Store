year = int(input("Введите год: "))
summ28 = 0
summ29 = 0
yearwithoutfeb = 0
r = 0
g = 1

for r in range(1,8):
    for g in range(1, 32):
        if len(str(g)) == 1:
            yearwithoutfeb += g
        elif len(str(g)) == 2:
            yearwithoutfeb += int(g / 10)
            yearwithoutfeb += g % 10

for r in range(1,5):
    for g in range(1, 31):
        if len(str(g)) == 1:
            yearwithoutfeb += g
        elif len(str(g)) == 2:
            yearwithoutfeb += int(g / 10)
            yearwithoutfeb += g % 10 


if (year % 4 == 0 and not (year % 100 == 0)) or year % 400 == 0:
    for g in range(1, 30):
        if len(str(g)) == 1:
            summ29 += g
        elif len(str(g)) == 2:
            summ29 += int(g / 10)
            summ29 += g % 10    
    result = yearwithoutfeb + summ29
    print("Год високосный: ", result)
else:
    for g in range(1, 29):
        if len(str(g)) == 1:
            summ28 += g
        elif len(str(g)) == 2:
            summ28 += int(g / 10)
            summ28 += g % 10    
    result = yearwithoutfeb + summ28
    print("Год не високосный: ",result)