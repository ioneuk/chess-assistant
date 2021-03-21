from os import getenv

import chess
from cairosvg import svg2png
from chess import svg
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
    fen = "r1bqkbnr/pppp2pp/2n2p2/1B2p3/4P3/5N2/PPPP1PPP/RNBQK2R w KQkq - 0 1"

    board = chess.Board(fen)
    boardsvg = svg.board(board=board)

    svg2png(bytestring=str(boardsvg), write_to='output.png')
    chat_id = update.message.chat.id
    bot.send_photo(chat_id,  photo=open('output.png', 'rb'), caption="Here is detected chessboard configuration")


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
