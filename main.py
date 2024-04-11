import os

from telegram import Update, Message
from telegram.ext import Application, MessageHandler, filters

from api import Wayne


async def echo(update: Update, context):
    msg: Message = update.message

    text = update.message.text
    chat_id = update.effective_chat.id

    bot = context.bot

    while True:
        wayne = Wayne()
        try:
            appts = wayne.get_appointments()
        except Exception as e:
            await msg.reply_text(f"{e}")
            return
        if appts["status"] == "ok":
            for appt in appts:
                await msg.reply_text(f"{appt['datetime']} - {appt['status']}")
        else:
            await msg.reply_text(f"Still not1hing")
        return


def main():
    """Start the bot."""
    BOT_TOKEN = os.getenv("TG_TOKEN")

    print("Stating")
    dp = Application.builder().token(BOT_TOKEN).build()

    dp.add_handler(MessageHandler(filters.TEXT, echo))

    # Start the Bot
    dp.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    main()
