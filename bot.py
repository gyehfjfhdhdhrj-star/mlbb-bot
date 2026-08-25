import os
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters
from groq import Groq
from flask import Flask
from threading import Thread

# API Tokens များ
TELEGRAM_BOT_TOKEN = "8892803898:AAEGRi8Uf9SGtFAVL5KYeeZ1KNNbdUuWTo4"
GROQ_API_KEY = "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"

client = Groq(api_key=GROQ_API_KEY)

SYSTEM_PROMPT = """
You are a helpful customer service AI for a Mobile Legends: Bang Bang (MLBB) account trading business. 
Your job is to answer customer inquiries professionally about buying and selling MLBB accounts, skin prices, 
safe transactions (MM/Middleman service), payment methods (Kpay, Wave, KBZ), and account details (Emblem, Win rate, Skins).
Be polite, clear, and helpful in Burmese.
"""

# Telegram Bot စာလက်ခံဖြေကြားခြင်း
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    try:
        chat_completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",  # အလုပ်လုပ်တဲ့ Model အမှန်
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_message}
            ]
        )
        bot_reply = chat_completion.choices[0].message.content
    except Exception as e:
        bot_reply = f"Error ဖြစ်နေပါသည်: {str(e)}"
    
    await update.message.reply_text(bot_reply)

# Render Port Error မတက်အောင် ယာယီ Flask Server ထောင်ခြင်း
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

# Main Program (Polling ကို Background Thread မှာ သီးသန့် run ခြင်းဖြင့် Conflict ရှင်းခြင်း)
def run_bot():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    
    # drop_pending_updates=True က အရင်က ပိတ်မိနေတဲ့ Conflict များကို ရှင်းပစ်ပါလိမ့်မည်
    application.run_polling(drop_pending_updates=True)

if __name__ == '__main__':
    # ၁။ Flask ကို စတင်ရန်
    keep_alive()
    print("Web server started...")

    # ၂။ Telegram Bot ကို သီးသန့် Thread ဖြင့် စတင်ရန်
    print("MLBB Trading Bot is running...")
    bot_thread = Thread(target=run_bot)
    bot_thread.start()
