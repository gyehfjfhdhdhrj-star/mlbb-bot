import os
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters
from groq import Groq
from flask import Flask
from threading import Thread

# API Tokens များ
TELEGRAM_BOT_TOKEN = "8892803898:AAGRuboJKkD9gTk9v3tYm-DnG3szsNNWOWY"
GROQ_API_KEY = "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"

client = Groq(api_key=GROQ_API_KEY)

# AI ရဲ့ စရိုက်နှင့် တာဝန်သတ်မှတ်ချက်
SYSTEM_PROMPT = """
You are a helpful customer service AI for a Mobile Legends: Bang Bang (MLBB) account trading business. 
Your job is to answer customer inquiries professionally about buying and selling MLBB accounts, skin prices, 
safe transactions (MM/Middleman service), payment methods (Kpay, Wave, KBZ), and account details (Emblem, Win rate, Skins).
Be polite, clear, and helpful in Burmese.
"""

# Telegram ကနေ စာလာပို့ရင် ဖြေကြားပေးမယ့် Function
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    try:
        chat_completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_message}
            ]
        )
        bot_reply = chat_completion.choices[0].message.content
    except Exception as e:
        bot_reply = "တောင်းပန်ပါတယ်၊ လက်တလော အခက်အခဲရှိနေလို့ ခဏနေမှ ထပ်မေးပေးပါ။"
    
    await update.message.reply_text(bot_reply)


# Render မှာ Port Error မတက်အောင် ယာယီ Web Server ထောင်ခြင်း (Flask)
app = Flask('')

@app.route('/')
def home():
    return "Bot is running!"

def run():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run)
    t.start()


# Main Program စတင်ရာနေရာ
if __name__ == '__main__':
    # ၁။ Flask ဝဘ်ဆာဗာကို Background မှာ စတင်ရန်
    keep_alive()
    print("Web server started...")

    # ၂။ Telegram Bot ကို စတင်ရန်
    print("MLBB Trading Bot is running...")
    application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    
    application.run_polling()
