def mystery():
    from random import randint, choice
    ch = 0
    while ch == 0:
        ch = 1
        select = int(input("---------- 1: Easy Level ----------\n---------- 2: Meduim Level ----------\n---------- 3: Hard Level ----------\nSelect your level:\n>>    "))
        attempt = 0
        if select == 1:
            guess = randint(0, 100)
            data = int(input("Guess the number from 0 -> 100:\n>>    "))
            for i in range(15):
                if data == guess:
                    attempt += 1
                    print("YOU GOT IT IN", attempt, "attempts")
                    break
                elif data > guess:
                    attempt += 1
                    count = 15 - attempt
                    print(count, "attempts left.")
                    data = int(input("less\n>>    "))
                elif data < guess:
                    attempt += 1
                    count = 15 - attempt
                    print(count, "attempts left.")
                    data = int(input("more\n>>    "))
                if attempt == 14:
                    if data != guess:
                        print("Failed :( try again later...")
                        break
        elif select == 2:
            guess = randint(0, 1000)
            data = int(input("Guess the number from 0 -> 1000:\n>>    "))
            for i in range(10):
                if data == guess:
                    attempt += 1
                    print("YOU GOT IT IN", attempt, "attempts")
                    break
                elif data > guess:
                    attempt += 1
                    count = 10 - attempt
                    print(count, "attempts left.")
                    data = int(input("less\n>>    "))
                elif data < guess:
                    attempt += 1
                    count = 10 - attempt
                    print(count, "attempts left.")
                    data = int(input("more\n>>    "))
                if attempt == 9:
                    if data != guess:
                        print("Failed :( try again later...")
                        break
        elif select ==3:
            guess = randint(10, 100)
            chr = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
            char = choice(chr)
            data = int(input("Guess the number from 10 -> 100:\n>>    "))
            datach = str(input("Guess the character from a -> z:\n>>    "))
            for i in range(10):
                datach = datach.lower()
                if data == guess and datach == char:
                    attempt += 1
                    count = 10 - attempt
                    print(count, "attempts left.")
                    print("YOU GOT IT IN", attempt, "attempts")
                    break
                elif data == guess and datach > char:
                    attempt += 1
                    count = 10 - attempt
                    print(count, "attempts left.")
                    print("Number is correct. Character is before")
                    datach = str(input("character is before\n>>    "))
                    datach = datach.lower()
                elif data == guess and datach < char:
                    attempt += 1
                    count = 10 - attempt
                    print(count, "attempts left.")
                    print("Number is correct. Character is after")
                    datach = str(input("character is after\n>>    "))
                    datach = datach.lower()
                elif data > guess and datach == char:
                    attempt += 1
                    count = 10 - attempt
                    print(count, "attempts left.")
                    print ("Character is correct. Number is less")
                    data = int(input("number is less\n>>    "))
                elif data > guess and datach > char:
                    attempt += 1
                    count = 10 - attempt
                    print(count, "attempts left.")
                    print("Number is less. Character is before")
                    data = int(input("number is less\n>>    "))
                    datach = str(input("character is before\n>>    "))
                    datach = datach.lower()
                elif data > guess and datach < char:
                    attempt += 1
                    count = 10 - attempt
                    print(count, "attempts left.")
                    print("Number is less. Character is after")
                    data = int(input("number is less\n>>    "))
                    datach = str(input("character is after\n>>    "))
                    datach = datach.lower()
                elif data < guess and datach == char:
                    attempt += 1
                    count = 10 - attempt
                    print(count, "attempts left.")
                    print("Character is correct. Number is more")
                    data = int(input("number is more\n>>    "))
                elif data < guess and datach < char:
                    attempt += 1
                    count = 10 - attempt
                    print(count, "attempts left.")
                    print("Number is more. Character is after")
                    data = int(input("number is more\n>>    "))
                    datach = str(input("character is after\n>>    "))
                    datach = datach.lower()
                elif data < guess and datach > char:
                    attempt += 1
                    count = 10 - attempt
                    print(count, "attempts left.")
                    print("Number is more. Character is before")
                    data = int(input("number is more\n>>    "))
                    datach = str(input("character is before\n>>    "))
                    datach = datach.lower()
                if attempt == 9:
                    if data != guess or datach != char:
                        print("Failed :( try again later...")
                        break
        else:
            print("error at choicing level :(")
            ch = 0
def euclidean_division():
    n1 = int(input('Choose the divisor:\n>>   '))
    n2 = int(input('Choose the denominator:\n>>   '))
    if n2 == 0:
        print("ZeroDivisionError: division by zero")
    else:
        print(f"Q: {n1//n2}\nR: {n1%n2}")
def mental_calculation():
    from time import sleep
    from threading import Thread
    from random import randint,choice
    t = 1
    print('You must get most points in mental calculation in 30 secondes')
    sleep(5)
    def SpeedRun():
        p = 0
        while t > 0:
            f = randint(0,10)
            s = randint(0,10)
            rand = ['add', 'sub', 'mult', 'div']
            o = choice(rand)
            if o == 'add':
                data = f + s
                ans = int(input(str(f)+' + '+str(s)+' = ?\n>>   '))
                if ans == data:
                    print('Correct!')
                    p += 1
                else:
                    print('Fail!')
            if o == 'sub':
                data = f - s
                ans = int(input(str(f)+' - '+str(s)+' = ?\n>>   '))
                if ans == data:
                    print('Correct!')
                    p += 1
                else:
                    print('Fail!')
            if o == 'mult':
                data = f * s
                ans = int(input(str(f)+' * '+str(s)+' = ?\n>>   '))
                if ans == data:
                    print('Correct!')
                    p += 1
                else:
                    print('Fail!')
            if o == 'div':
                s = randint(1,5)
                if s == 1:
                    f = randint(0,10)
                elif s == 2:
                    choices = [0,2,4,6,8,10]
                    f = choice(choices)
                elif s == 3:
                    choices = [0,1,3,6,9]
                    f = choice(choices)
                elif s == 4:
                    choices = [0,4,8]
                    f = choice(choices)
                elif s == 5:
                    choices = [0,5,10]
                    f = choice(choices)
                data =  f / s
                ans = int(input(str(f)+' / '+str(s)+' = ?\n>>   '))
                if ans == data:
                    print('Correct!')
                    p += 1
                else:
                    print('Fail!')
        if t == 0:
            print('Time is up!\nYou score is',p)
    Thread(target=SpeedRun).start()
    sleep(30)
    t = 0
def root(num, nth=2):
    return num**(1/nth)+abs(num)-abs(num)