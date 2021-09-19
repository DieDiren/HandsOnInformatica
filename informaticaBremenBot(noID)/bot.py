import time
import datetime
import subprocess
import sensor_bme280
import os
from telegram.ext import Updater, InlineQueryHandler, CommandHandler, CallbackContext

# Create a bme280 sensor object
bme280 = sensor_bme280.BME280()


def check_id(bot, update):
    # Check if chat_id is valid.
    # The default is, that all telegram bots are public.
    # If you don't want that, you can restict it to certain message_ids
    # Every group chat, message, ... on telegram has its own id.
    chat_id = update.message.chat_id
    print(chat_id)
    ok = True
    if not (chat_id in [123]):
        ok = False
        update.message.reply_text(
            "Sorry, you don't have access to this bot. If you know the guys who created this, just contact them.")
    return ok


def greet(update, bot):
    # send a greeting
    if check_id(bot, update):
        update.message.reply_text("Hi! I'm the Informatica Feminale Bot.")


def bme(update, bot):
    # read and send bme values
    if check_id(bot, update):
        data = bme280.measure()
        update.message.reply_text("Temperature: " +str(data["Temperature"])
                                +", Humidity: " +str(data["RelHumidity"])
                                +", Pressure: " + str(data["Pressure"]))

def time(update, bot):
    # send current time
    if check_id(bot, update):
        update.message.reply_text(str(datetime.datetime.now()))


def main():
    # Main function of telegram bot

    # bot token obtained from botfather goes here
    updater = Updater('')
    dp = updater.dispatcher
    # add commands here
    dp.add_handler(CommandHandler('hi', greet))
    dp.add_handler(CommandHandler('time', time))
    dp.add_handler(CommandHandler('sense', bme))
    # start bot
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
