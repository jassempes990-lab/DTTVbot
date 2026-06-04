import telebot
import requests
import os
from flask import Flask
from threading import Thread
from telebot.types import BotCommand

# إعداد توكن البوت
BOT_TOKEN = "8418374521:AAHRYTwDL9BErCaTYqIwjVjZifZE5LkiC-w"
bot = telebot.TeleBot(BOT_TOKEN)

# معرف القناة للتحقق من الاشتراك
CHANNEL_ID = "@cr7_cris07"

# نص الاشتراك المنسق
sub_message = (
    "عذرا عزيزي المستخدم ⚠️\n\n"
    "يجب عليك الأشتراك في هذه القناة أولاً لأستعمال البوت:\n"
    "👉 https://t.me/cr7_cris07nn"
    "بعد الاشتراك، اضغط على زر /start من القائمة بالأسفل 🚀"
)

def set_bot_commands():
    try:
        commands = [
            BotCommand("start", "لتشغيل البوت والتحقق من الاشتراك 🚀")
        ]
        bot.set_my_commands(commands)
        print("تم تفعيل قائمة الأوامر (Menu) بنجاح!")
    except Exception as e:
        print(f"فشل في إعداد قائمة الأوامر: {e}")

def is_subscribed(user_id):
    try:
        status = bot.get_chat_member(CHANNEL_ID, user_id).status
        return status in ['member', 'administrator', 'creator']
    except:
        return False

@bot.message_handler(commands=['start'])
def send_welcome(message):
    if is_subscribed(message.from_user.id):
        bot.reply_to(message, "أهلاً بك في بوت DTTVbot! 🤖🎬\nأرسل لي رابط فيديو تيك توك وسأقوم بتحميله بدون علامة مائية فوراً.")
    else:
        bot.reply_to(message, sub_message)

@bot.message_handler(func=lambda message: True)
def handle_tiktok(message):
    if not is_subscribed(message.from_user.id):
        bot.reply_to(message, sub_message)
        return

    url = message.text
    if "tiktok.com" in url:
        status_msg = bot.reply_to(message, "جاري معالجة الفيديو... انتظر لحظة ⏳")
        try:
            # استخدام API قوي ومباشر (يعمل على ريندر بدون حظر وبدون بروكسي)
            api_url = f"https://api.tiklydown.eu.org/api/download?url={url}"
            response = requests.get(api_url, timeout=15).json()
            
            if "video" in response and "noWatermark" in response["video"]:
                video_url = response["video"]["noWatermark"]
                video_title = response.get("title", "TikTok Video")
                caption_text = f"🎬 {video_title}\n\n🤖 تم التحميل بواسطة: DTTVbot"
                
                # إرسال الفيديو وحذف رسالة الانتظار
                bot.send_video(message.chat.id, video_url, caption=caption_text)
                bot.send_message(message.chat.id, "لا شكر على واجب 🌹")
                bot.delete_message(message.chat.id, status_msg.message_id)
            else:
                bot.edit_message_text("عذراً، تعذر سحب هذا الفيديو. قد يكون الحساب خاصاً أو الرابط غير صحيح.", message.chat.id, status_msg.message_id)
        except Exception as e:
            bot.edit_message_text("حدث خطأ أثناء محاولة جلب الفيديو، يرجى إعادة المحاولة لاحقاً.", message.chat.id, status_msg.message_id)
            print(f"الخطأ الداخلي: {e}")
    else:
        bot.reply_to(message, "عذراً، يرجى إرسال رابط تيك توك صحيح فقط. ⚠️")

# كود إضافي مخصص لمنصة Render لإبقاء البوت حياً وشغالاً 24 ساعة بدون توقف
app = Flask('')
@app.route('/')
def home():
    return "البوت شغال 100%"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

if __name__ == "__main__":
    set_bot_commands()
    keep_alive()
    print("البوت يعمل الآن بنجاح على منصة Render...")
    bot.infinity_polling()
      
