import settings
import keyboard

def registration(bot, message):

    def user_enter(user_name):
        bot.send_message(message.chat.id, f"{user_name}, Ви в меню!", reply_markup=keyboard.menu_keyboard)

    def get_user_address(user_address):
        user_data["address"] = user_address.text
        settings.my_col_u.insert_one(user_data)
        user_enter(user_data["firstname"])

    def get_user_phone(user_phone):
        user_data["phone"] = user_phone.text
        user_address = bot.send_message(message.chat.id, "Введіть адресу:")
        bot.register_next_step_handler(user_address, get_user_address)

    def get_user_email(user_email):
        user_data["email"] = user_email.text
        user_phone = bot.send_message(message.chat.id, "Введіть номер телефону:")
        bot.register_next_step_handler(user_phone, get_user_phone)

    def get_user_lastname(user_lastname):
        user_data["lastname"] = user_lastname.text
        user_email = bot.send_message(message.chat.id, "Введіть поштову скриньку:")
        bot.register_next_step_handler(user_email, get_user_email)

    def get_user_firstname(user_name):
        user_data["firstname"] = user_name.text
        user_lastname = bot.send_message(message.chat.id, "Введіть прізвище:")
        bot.register_next_step_handler(user_lastname, get_user_lastname)

    bot.send_message(message.chat.id, f"Добрий день, {message.from_user.username}!")

    user_exists = settings.my_col_u.find_one(
        {"tg_id": message.chat.id}
    )
    
    if user_exists == None:        
        bot.send_message(message.chat.id, "Будь ласка, зареєструйтеся:")

        user_data =  {
            "tg_id": message.chat.id,
            "firstname" : "",
            "lastname" : "",
            "email" : "",
            "phone" : "",
            "address" : "",
            "basket" : {}
        }

        user_name = bot.send_message(message.chat.id, "Введіть ім'я:")
        bot.register_next_step_handler(user_name, get_user_firstname)
        
    else:
        user_enter(user_exists["firstname"])