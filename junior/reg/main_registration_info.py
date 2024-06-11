import telebot
import json

token = "6125184865:AAEKvZfpnuPNTsqASOMSRAsRnRW_8-Urj18"

bot = telebot.TeleBot(token)

Keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
but1 = telebot.types.KeyboardButton("Початок")
Keyboard.add(but1)


Keyboard2 = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2, one_time_keyboard=True)
but2 = telebot.types.KeyboardButton("Профіль")
Keyboard2.add(but2)


@bot.message_handler(commands=["start"])
def start_click(message):
    bot.send_message(message.chat.id, "Привіт", reply_markup = Keyboard)

@bot.message_handler(content_types=["text"])
def get_text(message):

    def get_name(user_name):
        user_dict["name"] = user_name.text
        print(user_name.text)
        user_last_name = bot.send_message(message.chat.id, "Введіть прізвище:")
        bot.register_next_step_handler(user_last_name, get_last_name)

    def get_last_name(user_last_name):
        user_dict["last_name"] =  user_last_name.text
        print(user_last_name.text)
        user_age = bot.send_message(message.chat.id, "Введіть вік:")
        bot.register_next_step_handler(user_age, get_age)
    
    def get_age(user_age):
        user_dict["age"] =  user_age.text
        print(user_age.text)
        bot.send_message(message.chat.id, "Реєстрація завершена!", reply_markup=Keyboard2)
        print(user_dict)

        file_name = str(message.chat.id) + ".json"
        with open(file_name, 'w') as f:
            json.dump(user_dict, f)

          
    if message.text == "Початок":
        user_dict = {
            "name": " ",
            "last_name": " ",
            "age": " "
        }

        bot.send_message(message.chat.id, "Привіт, пройдіть реєстрацію")
        user_name = bot.send_message(message.chat.id, "Введіть ім'я:")
        bot.register_next_step_handler(user_name, get_name)


    if message.text == "Профіль":
        try:
            with open(str(message.chat.id)+".json", "r") as f:
                user_dict = json.load(f)
                text = ""
                for i in user_dict:
                    text += i + ": " + user_dict[i] + ";\n"
                bot.send_message(message.chat.id, text)
        except:
            bot.send_message(message.chat.id, "Error")
        
bot.infinity_polling()