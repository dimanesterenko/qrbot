import telebot
from telebot import types
import os

from qr_implementation import generate_qr_code
API_TOKEN = '7135897142:AAFInzxJBBNIMe9uDiwFx2Z75ce1dD39J-0'

bot=telebot.TeleBot(API_TOKEN)
user_data={}

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, """\
Hi there, I am qrencrypterbot.
I am here to generate qr-code by your link.\
""")
    menucka(message)
@bot.message_handler(commands=['create_qr'])
def create_qr(message):
    msg = bot.reply_to(message, "Please, enter a link for qr-generator:")
    bot.register_next_step_handler(msg, process_link_step)

def process_link_step(message):
    chat_id = message.chat.id
    link_data = message.text
    user_data[chat_id] = {'link': link_data}
    markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=1)
    markup.add('Image', 'Document')
    msg = bot.reply_to(message, "How would you like to receive the QR code? Choose format:", reply_markup=markup)
    bot.register_next_step_handler(msg, process_format_step)

def process_format_step(message):
    chat_id = message.chat.id
    format_choice = message.text.lower()
    link_data = user_data[chat_id]['link']
    filename = f"{chat_id}_{message.from_user.first_name}.png"
    generate_qr_code(link_data,filename)
    with open(filename, 'rb') as img_file:
        if format_choice == 'image':
            bot.send_photo(chat_id, img_file)
        elif format_choice == 'document':
            bot.send_document(chat_id, img_file, caption="Here is your QR code. You can save it to your gallery.")
        else:
            bot.reply_to(message, "Invalid choice. Please try again.")

    os.remove(filename)


@bot.message_handler(commands=['menu'])
def menucka(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    start = types.KeyboardButton('/start')
    create = types.KeyboardButton('/create_qr')

    markup.add(start, create)
    bot.send_message(message.chat.id, 'You have some buttons here', reply_markup=markup)

bot.infinity_polling()
