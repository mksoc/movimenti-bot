#!/usr/bin/python3

import config
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
import datetime

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="""
Ciao! Sono un bot che ti aiuta a registrare i tuoi movimenti. Usami per aggiungere le tue spese!

In questa prima versione, il massimo che posso fare è restituirti una stringa pronta da inviare al bot di IFTTT.

Per iniziare, mandami un messaggio con i seguenti campi (separati da virgole):
    - Categoria
    - Sottocategoria (optional, ma metti comunque la virgola)
    - Importo
""")

def spesa(update, context):
    # Get date in the format dd/mm/yy
    date = datetime.datetime.now()
    date = date.strftime('%d/%m/%y')

    # IFTTT bot expects a #spesa trigger, followed by the text input
    # '|||' separates the fields
    formatted_text = update.message.text.replace(',', '|||')
    ifttt_msg = f'#spesa {date} ||| {formatted_text}'

    # Send the reply
    context.bot.send_message(chat_id=update.effective_chat.id, text=ifttt_msg)

def main():
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(token=config.token, use_context=True)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Add handlers
    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)

    spesa_handler = MessageHandler(Filters.text & (~Filters.command), spesa)
    dispatcher.add_handler(spesa_handler)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()

if __name__ == '__main__':
    main()