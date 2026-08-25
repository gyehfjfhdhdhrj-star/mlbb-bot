async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    try:
        chat_completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",  # Model နာမည်ကို ဒါလေးနဲ့ စမ်းပါ။
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_message}
            ]
        )
        bot_reply = chat_completion.choices[0].message.content
    except Exception as e:
        # ဘာ Error တက်နေလဲ Telegram ထဲမှာ ပေါ်လာအောင် လုပ်ခြင်း
        bot_reply = f"Error ဖြစ်နေ습니다: {str(e)}"
    
    await update.message.reply_text(bot_reply)
