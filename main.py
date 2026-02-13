import requests
from telebot import TeleBot
from translate import Translator
from telebot import types

bot = TeleBot(token ='8246312790:AAHIFGJRux8F0ivXVaZG20Q41jLEcD_bhGk')
def fetch_facts():
    API = 'https://catfact.ninja/fact'
    try:
        data = requests.get(API).json()
        translator = Translator(to_lang='ru')
        ru = translator.translate(data['fact'])
        return {"en":data['fact'], 'ru':ru}

    except BaseException as e:
        print(f"got error while fetching cats {e}")

def send_to_admin(message):
    Admin_Id =6789932060
    user_text = message.text
    user_id = message.from_user.id
    username= message.from_user.username

    text = f"""
    📩  Новое сообшение в поддержку
    
    Username: @{username}
    ID: {user_id}

    Сообшение:
    {user_text}
    """

@bot.message_handler(commands=['start'])
def start(message):
    chat_id = message.chat.id
    keyboard = types.InlineKeyboardMarkup()
    btn_ru = types.InlineKeyboardButton(text='in Russian', callback_data='ru')
    btn_eng = types.InlineKeyboardButton(text='На английском  ', callback_data='eng')
    btn_support = types.InlineKeyboardButton(text='Написать в поддержку',
    callback_data='support')
    keyboard.add(btn_eng, btn_ru, btn_support)
    bot.send_message(chat_id, 'Получить Фак о кошках', reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: call.data == 'eng')
def btn_eng(call):
    message = call.message
    chat_id = message.chat.id
    facts = fetch_facts()
    bot.send_message(chat_id, facts['en'])

@bot.callback_query_handler(func=lambda call: call.data == 'ru')
def btn_ru(call):
    message = call.message
    chat_id = message.chat.id
    facts = fetch_facts()
    bot.send_message(chat_id, facts['ru'])

@bot.callback_query_handler(func=lambda call: call.data == 'support')
def btn_ru(call):
    message = call.message
    chat_id = message.chat.id
    facts = fetch_facts()
    bot.send_message(chat_id, facts['ru'])

bot.infinity_polling()
