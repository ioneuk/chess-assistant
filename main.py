from os import getenv

from telegram import bot, Bot
from telegram.ext import Updater, run_async, MessageHandler, Filters

from detect import detection_and_classification

TOKEN = getenv("TOKEN")
WEBHOOK_URL = getenv("WEBHOOK_URL")

bot = Bot(TOKEN)
WORKING_DIR = "./"


@run_async
def document_handler(update, context):
    print("")


@run_async
def message_handler(update, context):
    bot.send_message(update.message.chat.id, "Send photo of the chess board")


@run_async
def photo_handler(update, context):
    photo = update.message.photo[-1]
    photo_id = photo.file_id
    photo_meta = bot.get_file(photo_id)
    photo_meta.download('image.jpg')

    result = detection_and_classification("./")
    print(result)


def main():
    updater = Updater(bot=bot, use_context=True)
    dispatcher = updater.dispatcher

    document = MessageHandler(Filters.document, document_handler)
    text = MessageHandler(Filters.text, message_handler)
    photo = MessageHandler(Filters.photo, photo_handler)
    doc = MessageHandler(Filters.document, photo_handler)
    dispatcher.add_handler(document)
    dispatcher.add_handler(text)
    dispatcher.add_handler(photo)
    dispatcher.add_handler(doc)

    updater.start_webhook(listen='127.0.0.1', port=8000, url_path="/")
    updater.bot.set_webhook(url=WEBHOOK_URL)
    updater.idle()


if __name__ == '__main__':
    main()
