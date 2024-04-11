import os
import re
import sys
import datetime

import requests
from telegram import Update, Message, Bot
from telegram.ext import Application, Updater, CommandHandler, MessageHandler, filters

import utils

from api import Wayne


async def echo(update: Update, context):
    msg: Message = update.message

    text = update.message.text
    chat_id = update.effective_chat.id

    bot = context.bot

    while True:
        wayne = Wayne()
        appts = wayne.get_appointments()
        if appts["status"] == "ok":
            for appt in appts:
                await msg.reply_text(f"{appt['datetime']} - {appt['status']}")
        else:
            await msg.reply_text(f"Still nothing")
        return


def main():
    """Start the bot."""
    BOT_TOKEN = os.getenv("TG_TOKEN")

    print("Stating")
    dp = Application.builder().token(BOT_TOKEN).build()

    dp.add_handler(MessageHandler(filters.TEXT, echo))

    # Start the Bot
    DEBUG = True if os.getenv("DEBUG") else False
    if DEBUG:
        dp.run_polling(allowed_updates=Update.ALL_TYPES)
        # updater.start_polling()
        # Run the bot until you press Ctrl-C or the process receives SIGINT,
        # SIGTERM or SIGABRT. This should be used most of the time, since
        # start_polling() is non-blocking and will stop the bot gracefully.
        # updater.idle()
    else:
        logger.info('Starting bot in production webhook mode')
        HOST_URL = os.environ.get("HOST_URL")
        if HOST_URL is None:
            logger.critical('HOST URL is not set!')
            sys.exit(-1)
        updater.start_webhook(listen="0.0.0.0",
                              port='8443',
                              url_path=BOT_TOKEN)
        updater.bot.set_webhook("https://{}/{}".format(HOST_URL, BOT_TOKEN))


if __name__ == '__main__':
    main()
