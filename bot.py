import os
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

# ===== Environment variables =====
BOT_TOKEN = os.getenv("BOT_TOKEN")
SOURCE_CHAT_ID = int(os.getenv("SOURCE_CHAT_ID"))   # e.g. -1002552543046
DEST_CHAT_ID = int(os.getenv("DEST_CHAT_ID"))       # e.g. -1009876543210
TOPIC_ID = int(os.getenv("TOPIC_ID"))               # e.g. 75
KOYEB_URL = os.getenv("KOYEB_URL")                  # e.g. https://your-app.koyeb.app

async def forward_from_topic(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message:
        return
    
    # DEBUG: print all message info to logs
    print("DEBUG — Chat ID:", update.message.chat.id)
    print("DEBUG — Thread ID:", update.message.message_thread_id)
    print("DEBUG — Text:", update.message.text)
    
    # Filter only from the source group
    if update.message.chat.id != SOURCE_CHAT_ID:
        print("SKIPPED — Wrong chat ID")
        return

    # Filter only the specific topic/thread
    if update.message.message_thread_id != TOPIC_ID:
        print("SKIPPED — Wrong topic ID")
        return

    # Forward without showing "Forwarded from"
    try:
        if update.message.text:
            await context.bot.send_message(DEST_CHAT_ID, update.message.text)
        elif update.message.photo:
            await context.bot.send_photo(DEST_CHAT_ID, photo=update.message.photo[-1].file_id, caption=update.message.caption)
        elif update.message.video:
            await context.bot.send_video(DEST_CHAT_ID, video=update.message.video.file_id, caption=update.message.caption)
        elif update.message.audio:
            await context.bot.send_audio(DEST_CHAT_ID, audio=update.message.audio.file_id, caption=update.message.caption)
        elif update.message.document:
            await context.bot.send_document(DEST_CHAT_ID, document=update.message.document.file_id, caption=update.message.caption)
        print("FORWARDED successfully")
    except Exception as e:
        print("ERROR forwarding:", e)

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(MessageHandler(filters.ALL, forward_from_topic))

if __name__ == "__main__":
    app.run_webhook(
        listen="0.0.0.0",
        port=int(os.getenv("PORT", "8080")),
        url_path=BOT_TOKEN,
        webhook_url=f"{KOYEB_URL}/{BOT_TOKEN}"
    )
