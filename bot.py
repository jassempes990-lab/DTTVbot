import telebot
import requests
from flask import Flask
from threading import Thread

# توكن البوت الخاص بك
TOKEN = "7334710403:AAH_18-4v-iS6VwXw8R1K_N_5hSAs_xOfc0"
bot = telebot.TeleBot(TOKEN)

# قناة الاشتراك الإجباري (بدون @)
CHANNEL_USERNAME = "u_p_6"

def is_subscribed(user_id):
    try:
        member = bot.get_chat_member(f"@{CHANNEL_USERNAME}", user_id)
        if member.status in ['creator', 'administrator', 'member']:
            return True
        return False
    except Exception as e:
        print(f"Error checking subscription: {e}")
        return True

@bot.message_handler(commands=['start'])
def welcome(message):
    if not is_subscribed(message.from_user.id):
        sub_message = f"⚠️ عذراً! يجب عليك الاشتراك في قناة البوت أولاً لتتمكن من استخدامه.\n\nاضغط هنا: @{CHANNEL_USERNAME}\n\nبعد الاشتراك، أرسل /start مرة أخرى."
        bot.reply_to(message, sub_message)
        return

    bot.reply_to(message, "أهلاً بك في بوت DTTVbot! 🤖🎬\nأرسل لي رابط فيديو تيك توك وسأقوم بتحميله بدون علامة مائية فوراً.")

@bot.message_handler(func=lambda message: True)
def handle_tiktok(message):
    if not is_subscribed(message.from_user.id):
        sub_message = f"⚠️ عذراً! يجب عليك الاشتراك في قناة البوت أولاً لتتمكن من استخدامه.\n\nاضغط هنا: @{CHANNEL_USERNAME}"
        bot.reply_to(message, sub_message)
        return

    url = message.text
    if "tiktok.com" in url:
        status_msg = bot.reply_to(message, "⏳ جاري معالجة الفيديو... انتظر لحظة")
        try:
            api_url = f"https://api.tiklydown.eu.org/api/download?url={url}"
            response = requests.get(api_url, timeout=15).json()

            if "video" in response and "noWatermark" in response["video"]:
                video_url = response["video"]["noWatermark"]
                video_title = response.get("title", "فيديو TikTok")
                caption_text = f"🎬 {video_title}\n\nتم التحميل بواسطة: @DTTVbot"
                
                bot.send_video(message.chat.id, video_url, caption=caption_text, reply_to_message_id=message.message_id)
                bot.delete_message(message.chat.id, status_msg.message_id)
            else:
                bot.edit_message_text("❌ لم نتمكن من جلب الفيديو، تأكد أن الحساب ليس خاصاً أو الرابط صحيح.", message.chat.id, status_msg.message_id)
        except Exception as e:
            bot.edit_message_text("❌ حدث خطأ أثناء محاولة جلب الفيديو، يرجى إعادة المحاولة لاحقاً.", message.chat.id, status_msg.message_id)
            print(f"Internal Error: {e}")
    else:
        bot.reply_to(message, "⚠️ عذراً، يرجى إرسال رابط تيك توك صحيح فقط.")

# كود إضافي مخصص لمنصة Render لإبقاء البوت حياً
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
    keep_alive()
    print("البوت بدأ العمل الآن بنجاح...")
    bot.infinity_polling()
