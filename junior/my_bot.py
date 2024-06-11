import telebot
import json
import random
import os
import time

token = "5950485062:AAHk11VIaP2FRIRJuIFcsaXHWyNrxzI5kuk"

bot = telebot.TeleBot(token)

keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
keyboard2 = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)

button1 = telebot.types.KeyboardButton("Почати")
button2 = telebot.types.KeyboardButton("Привітання😊")
button3 = telebot.types.KeyboardButton("Мій профіль")
button4 = telebot.types.KeyboardButton("Прощання😢")
button5 = telebot.types.KeyboardButton("Ігри🎮")
keyboard.add(button1)
keyboard2.add(button2,button3,button4,button5)

reply_keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
btn1 = telebot.types.KeyboardButton("1️⃣Вгадай число")
btn2 = telebot.types.KeyboardButton("🪨✂️📄Камінь ножиці папір")
btn3 = telebot.types.KeyboardButton("❌⭕️Хрестики нулики")
reply_keyboard.add(btn1, btn2, btn3)

inline_keyboard = telebot.types.InlineKeyboardMarkup()
inl1 = telebot.types.InlineKeyboardButton("🪨", callback_data = "Stone")
inl2 = telebot.types.InlineKeyboardButton("✂️", callback_data = "Scissor")
inl3 = telebot.types.InlineKeyboardButton("📄", callback_data = "Paper")
inline_keyboard.add(inl1, inl2, inl3)


@bot.message_handler(commands=["start"])
def start2(message):
    bot.send_message(message.chat.id, "Натисніть кнопку 'Почати'", reply_markup=keyboard)
    bot.register_next_step_handler(message, start)
    

def start(message):

    user_dict = {
        "Ім'я": "" ,
        "Прізвище": "",
        "Вік": "",
        "Пошта": "",
        "Телефон": "",
        
    }

    def get_name(user_name):
        user_dict["Ім'я"] = user_name.text
        user_age = bot.send_message(message.chat.id, "Введіть будь-ласка вік: ")
        bot.register_next_step_handler(user_age, get_age)

    def get_surname(user_sername):
        user_dict["Прізвище"] = user_sername.text
        user_email = bot.send_message(message.chat.id, "Введіть електрону пошту:")
        bot.register_next_step_handler(user_email, get_email)

    def get_email(user_email):
        user_dict["Пошта"] = user_email.text
        user_phone = bot.send_message(message.chat.id, "Введіть номер телефону:")
        bot.register_next_step_handler(user_phone, get_phone)

    def get_phone(user_phone):
        user_dict["Телефон"] = user_phone.text
        bot.send_message(message.chat.id, "Реєстрацію закінчено:)")
        print(user_dict)
        
        file_name = "json_my_bot\\" + str(message.chat.id) + '.json'
        with open(file_name,"w", encoding="utf-8") as file:
            json.dump(user_dict, file, ensure_ascii=False)

        bot.send_message(message.chat.id, "Тепер ви можете працювати з ботом.", reply_markup=keyboard2)


    def get_age(user_age):
        user_dict["Вік"] = user_age.text
        try:
            a = int(user_age.text)
            user_surname = bot.send_message(message.chat.id, "Введіть прізвище:")
            bot.register_next_step_handler(user_surname, get_surname)
        except:
            answer_age = bot.send_message(message.chat.id, "Введіть число :(")
            bot.register_next_step_handler(answer_age, get_age)
    
    
    bot.send_message(message.chat.id, "Привіт, пройди реєстрацію!",reply_markup = telebot.types.ReplyKeyboardRemove())
    user_name = bot.send_message(message.chat.id, "Введіть ім'я:")
    bot.register_next_step_handler(user_name, get_name)


@bot.message_handler(content_types=["text"])

