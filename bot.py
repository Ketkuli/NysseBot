# coding: utf-8
import requests
from os import environ
from dotenv import load_dotenv

from telegram import (
  Update,
) 
from telegram.ext import (
  CallbackContext,
  CommandHandler,
  Filters,
  MessageHandler,
  Updater,
)

# Loads .env file to environ, after that we can read the variables from .env
load_dotenv()

TG_TOKEN = environ['TG_TOKEN']


# -----------------------------------------------------------------------------
# Utils

def update_get_ids(update: Update):
  """Return chat_id, user_id and message_id if they exist."""
  chat_id = update.effective_chat.id
  user_id = update.effective_user.id
  message_id = update.effective_message.message_id

  return chat_id, user_id, message_id


# -----------------------------------------------------------------------------
# Command and message handlers

# Update documentation: https://docs.python-telegram-bot.org/en/latest/telegram.update.html
# CallbackContext documentation: https://docs.python-telegram-bot.org/en/latest/telegram.ext.callbackcontext.html

def start(update: Update, context: CallbackContext):
  msg = 'Hei, olen NysseBOT, anna minulle komennoksi /kettu'
  update.message.reply_html(msg)

def help(update: Update, context: CallbackContext):
  msg = '/kettu satunnaista kettukuvaa varten\n/leirintakatu seuraavien bussien saapumisaikatauluja varten'
  update.message.reply_html(msg)

# Simple API request to get fox pictures
def get_fox(update: Update, context: CallbackContext):

  response = requests.get("https://randomfox.ca/floof")
  fox = response.json()

  update.message.reply_photo(fox['image'])

# Simple API request and not so simple data stuff
def get_schedule(update: Update, context: CallbackContext):
  response = requests.get("http://data.itsfactory.fi/journeys/api/1/stop-monitoring?stops=2519")
  received = response.json()
  timetable = received['body']

  msg = f"Seuraavat bussit ovat:\n{timetable['2519'][0]['lineRef']}: {timetable['2519'][0]['call']['aimedArrivalTime']}\n{timetable['2519'][1]['lineRef']}: {timetable['2519'][1]['call']['aimedArrivalTime']}"
  update.message.reply_text(msg)

  # No argument?
#  if (len(context.args) == 0):
#    update.message.reply_text('No text given after the command.')
#    return

#  word = context.args[0].lower()

  # Example of logging to terminal and formatting a string programmatically
#  print(f'Example command args: {context.args}, first arg lowercased: {word}')

#  update.message.reply_text(f'The first word after the command was {word}.')

def message_handler(update: Update, context: CallbackContext):
  # Get chat id and user id, discard message id that is also returned by the function
  chat_id, user_id, _ = update_get_ids(update)
  
  msg = f'The message was sent to chat {chat_id} by user {user_id}.'

  update.message.reply_text(msg)


# -----------------------------------------------------------------------------
# Main loop

def main():
  updater = Updater(TG_TOKEN, use_context=True)
  
  # Add handlers to commands and messages
  dp = updater.dispatcher

  dp.add_handler(CommandHandler("start", start))
  dp.add_handler(CommandHandler("help", help))
  dp.add_handler(CommandHandler("kettu", get_fox))
  dp.add_handler(CommandHandler("leirintakatu", get_schedule))
  dp.add_handler(MessageHandler(Filters.text, message_handler))

  # Poll for new messages and commands every second
  updater.start_polling(poll_interval=1.0)


main()
