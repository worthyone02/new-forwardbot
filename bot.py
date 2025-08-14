import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
SOURCE_CHAT_ID = int(os.environ.get("SOURCE_CHAT_ID", "0"))
DEST_CHAT_ID = int(os.environ.get("DEST_CHAT_ID", "0"))
TOPIC_ID = int(os.environ.get("TOPIC_ID", "0"))
PORT = int(os.environ.get("PORT", 8080))

logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO)
log = logging.getLogger("relay")

async def relay(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message
    if not msg:
        return
    if msg.chat.id != SOURCE_CHAT_ID:
        return
    if msg.message_thread_id != TOPIC_ID:
        return

    caption = msg.caption or ""
    try:
        if msg.text:
            await context.bot.send_message(DEST_CHAT_ID, msg.text)
        elif msg.photo:
            await context.bot.send_photo(DEST_CHAT_ID, msg.photo[-1].file_id, caption=caption)
        elif msg.video:
            await context.bot.send_video(DEST_CHAT_ID, msg.video.file_id, caption=caption)
        elif msg.animation:
            await context.bot.send_animation(DEST_CHAT_ID, msg.animation.file_id, caption=caption)
        elif msg.audio:
            await context.bot.send_audio(DEST_CHAT_ID, msg.audio.file_id, caption=caption)
        elif msg.voice:
            await context.bot.send_voice(DEST_CHAT_ID, msg.voice.file_id, caption=caption)
        elif msg.document:
            await context.bot.send_document(DEST_CHAT_ID, msg.document.file_id, caption=caption)
        else:
            log.info("Message type not handled.")
    except Exception as e:
        log.error(f"Error relaying message: {e}")

def main():
    if not BOT_TOKEN:
        log.error("BOT_TOKEN is missing")
        raise SystemExit(1)

    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.ALL, relay))

    # Webhook setup
    url = f"https://{os.environ.get('KOYEB_APP_NAME')}.koyeb.app"  # Koyeb's public URL
    app.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        url_path=BOT_TOKEN,
        webhook_url=f"{url}/{BOT_TOKEN}"
    )

if __name__ == "__main__":
    main()
