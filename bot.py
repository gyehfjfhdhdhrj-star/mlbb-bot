import os
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters
from groq import Groq

TELEGRAM_BOT_TOKEN = "8892803898:AAGRuboJKkD9gTk9v3tYm-DnG3szsNNWOWY"
GROQ_API_KEY = "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"

client = Groq(api_key=GROQ_API_KEY)

SYSTEM_PROMPT = """
You are a helpful customer service AI for a Mobile Legends: Bang Bang (MLBB) account trading business. 
Your job is to answer customer inquiries professionally about buying and selling MLBB accounts, skin prices, 
safe transactions (MM/Middleman service), payment methods (Kpay, Wave, KBZ), and account details (Emblem, Win rate, Skins).
Be polite, clear, and helpful in Burmese.
"""

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

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    print("MLBB Trading Bot is running...")
    app.run_polling()