def send_text(message):
    
    user_say = message.text.lower()

    if user_say == "скинь фотку":
        picture1 = open("photo//R.jpg", "rb")
        bot.send_photo(message.chat.id, picture1, "Українська краса😍")
        picture1.close()
    elif user_say == "скинь ще":
        picture2 = open("photo//OIP.jpg", "rb")
        bot.send_photo(message.chat.id, picture2, "Озеро України Синевир🖼️")
        picture2.close()
    elif user_say == "покажи більше":
        picture3 = open("photo//mountain.jpg", "rb")
        bot.send_photo(message.chat.id, picture3, "А це гори України⛰️")
        picture3.close()

        picture4 = open("photo//field.jpg", "rb")
        bot.send_photo(message.chat.id, picture4, "Поле😚")
        picture4.close()
    elif user_say == "круто":
        picture5 = open("photo//holy.jpg", "rb")
        bot.send_photo(message.chat.id, picture5, "І на останок - Національний ботанічний сад імені Миколи Гришка НАН України")
        picture5.close()
    

    if user_say == "ігри🎮":
        bot.send_message(message.chat.id, "Будь ласка, оберіть гру!", reply_markup = reply_keyboard)
    elif message.text == "1️⃣Вгадай число":
        bot.send_message(message.chat.id, "Ви обрали гру Вгадай число", reply_markup = telebot.types.ReplyKeyboardRemove())

        game_num = random.randint(1,100)
        print(game_num)
        tries = 0        

        def guess_number(res, tries):
            tries += 1
            if str(game_num) == res.text:
                bot.send_message(message.chat.id, "Ви вгадали! Оберіть іншу гру:", reply_markup = reply_keyboard)
                #-----------------------------------------
                id_str = str(message.chat.id)
                game_directory = "games_history/dir_" + id_str

                if os.path.exists(game_directory) == False:
                    os.mkdir(game_directory)
                    
                files = os.listdir(game_directory)
                files.sort()
                if len(files) == 0:
                    game_number = "1"
                else:
                    last_file_name = files[-1]
                    game_number = str(int(last_file_name.split(".")[0])+1)
                
                game_session = {
                    "name": "guess_number",
                    "time": time.time(),
                    "answer": game_num,
                    "tries": tries
                }
                with open(game_directory+"/"+game_number+'.json', "w") as file:
                    json.dump(game_session, file)
                #-----------------------------------------
            else:                
                if game_num > int(res.text):
                    reset = bot.send_message(message.chat.id, "Ви не вгадали. Загадане число більше. Спробуйте ще раз:")
                if game_num < int(res.text):
                    reset = bot.send_message(message.chat.id, "Ви не вгадали. Загадане число менше. Спробуйте ще раз:")
                bot.register_next_step_handler(reset, guess_number, tries)
        
        res = bot.send_message(message.chat.id, "Число сгенеровоно! Введіть число:")
        bot.register_next_step_handler(res, guess_number, tries)
  
    elif message.text == "🪨✂️📄Камінь ножиці папір":
        bot.send_message(message.chat.id, "Ви обрали гру Камінь ножиці папір")
        result_2 = bot.send_message(message.chat.id, "Будь ласка, оберіть символ:", reply_markup = inline_keyboard)
        
    
    elif message.text == "❌⭕️Хрестики нулики":
        bot.send_message(message.chat.id, "Ви обрали гру Хрестики нулики")

    if user_say == "мій профіль":
        try:
            with open("json_my_bot\\"+ str(message.chat.id)+".json", "r", encoding="utf-8") as f:
                user_dict = json.load(f)
                text = ""
                for i in user_dict:
                    text += i + ": " + user_dict[i] + ";\n"
                bot.send_message(message.chat.id, text)
        except:
            bot.send_message(message.chat.id, "Error")
        

    if user_say == "привітання😊":
        bot.send_message(message.chat.id, "Привіт")
    if user_say == "прощання😢":
        bot.send_message(message.chat.id, "Бувай, мені приємно було з тобою спілкуватися)")

    if user_say in ["привет" , "добрый день" , "доброе утро" ,"хаюшки" , "здравствуйте", "здорова", "приветик"]:
        bot.send_message(message.chat.id, "Я не розумію🙄, продовжіть УКРАЇНСЬКОЮ😊🇺🇦")
    if user_say in ["привіт" , "hi" , ")" ,"hello" , "добрий день", "здоров", "ку"]:
        bot.send_message(message.chat.id, "Привіт")
    if user_say in ["як справи?" , "як сямаєш?" ,"як справи" , "як сямаєш" ,"how are you?" ,"how are you"]:
        bot.send_message(message.chat.id, "У мене все добре:) ")
        bot.send_message(message.chat.id, "А як у тебе? ")
    if user_say in ["все добре" ,"все ок" , "нормально" ,"добре" , "клас" ,"чудово", "ок", "норм"]:
        bot.send_message(message.chat.id, "Чудово, я радий за тебе:)")
    if user_say in ["бувай" , "до зустрічі" ,"прощавай","goodbye" , "bye"]:
        bot.send_message(message.chat.id, "Бувай, мені приємно було з тобою спілкуватися)")
    if  user_say == "cookie":
        pass

