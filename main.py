import logging
import os
from apis import audio, video
from telegram import KeyboardButton, __version__ as TG_VER

try:
    from telegram import __version_info__
except ImportError:
    __version_info__ = (0, 0, 0, 0, 0)

if __version_info__ < (20, 0, 0, "alpha", 1):
    raise RuntimeError(
        f"This example is not compatible with your current PTB version {TG_VER}. To view the "
        f"{TG_VER} version of this example, "
        f"visit https://docs.python-telegram-bot.org/en/v{TG_VER}/examples.html"
    )
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

social_link = "https://www.youtube.com"
social_link_ = "https://youtu.be/"

TOKEN = "5751525487:AAGdkIMLYq9PXKpxHzcYMaDSwr5AsKu4f4k"

ENTRY, MP3, VIDEO, MP3_HANDLER, VIDEO_HANDLER, END = range(6)


async def start(update: Update, context: ContextTypes):
    user = update.message.from_user
    """Starts the conversation and asks the user about their gender."""
    button = [[KeyboardButton(text="Video"), KeyboardButton(text="Mp3")]]
    reply_markup = ReplyKeyboardMarkup(
        button, resize_keyboard=True, one_time_keyboard=True
    )

    await update.message.reply_text(
        f"Hi {user.first_name}! I can help you to download videos and mp3 files from YouTube. To stop using the bot /stop",
        reply_markup=reply_markup,
    )

    return ENTRY


async def stop(update: Update, context: ContextTypes):
    """Stops the bot"""
    await update.message.reply_text(
        "Thank you for using the bot. \n For restart /start",
        reply_markup=ReplyKeyboardRemove(),
    )

    return ConversationHandler.END


async def mp3(update: Update, context: ContextTypes):
    """Accepts link and gives mp3 file back"""

    link = update.message.text
    context.user_data["choice"] = link

    await update.message.reply_text("Send me a link")

    return MP3


async def mp3_handler(update: Update, context: ContextTypes):

    link = update.message.text
    context.user_data["choice"] = link

    if social_link in link or social_link_ in link:
        await update.message.reply_text("Be patient! Downloading...")

        response = await audio(link)

        if response:
            await update.message.reply_audio(open("audio/audio.mp3", "rb"))
            await update.message.reply_text("/start for another request")

            os.remove("audio/audio.mp3")

        else:
            await update.message.reply_text("Please, try again later")

    else:
        await update.message.reply_text("Invalid input!")

    return MP3_HANDLER


async def mp4(update: Update, context: ContextTypes):
    """Accepts link and gives mp4 file back"""

    link = update.message.text
    context.user_data["choice"] = link

    await update.message.reply_text("Send me a link")

    return VIDEO


async def mp4_handler(update: Update, context: ContextTypes):

    link = update.message.text
    context.user_data["choice"] = link

    if social_link in link or social_link_ in link:
        await update.message.reply_text("Be patient! Downloading...")

        response = await video(link)

        if response:
            await update.message.reply_video(open("video/video.mp4", "rb"))
            await update.message.reply_text("/start for another request")

        else:
            await update.message.reply_text("Please, try again later")

    else:
        await update.message.reply_text("Invalid input")

    os.remove("video/video.mp4")

    return VIDEO_HANDLER


def main():
    """Run the bot"""

    application = Application.builder().token(TOKEN).build()
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            ENTRY: [
                MessageHandler(filters.Regex("^Mp3$"), mp3),
                MessageHandler(filters.Regex("^Video$"), mp4),
                CommandHandler("start", start),
                CommandHandler("stop", stop),
            ],
            MP3: [MessageHandler(filters.TEXT & ~filters.COMMAND, mp3_handler)],
            VIDEO: [MessageHandler(filters.TEXT & ~filters.COMMAND, mp4_handler)],
        },
        fallbacks=([CommandHandler("stop", stop)],),
    )

    application.add_handler(conv_handler)

    application.run_polling()


if __name__ == "__main__":
    main()
