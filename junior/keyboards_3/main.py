import telebot

token = "..."
bot = telebot.TeleBot(token)

#Клавиатура текстовая (REPLY) - текстовое сообщение в чат
under_board = telebot.types.ReplyKeyboardMarkup(resize_keyboard = True, row_width = 1)
under_btn1 = telebot.types.KeyboardButton("Текст 1")
under_btn2 = telebot.types.KeyboardButton("Текст 2")
under_board.add(under_btn1, under_btn2)

#Клавиатура на вызовах (CALLBACK) - сигнал внутри системы
message_board = telebot.types.InlineKeyboardMarkup(row_width = 1)
message_btn1 = telebot.types.InlineKeyboardButton("Вызов 1", callback_data = "call1")
message_btn2 = telebot.types.InlineKeyboardButton("Вызов 2", callback_data = "call2")
message_board.add(message_btn1, message_btn2)

#Декоратор для комманд
@bot.message_handler(commands=["start"])
def start_click(message):
    bot.send_message(message.chat.id, "Начало, вот ваша клавиатура:", reply_markup = under_board)

#Декоратор для текста
@bot.message_handler(content_types=["text"])
def get_text(message):
    if message.text == "Текст 1":
        bot.send_message(message.chat.id, "Ответ1 - вызов Инлайн клавиатуры", reply_markup = message_board)
    elif message.text == "Текст 2":
        bot.send_message(message.chat.id, "Ответ2 - удаление клавиатуры", reply_markup = telebot.types.ReplyKeyboardRemove())

#Декоратор для вызовов
@bot.callback_query_handler(func = lambda call: True)
def get_call(call):
    if call.data == "call1":
        bot.send_message(call.message.chat.id, "Звонок1", reply_markup = None)
    elif call.data == "call2":
        bot.edit_message_text("Сообщение изменено", call.message.chat.id, call.message.id)

bot.infinity_polling()