@bot.callback_query_handler(func = lambda call: True)
def get_call(call):
    call_list = ["Stone","Scissor","Paper"]
    rand_choice = random.choice(call_list)
    amount_victory = 0
    loss_amount = 0

    if call.data != rand_choice:
        if call.data == "Stone" and rand_choice == "Scissor":
            bot.send_message(call.message.chat.id, "Ваш вибір камінь")
            bot.send_message(call.message.chat.id, "Вибір боту ножиці")
            bot.send_message(call.message.chat.id, "Ви перемогли! Оберіть іншу гру", reply_markup = reply_keyboard)
            amount_victory += 1
            print("Победа")
        elif call.data =="Stone" and rand_choice == "Paper":
            bot.send_message(call.message.chat.id, "Ваш вибір камінь")
            bot.send_message(call.message.chat.id, "Вибір боту папір")
            bot.send_message(call.message.chat.id, "Ви програли! Спробуйте ще раз", reply_markup = inline_keyboard)
            loss_amount += 1
            print("Поражение")        
        if call.data =="Scissor" and rand_choice == "Paper":
            bot.send_message(call.message.chat.id, "Ваш вибір ножиці")
            bot.send_message(call.message.chat.id, "Вибір боту папір")
            bot.send_message(call.message.chat.id, "Ви перемогли! Оберіть іншу гру", reply_markup = reply_keyboard)
            amount_victory += 1
            print("Победа")
        elif call.data =="Scissor" and rand_choice == "Stone":
            bot.send_message(call.message.chat.id, "Ваш вибір ножиці")
            bot.send_message(call.message.chat.id, "Вибір боту камінь")
            bot.send_message(call.message.chat.id, "Ви програли! Спробуйте ще раз", reply_markup = inline_keyboard)
            loss_amount += 1
            print("Поражение")
        if call.data =="Paper" and rand_choice == "Stone":
            bot.send_message(call.message.chat.id, "Ваш вибір папір")
            bot.send_message(call.message.chat.id, "Вибір боту камінь")
            bot.send_message(call.message.chat.id, "Ви перемогли! Оберіть іншу гру", reply_markup = reply_keyboard)
            amount_victory += 1
            print("Победа")
        elif call.data =="Paper" and rand_choice == "Scissor":
            bot.send_message(call.message.chat.id, "Ваш вибір папір")
            bot.send_message(call.message.chat.id, "Вибір боту ножиці")
            bot.send_message(call.message.chat.id, "Ви програли! Спробуйте ще раз", reply_markup = inline_keyboard)
            loss_amount += 1
            print("Поражение")
    else:
        bot.send_message(call.message.chat.id, "Ніхто не переміг! Спробуйте ще раз", reply_markup = inline_keyboard)
        print("Ничья")
        loss_amount += 1

    if call.data == "Stone" and rand_choice == "Scissor" or call.data =="Scissor" and rand_choice == "Paper" or call.data =="Paper" and rand_choice == "Stone":
        id_str = str(call.message.chat.id)
        game_directory = "games_history/dir_" + id_str

        if os.path.exists(game_directory) == False:
            os.mkdir(game_directory)
                        
        files = os.listdir(game_directory)
        files.sort()
        if len(files) == 0:
            game_number = "1"
        else:
            last_file_name = files[-1]
            game_number = str(int(last_file_name.split(".")[0])+1)
                    
            game_session2 = {
                "name": "crosses zeros",
                "time": time.time(),
                "amount_victory": amount_victory,
                "loss_amount": loss_amount
            }
        with open(game_directory+"/"+game_number+'.json', "w") as file:
            json.dump(game_session2, file)

bot.infinity_polling()