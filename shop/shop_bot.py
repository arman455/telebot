import telebot
import register
import keyboard
from settings import data, my_col_u, my_col_p

bot = telebot.TeleBot(data["bot"]["tg_token"])

@bot.message_handler(commands=["start"])
def main_func(message):    
    register.registration(bot, message)


@bot.message_handler(content_types=["text", "photo"])
def get_text(message):
    if message.text == "🪪 Мій профіль":
        user_info = my_col_u.find_one({"tg_id" : message.chat.id})

        # <b> or <strong> - жирный
        # <i> or <em> - наклонный
        t0 = f"*Твій профіль*\n\n" 
        t1 = f"Ім'я: {user_info['firstname']}\n"
        t2 = f"Прізвище: {user_info['lastname']}\n"
        t3 = f"Пошта: {user_info['email']}\n"
        t4 = f"Номер телефону: {user_info['phone']}\n"
        t5 = f"Адреса: {user_info['address']}\n"

        info_parsed = t0 + t1 + t2 + t3 + t4 + t5
        bot.send_message(message.chat.id, info_parsed, parse_mode="Markdown", reply_markup=keyboard.profile_keyboard)

    elif message.text == "✏️ Змінити інформацію профілю":
        bot.send_message(message.chat.id, "Оберіть поле, яке бажаєте змінити:", parse_mode="Markdown", reply_markup=keyboard.change_profile_keyboard)

    elif message.text == "🔍 Про магазин":
        t0 = f"*Про магазин*\n\n" 
        t1 = f"Назва: {data['bot']['bot_name']}\n"
        t2 = f"Пошта: {data['bot']['email']}\n"
        t3 = f"Номер телефону: {data['bot']['phone_number']}\n"
        t4 = f"Адреса: {data['bot']['address']}\n"

        info_parsed = t0 + t1 + t2 + t3 + t4
        bot.send_message(message.chat.id, info_parsed, parse_mode="Markdown")
        
    elif message.text == "🛒 Кошик":
        get_user = my_col_u.find_one({"tg_id": message.chat.id})
        user_basket = get_user["basket"]
        info_parsed = "*Кошик користувача*\n\n"
        whole_price = 0
        for k,v in user_basket.items():
            item_id = k
            item_amount = v
            product = my_col_p.find_one({"id": item_id})
            t1 = f"{item_id}. {product['brand']} {product['name']} ({product['price']} x {item_amount} = {product['price'] * item_amount} грн)\n"
            item_price = product['price'] * item_amount
            info_parsed += t1
            whole_price += item_price
        t2 = f"\n*Усього до сплати: {whole_price}*"
        info_parsed += t2
        
        bot.send_message(message.chat.id, info_parsed, parse_mode="Markdown", reply_markup=keyboard.basket_keyboard)
        
    elif message.text == "🔙 Повернутися назад":
        register.registration(bot, message)

bot.infinity_polling()