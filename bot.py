import os
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters
from groq import Groq
from flask import Flask, request

TELEGRAM_BOT_TOKEN = "8892803898:AAEGRi8Uf9SGtFAVL5KYeeZ1KNNbdUuWTo4"
GROQ_API_KEY = "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"

client = Groq(api_key=GROQ_API_KEY)

SYSTEM_PROMPT = """
You are a helpful customer service AI for a Mobile Legends: Bang Bang (MLBB) account trading business. 
Your job is to answer customer inquiries professionally about buying and selling MLBB accounts, skin prices, 
safe transactions (MM/Middleman service), payment methods (Kpay, Wave, KBZ), and account details (Emblem, Win rate, Skins).
Be polite, clear, and helpful in Burmese.
"""

app = Flask('')

# Telegram Bot Application ကို တစ်ခါတည်း တည်ဆောက်ခြင်း
application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

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

application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))

@app.route('/')
def home():
    return "Bot is running!"

# Render ကနေ Telegram Update များကို Webhook ဖြင့် လက်ခံရန်
@app.route(f'/{TELEGRAM_BOT_TOKEN}', methods=['POST'])
def webhook():
    update = Update.de_json(request.get_json(force=True), application.bot)
    application.update_queue.put(update)
    return 'ok'

if __name__ == '__main__':
    # Webhook ကို Render ရဲ့ URL နဲ့ ချိတ်ဆက်ခြင်း
    PORT = int(os.environ.get('PORT', 8080))
    URL = os.environ.get('RENDER_EXTERNAL_URL') # Render ကပေးတဲ့ URL ကို အလိုအလျောက်ယူမည်
    
    if URL:
        application.bot.set_webhook(url=f"{URL}/{TELEGRAM_BOT_TOKEN}")
        print(f"Webhook set to: {URL}/{TELEGRAM_BOT_TOKEN}")
    
    app.run(host='0.0.0.0', port=PORT)
