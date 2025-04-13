import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import yt_dlp

# Paste your NEW token below
BOT_TOKEN = "PASTE_YOUR_NEW_TOKEN_HERE"

# Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Welcome to LUHAR_YT_DOWNLOADER_bot!\n\n"
        "Send /download <YouTube Playlist URL> to begin downloading audio tracks.\n\n"
        "Example:\n/download https://youtube.com/playlist?list=YOUR_PLAYLIST_ID"
    )

# Download command
async def download(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("❌ Please provide a playlist URL.\nExample:\n/download https://youtube.com/playlist?list=...")
        return

    url = context.args[0]
    user_id = str(update.effective_user.id)
    download_path = f"downloads/{user_id}/"

    os.makedirs(download_path, exist_ok=True)

    await update.message.reply_text("📥 Downloading your playlist… please wait...")

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': f'{download_path}%(title)s.%(ext)s',
        'quiet': True,
        'ignoreerrors': True,
        'extractaudio': True,
        'audioformat': 'mp3'
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        files = os.listdir(download_path)
        if not files:
            await update.message.reply_text("❌ Failed to download or find files.")
            return

        for i, file in enumerate(files[:5]):  # Limit to 5 files max
            with open(os.path.join(download_path, file), 'rb') as f:
                await update.message.reply_document(f)

        if len(files) > 5:
            await update.message.reply_text("⚠️ Only first 5 files sent to avoid Telegram limits.")

    except Exception as e:
        await update.message.reply_text(f"❌ Error: {e}")

# Run the bot
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("download", download))

    print("✅ LUHAR_YT_DOWNLOADER_bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
