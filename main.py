from os import getenv

from stockfish import Stockfish
from telegram import bot, Bot, Update
from telegram.ext import Updater, run_async, MessageHandler, Filters, CommandHandler, CallbackContext

from pipeline import photo_to_fen
from utils.fen2png import Board, DrawImage

TOKEN = getenv("TOKEN")
WEBHOOK_URL = getenv("WEBHOOK_URL")

bot = Bot(TOKEN)
WORKING_DIR = "./"
SUFFIX = " w KQkq - 0 1"
stockfish_engine = Stockfish('./stockfish')

@run_async
def document_handler(update, context):
    print("")


@run_async
def message_handler(update, context):
    # bot.send_message(update.message.chat.id, "Send photo of the chess board")
    pass


@run_async
def photo_handler(update: Update, context: CallbackContext):
    photo = update.message.photo[-1]
    photo_id = photo.file_id
    photo_meta = bot.get_file(photo_id)
    photo_meta.download('image.jpg')

    fen = photo_to_fen('./image.jpg')

    context.user_data["fen"] = fen

    fen_parts = [None] * 6
    fen_parts[0] = fen[:-1]
    board = Board(fen_parts)
    boardGrid = board.board
    boardImg = DrawImage(boardGrid, 'png', './', 'result')
    boardImg.create()
    boardImg.to_image()

    stockfish_engine.set_fen_position(fen)

    chat_id = update.message.chat.id
    bot.send_photo(chat_id, photo=open('result.png', 'rb'), caption="Here is detected chessboard configuration")


def check_validity(update: Update, context: CallbackContext) -> None:
    if "fen" not in context.user_data:
        bot.send_message(update.message.chat.id, "Send photo of the chess board")
    else:
        fen = context.user_data["fen"]
        turn = context.args[0]
        stockfish_engine.set_fen_position(fen)
        validity = stockfish_engine.is_move_correct(turn)
        if validity is True:
            bot.send_message(update.message.chat.id, "Move is valid")
        elif validity is False:
            bot.send_message(update.message.chat.id, "Move is wrong")


def get_best_move(update: Update, context: CallbackContext) -> None:
    if "fen" not in context.user_data:
        bot.send_message(update.message.chat.id, "Send photo of the chess board")
    else:
        fen = context.user_data["fen"]
        stockfish_engine.set_fen_position(fen)
        best_move = stockfish_engine.get_best_move()

        bot.send_message(update.message.chat.id, best_move)



def start(update: Update, context: CallbackContext) -> None:
    bot.send_message(update.message.chat.id,
                     "Hi! Send me a photo of your chessboard, and do one of the following:\n1. Validate your turns\n2.Ask to suggestt a good move")


def main():
    updater = Updater(bot=bot, use_context=True)
    dispatcher = updater.dispatcher

    document = MessageHandler(Filters.document, document_handler)
    text = MessageHandler(Filters.text, message_handler)
    photo = MessageHandler(Filters.photo, photo_handler)
    doc = MessageHandler(Filters.document, photo_handler)
    check_turn = CommandHandler("check", check_validity)
    dispatcher.add_handler(check_turn)
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", start))
    dispatcher.add_handler(CommandHandler("get_best_move", get_best_move))

    dispatcher.add_handler(document)
    dispatcher.add_handler(text)
    dispatcher.add_handler(photo)
    dispatcher.add_handler(doc)

    updater.start_webhook(listen='127.0.0.1', port=8000, url_path="/")
    updater.bot.set_webhook(url=WEBHOOK_URL)
    updater.idle()


if __name__ == '__main__':
    main()
