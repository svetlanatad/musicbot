import os
import logging
import yt_dlp
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import urllib.parse
import glob
import re

os.environ["IMAGEIO_FFMPEG_EXE"] = "/path/to/venv/ffmpeg"
os.environ["FFMPEG_BINARY"] = ".........^same"

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[
        logging.FileHandler("bot.log"),
        logging.StreamHandler()
    ]
)

TOKEN = '....my_token....'

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Hi, I am telegram bot that downloads music, send me a youtube link "
    )

async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Here is a list of the following commands\n")
    await update.message.reply_text("/start: try and see\n /howru: try and see\n example usage: https://yoututbelinkblablabla RezeIsBestWaifu for sure {[=&)*[&{])]) \n ...^will save it as: RezeIsBestWaifu_for_sure.mp3 \n created by a python noob, btw i hate python! ")

async def howru(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Oh, I am doing cheese, how about you?")



def cleanFilename(name):
    return re.sub(r'[^a-zA-Z0-9_\- ]+', '', name).strip().replace(" ", "_")



async def convert_to_mp3(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    parts = text.split(" ", 1)

    url = parts[0]
    custom_name = parts[1] if len(parts) > 1 else None
    logging.info(f"Received URL: {url}")
    clean_url = urllib.parse.urlsplit(url)._replace(query="").geturl()
    logging.info(f"Cleaned URL: {clean_url}")
    if "youtube.com" not in clean_url and "youtu.be" not in clean_url:
        await update.message.reply_text("Are you sure it's a youtube link?")
        return

    try:
        if not os.path.exists('downloads'):
            os.makedirs('downloads')

        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': 'downloads/%(id)s.%(ext)s',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'ffmpeg_location': '/path/to/venv/bin/ffmpeg',
            'quiet': False
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(clean_url, download=True)
            video_id = info.get("id", "")
            title = info.get("title", "audio")
        original_mp3 = f"downloads/{video_id}.mp3"
        if not os.path.exists(original_mp3):
            raise FileNotFoundError(f"Expected MP3 not found: {original_mp3}")

        safe_name = cleanFilename(custom_name or title)
        final_mp3 = f"downloads/{safe_name}.mp3"
        os.rename(original_mp3, final_mp3)
        logging.info(f"Renamed to: {final_mp3}")
        with open(final_mp3, 'rb') as audio_file:
            await context.bot.send_audio(chat_id=update.message.chat_id, audio=audio_file)

        os.remove(final_mp3)
        logging.info(f"Deleted temporary file: {final_mp3}")

    except Exception as e:
        logging.error(f"Error: {str(e)}")
        await update.message.reply_text(f"Oops! Something went wrong:\n{e}")

def main():
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("howru", howru))
    application.add_handler(CommandHandler("help", help))
    application.add_handler(MessageHandler(
        filters.Regex(r'^(https?\:\/\/)?(www\.)?(youtube\.com|youtu\.be)\/.+$'),
        convert_to_mp3
    ))

    application.run_polling()

if __name__ == '__main__':
    main()
