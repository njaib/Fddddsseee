import telebot
import requests
from gtts import gTTS
import speech_recognition as sr
import os


# ==========================
# تنظیمات - اطلاعات خودت را اینجا بگذار
# ==========================

BOT_TOKEN = "8942028679:AAFDCbBJhVioczUtlgD3B9gJbSVM2YVLz9o"

AI_API_KEY = "AQ.Ab8RN6IY9M8qPSa_1uJD7l2-jkCZa4ieRD2hiThlH6DTU3kLDA"


bot = telebot.TeleBot(BOT_TOKEN)



# ==========================
# ارتباط با هوش مصنوعی
# ==========================

def ask_ai(message):

    url = "https://api.openai.com/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {AI_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "gpt-4o-mini",
        "messages": [
            {
                "role": "user",
                "content": message
            }
        ]
    }


    response = requests.post(
        url,
        headers=headers,
        json=data
    )


    result = response.json()

    return result["choices"][0]["message"]["content"]



# ==========================
# شروع ربات
# ==========================

@bot.message_handler(commands=["start"])
def start(message):

    bot.reply_to(
        message,
        "سلام 👋\nمن ربات هوش مصنوعی هستم.\nمتن یا ویس بفرست."
    )



# ==========================
# پیام متنی
# ==========================

@bot.message_handler(content_types=["text"])
def text_ai(message):

    try:

        answer = ask_ai(message.text)

        bot.reply_to(
            message,
            answer
        )

    except:

        bot.reply_to(
            message,
            "خطا در اتصال به AI"
        )



# ==========================
# پیام صوتی
# ==========================

@bot.message_handler(content_types=["voice"])
def voice_ai(message):

    try:

        file = bot.get_file(
            message.voice.file_id
        )

        data = bot.download_file(
            file.file_path
        )


        with open("voice.ogg","wb") as f:
            f.write(data)



        # تبدیل صدا به متن

        r = sr.Recognizer()


        with sr.AudioFile("voice.ogg") as source:

            audio = r.record(source)

            text = r.recognize_google(
                audio,
                language="fa-IR"
            )



        answer = ask_ai(text)



        # ارسال متن جواب

        bot.send_message(
            message.chat.id,
            answer
        )



        # تبدیل جواب به صدا

        voice = gTTS(
            answer,
            lang="fa"
        )

        voice.save("answer.mp3")



        with open("answer.mp3","rb") as f:

            bot.send_voice(
                message.chat.id,
                f
            )


    except Exception as e:

        bot.reply_to(
            message,
            "مشکل در پردازش صدا"
        )




print("ربات روشن شد...")


bot.infinity_polling()