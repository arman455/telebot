def decorator(func):

    def into():
        print("----------")
        func()
        print("----------")

    return into
    

def happy_birthday():
    print("С ДНЕМ РОЖДЕНИЯ ВАСЯ")


decorator(happy_birthday)()











