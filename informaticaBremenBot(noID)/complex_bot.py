# Parts are taken from:
# https://github.com/python-telegram-bot/python-telegram-bot/blob/master/examples/echobot.py

import time
import datetime
import subprocess
import sensor_bme280
import os
import random
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import Updater, InlineQueryHandler, CommandHandler, CallbackContext, MessageHandler, Filters, ConversationHandler

# Create a bme280 sensor object
bme280 = sensor_bme280.BME280()
main_chat_id = 123
FUNFACTS, TONGUE_TWIST = range(2)

def check_id(context, update):
    # Check if chat_id is valid.
    # The default is, that all telegram bots are public.
    # If you don't want that, you can restict it to certain message_ids
    # Every group chat, message, ... on telegram has its own id.
    chat_id = update.message.chat_id
    print(chat_id)
    ok = True
    if not (chat_id in [main_chat_id]):
        ok = False
        update.message.reply_text(
            "Sorry, you don't have access to this bot. If you know the guys who created this, just contact them.")
    return ok

def greet(update, context):
    # send a greeting
    if check_id(context, update):
        update.message.reply_text("Hi! I'm the Informatica Feminale Bot.")


def bme(update, context):
    # read and send bme values
    if check_id(context, update):
        data = bme280.measure()
        update.message.reply_text("Temperature: " +str(data["Temperature"])
                                +", Humidity: " +str(data["RelHumidity"])
                                +", Pressure: " + str(data["Pressure"]))

def time(update, context):
    # send current time
    if check_id(context, update):
        update.message.reply_text(str(datetime.datetime.now()))

def echo(update, context):
    """Echo the user message."""
    update.message.reply_text(update.message.text)

def alarm_10(job_context):
    job_context.bot.send_message(chat_id=job_context.job.context,
                             text='Drrrrrrring!!! 10 seconds passed.')

def set_alarm_10(update, context):
    chat_id = update.message.chat_id
    job = context.job_queue
    job.run_once(alarm_10, 10, context=chat_id, name=str(chat_id))

def good_morning(job_context):
    job_context.bot.send_message(chat_id=main_chat_id,
                             text="Good morning. An other day of Informatica summer university is starting :)")

def funfact_helper():
    facts = ["'Buffalo buffalo Buffalo buffalo buffalo buffalo Buffalo buffalo' is a grammatically correct sentence in English",
    "'James while John had had had had had had had had had had had a better effect on the teacher' is an English sentence used to demonstrate lexical ambiguity and the necessity of punctuation.",
    "The Ténéré Tree (French: L'Arbre du Ténéré) was a solitary acacia, of either Acacia raddiana or Acacia tortilis, that was once considered the most isolated tree on Earth[3]—the only one for over 150 kilometres (93 mi). It was knocked down in 1973 by a truck driver.",
    "Anatoli Petrovich Bugorski (Russian: Анатолий Петрович Бугорский), born 25 June 1942, is a retired Russian particle physicist. He is known for surviving a radiation accident in 1978, when a high-energy proton beam from a particle accelerator passed through his brain.",
    "Aachenosaurus is a dubious genus of prehistoric plant from the Late Cretaceous (Santonian-Campanian). It was named based solely on fossilized fragments of material that were originally thought to be jaw fragments from a duck-billed dinosaur (a hadrosaur). However, the fossils turned out to be petrified wood, to the great embarrassment of the discoverer.",
    "Though no standard exists, numerous calendars and other timekeeping approaches have been proposed for the planet Mars. The most commonly seen in scientific literature denotes the time of year as the number of degrees from the northern vernal equinox, and increasingly there is use of numbering the Martian years beginning at the equinox that occurred April 11, 1955.",
    "Adactylidium is a genus of mites known for its unusual life cycle.[1] The pregnant female mite feeds upon a single egg of a thrips, growing five to eight female offspring and one male in her body. The single male mite mates with all the daughters when they are still in the mother."]
    random_int = random.randint(0, len(facts)-1)
    return(facts[random_int])

