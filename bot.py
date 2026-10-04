import os
import logging
BOT_TOKEN = os.getenv("BOT_TOKEN", "").strip()
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "").strip()
GROQ_MODEL = "llama-3.1-8b-instant"

SYSTEM_PROMPT = """
Ikaw ay auto-reply bot ni Edwin. Taglish ka sumagot, friendly, maikli lang max 2 sentences.
Nasa biyahe ka madalas. May emoji minsan.
"""

from telegram import Update
from telegram.ext import Application, MessageHandler, CommandHandler, ContextTypes, filters
from groq import Groq

logging.basicConfig(level=logging.INFO)
groq_client = Groq(api_key=GROQ_API_KEY) if GROQ_API_KEY else None

async def start(update, context):
    await update.message.reply_text("✅ AI Bot ON! Groq powered")

async def ai_reply(update, context):
    if not update.message or not update.message.text.startswith("/")==False and update.message.text.startswith("/"):
        return
    if update.message.text.startswith("/"):
        return
    user_msg = update.message.text
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
    try:
        if groq_client:
            res = groq_client.chat.completions.create(
                messages=[{"role":"system","content":SYSTEM_PROMPT},{"role":"user","content":user_msg}],
                model=GROQ_MODEL, max_tokens=150, temperature=0.7
            )
            reply = res.choices[0].message.content
        else:
            reply = "Nareceive ko message mo boss! Nasa biyahe lang ako, balikan kita agad 🙏"
    except:
        reply = "Busy lang boss, balikan kita agad 🙏"
    await update.message.reply_text(reply)

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, ai_reply))
    app.run_polling()

if __name__ == "__main__":
    main()