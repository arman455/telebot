import telebot
import random
import json
import os

bot = telebot.TeleBot("5950485062:AAHk11VIaP2FRIRJuIFcsaXHWyNrxzI5kuk")

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

xo_keyboard = telebot.types.InlineKeyboardMarkup(row_width=3)
count = 1
for i in range(3):        
    xo_btn1 = telebot.types.InlineKeyboardButton("⬜️", callback_data = f"xo{count+0}")
    xo_btn2 = telebot.types.InlineKeyboardButton("⬜️", callback_data = f"xo{count+1}")
    xo_btn3 = telebot.types.InlineKeyboardButton("⬜️", callback_data = f"xo{count+2}")
    count += 3
    xo_keyboard.add(xo_btn1, xo_btn2, xo_btn3)
    

@bot.message_handler(content_types=["text", "photo"])
def get_text(message):
    if message.text == "/start" or message.text == "/new_game":  
        bot.send_message(message.chat.id, "Будь ласка, оберіть гру!", reply_markup = reply_keyboard)
    elif message.text == "1️⃣Вгадай число":
        bot.send_message(message.chat.id, "Ви обрали гру Вгадай число", reply_markup = telebot.types.ReplyKeyboardRemove())
        
        game_number = random.randint(1,100)
        game_session = {
            'game_number': game_number
        }
        with open(str(message.chat.id)+'.json', "w") as file:
            json.dump(game_session, file)
            
        def guess_number(res):
            with open(str(message.chat.id)+'.json', "r") as f:
                user_dict = json.load(f)
                numb = user_dict["game_number"]
                numb = str(numb) 
                if numb == res.text:
                    bot.send_message(message.chat.id, "Ви вгадали! Оберіть іншу гру:", reply_markup = reply_keyboard)
                else:
                    reset = bot.send_message(message.chat.id, "Ви не вгадали. Спробуйте ще раз:")
                    if int(numb) > int(res.text):
                        bot.send_message(message.chat.id, "Загадане число більше")
                    if int(numb) < int(res.text):
                        bot.send_message(message.chat.id, "Загадане число менше")
                    bot.register_next_step_handler(reset, guess_number)

        res = bot.send_message(message.chat.id, "Число сгенеровоно! Введіть число:")
        bot.register_next_step_handler(res, guess_number)

    elif message.text == "🪨✂️📄Камінь ножиці папір":
        bot.send_message(message.chat.id, "Ви обрали гру Камінь ножиці папір")
        bot.send_message(message.chat.id, "Будь ласка, оберіть символ:", reply_markup = inline_keyboard)
    
    elif message.text == "❌⭕️Хрестики нулики":
        bot.send_message(message.chat.id, "Ви обрали гру Хрестики нулики")
        bot.send_message(message.chat.id, "Будь ласка, оберіть клітинку:", reply_markup = xo_keyboard)
        
def change_board():
    pass

def make_move(id, data, old_moves):
    if old_moves == None: 
        dict_game3 = {
            "id": id,
            "all_cells": []
        }
    else:
        dict_game3 = {
            "id": id,
            "all_cells": old_moves 
        }
        
    player_move = {
        data[-1] : "x"
    }
    dict_game3["all_cells"].append(player_move)

    bot_replay = True
    while bot_replay == True: 
        bot_replay = False
        choice_bot = str(random.randint(1, 9))     
        print("Результат бота:", choice_bot, "существующие клетки:", dict_game3["all_cells"])
        for n in dict_game3["all_cells"]:
            if choice_bot == n:     
                bot_replay = True  
    
    if bot_replay == False:                
        bot_move = {
            choice_bot : "o"
        }              
        dict_game3["all_cells"].append(bot_move)
        
        return dict_game3
        

@bot.callback_query_handler(func = lambda call: True)
def get_call(call):

    #проверяем, является ли это ходом из игры Крестики нолики
    if call.data in ["xo1","xo2","xo3","xo4","xo5","xo6","xo7","xo8","xo9"]: #если является, то...
        if "zxc.json" not in os.listdir(): #проверяем запись файла в нашем компьютере
            with open("zxc.json","w") as file: #когда файл не найден - создаем свой с нуля
                res = make_move(call.message.chat.id, call.data, None) #делаем первый ход (свой и бота)
                bot.send_message(call.message.chat.id, "Будь ласка, оберіть клітинку:", reply_markup = xo_keyboard)
                json.dump(res, file) #записали обновленный результат в систему
        else:
            with open("zxc.json","r") as file: #если же файл найден в системе
                my_js = json.load(file) #считываем что в нем
            
            with open("zxc.json","w") as file: #открываем запись
                res = make_move(call.message.chat.id, call.data, my_js["all_cells"]) #делаем ход (свой и бота)
                bot.send_message(call.message.chat.id, "Будь ласка, оберіть клітинку:", reply_markup = xo_keyboard)
                json.dump(res, file) #записали обновленный результат в систему
    #---------------------------------------------------------
    
    else:
        call_list = ["Stone","Scissor","Paper"]
        rand_choice = random.choice(call_list)
        if call.data != rand_choice:
            if call.data =="Stone" and rand_choice == "Scissor":
                bot.send_message(call.message.chat.id, "Ваш вибір камінь")
                bot.send_message(call.message.chat.id, "Вибір боту ножиці")
                bot.send_message(call.message.chat.id, "Ви перемогли! Оберіть іншу гру", reply_markup = reply_keyboard)
                print("Перемога")
            elif call.data =="Stone" and rand_choice == "Paper":
                bot.send_message(call.message.chat.id, "Ваш вибір камінь")
                bot.send_message(call.message.chat.id, "Вибір боту папір")
                bot.send_message(call.message.chat.id, "Ви програли! Спробуйте ще раз", reply_markup = inline_keyboard)
                print("Поразка")        
            if call.data =="Scissor" and rand_choice == "Paper":
                bot.send_message(call.message.chat.id, "Ваш вибір ножиці")
                bot.send_message(call.message.chat.id, "Вибір боту папір")
                bot.send_message(call.message.chat.id, "Ви перемогли! Оберіть іншу гру", reply_markup = reply_keyboard)
                print("Перемога")
            elif call.data =="Scissor" and rand_choice == "Stone":
                bot.send_message(call.message.chat.id, "Ваш вибір ножиці")
                bot.send_message(call.message.chat.id, "Вибір боту камінь")
                bot.send_message(call.message.chat.id, "Ви програли! Спробуйте ще раз", reply_markup = inline_keyboard)
                print("Поразка")
            if call.data =="Paper" and rand_choice == "Stone":
                bot.send_message(call.message.chat.id, "Ваш вибір папір")
                bot.send_message(call.message.chat.id, "Вибір боту камінь")
                bot.send_message(call.message.chat.id, "Ви перемогли! Оберіть іншу гру", reply_markup = reply_keyboard)
                print("Перемога")
            elif call.data =="Paper" and rand_choice == "Scissor":
                bot.send_message(call.message.chat.id, "Ваш вибір папір")
                bot.send_message(call.message.chat.id, "Вибір боту ножиці")
                bot.send_message(call.message.chat.id, "Ви програли! Спробуйте ще раз", reply_markup = inline_keyboard)
                print("Поразка")
        else:
            bot.send_message(call.message.chat.id, "Ніхто не переміг! Спробуйте ще раз", reply_markup = inline_keyboard)
            print("Нічия")
  
bot.infinity_polling()