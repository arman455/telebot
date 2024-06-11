import telebot

bot = telebot.TeleBot("...")

@bot.message_handler(commands=["start", "yarik"])
def start(message):
    
    def get_name(user_name):
        print(user_name.text)
        user_age = bot.send_message(message.chat.id, "Пожалуйста введите возраст:")
        bot.register_next_step_handler(user_age, get_age)

    def get_age(user_age):
        print(user_age.text)
        try:
            a = int(user_age.text)
        except:
            answer_age = bot.send_message(message.chat.id, "Вы ввели не число! Введите правильно число:")
            bot.register_next_step_handler(answer_age, get_age)

    bot.send_message(message.chat.id, "Добро пожаловать. Пройдите регистрацию!")
    user_name = bot.send_message(message.chat.id, "Введите имя: ")
    bot.register_next_step_handler(user_name, get_name)

@bot.message_handler(content_types = ["text"]) 
def send_text(message):
    user_text = message.text.lower()
    if user_text in ["привет", "здравствуйте", "добрый день"]:
        bot.send_message(message.chat.id, "HELLO")

bot.infinity_polling()
