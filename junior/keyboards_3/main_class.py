import telebot

token = "..."

bot = telebot.TeleBot(token)

keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
btn1 = telebot.types.KeyboardButton("🤝 Поздороваться")
btn2 = telebot.types.KeyboardButton("🤝 Попрощаться")
btn3 = telebot.types.KeyboardButton("🤝 Пожать руку")
btn4 = telebot.types.KeyboardButton("🤝 Приветствовать")
keyboard.add(btn1, btn2, btn3, btn4)

@bot.message_handler(commands=["start"])
def start_click(message):
    bot.send_message(message.chat.id, "Hi", reply_markup=keyboard)

@bot.message_handler(content_types=["text"])
def send_text(message):
    if message.text == "🤝 Поздороваться":
        bot.send_message(message.chat.id, "Hi")
    if message.text == "🤝 Попрощаться":
        bot.send_message(message.chat.id, "Goodbye")

bot.infinity_polling()