def tongue_twist_helper():
    twists = ["The seething sea ceaseth and thus the seething sea sufficeth us.",
                "She sells sea-shells by the sea-shore. The shells she sells are sea-shells, I'm sure. For if she sells sea-shells by the sea-shore Then I'm sure she sells sea-shore shells.",
                "Peter Piper picked a peck of pickled peppers - A peck of pickled peppers Peter Piper picked - If Peter Piper picked a peck of pickled peppers - Where's the peck of pickled peppers Peter Piper picked ",
                "Betty Botter bought a bit of butter. -The butter Betty Botter bought was a bit bitter - And made her batter bitter. - But a bit of better butter makes better batter. - So Betty Botter bought a bit of better butter - Making Betty Botter's bitter batter better ",
                "How much wood would a woodchuck chuck - if a woodchuck could chuck wood? - A woodchuck would chuck all the wood he could chuck - if a woodchuck would chuck wood.",
                "Shep Schwab shopped at Scott's Schnapps shop; One shot of Scott's Schnapps stopped Schwab's watch. "]
    random_int = random.randint(0, len(twists)-1)
    return(twists[random_int])

def start_conversation(update, context):
    reply_keyboard = [['Yes', 'No']]

    update.message.reply_text(
        'Are you bored? '
        'Do you want me to tell you some random fact?',
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder='Random facts?'
        ),
    )

    return FUNFACTS

def more_funfacts(update, context):
    if update.message.text.lower() in ['yes', 'y', 'Yes']:
        reply_keyboard = [['Yes', 'No']]
        fact = funfact_helper()
        update.message.reply_text(fact)
        update.message.reply_text(
            'Do you want more facts?',
            reply_markup=ReplyKeyboardMarkup(
                reply_keyboard, one_time_keyboard=True, input_field_placeholder='Random facts?'
            ),
        )
        return FUNFACTS
    else:
        reply_keyboard = [['Yes', 'No']]
        update.message.reply_text("Ok, should I give you a random tongue twist instead?",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder='Random tongue twist?'
        ),)
        return TONGUE_TWIST

def tongue_twist(update, context):
    if update.message.text.lower() in ['yes', 'y', 'Yes']:
        reply_keyboard = [['Yes', 'No']]
        update.message.reply_text(tongue_twist_helper())
        update.message.reply_text(
            'Do you want another tongue twist?',
            reply_markup=ReplyKeyboardMarkup(
                reply_keyboard, one_time_keyboard=True, input_field_placeholder='Random tongue twist?'
            ),
        )
        return TONGUE_TWIST
    else:
        return bye(update, context)

def bye(update, context):
    update.message.reply_text(
        'Bye! Have a nice day. Hope you are not bored anymore', reply_markup=ReplyKeyboardRemove()
    )
    return ConversationHandler.END


def main():
    # Main function of telegram bot

    # bot token obtained from botfather goes here
    updater = Updater('')
    j = updater.job_queue
    dp = updater.dispatcher
    # add commands here
    dp.add_handler(CommandHandler('hi', greet))
    dp.add_handler(CommandHandler('time', time))
    dp.add_handler(CommandHandler('sense', bme))
    dp.add_handler(CommandHandler('alarm_10', set_alarm_10))

    # on non command i.e message - echo the message on Telegram
    #dp.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    # run_daily days=(2,)
    j.run_daily(good_morning, time = datetime.time(hour = 8, minute = 0, second = 0))

     # Add conversation handler
    conv_handler = ConversationHandler(
        entry_points=[MessageHandler(Filters.regex('.*boring.*'), start_conversation)],
        states={
            FUNFACTS: [MessageHandler(Filters.regex('^(y|yes|Yes|n|no|No)$'), more_funfacts)],
            TONGUE_TWIST: [MessageHandler(Filters.regex('^(y|yes|Yes|n|no|No)$'), tongue_twist)]
        },
        fallbacks=[MessageHandler(~Filters.regex('^(y|yes|Yes|n|no|No)$'), bye), CommandHandler('cancel', bye)],
    )

    dp.add_handler(conv_handler)

    # start bot
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
