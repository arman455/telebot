def decorator(func):

    def into():
        print("----------")
        func()
        print("----------")

    return into


@decorator
def happy_birthday():
    print("С ДНЕМ РОЖДЕНИЯ ВАСЯ")

@decorator
def say_bye():
    print("ПОКА, ЧУВАЧКИ")

say_bye()



