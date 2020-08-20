from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler
from python import functions, number_generator, keyboards
from telegram import ReplyKeyboardMarkup, ChatAction
from kit_logger import KitLogger
from python import wraps, logger
from python import globals as g
from pathlib import Path
import configparser
import datetime
import csv
import os

print = logger.print_and_log
config = configparser.ConfigParser()
config.read('config.ini')
send_busy_reply = wraps.busy_reply(g.user)
send_typing_action = wraps.send_action(ChatAction.TYPING)

# Wraps functions as states
STATE, CITY, ZIP_CODE, KIT_COUNT, NUMBERS, CREDS, GROUP, GENERATE, LOG = range(9)

# Telegram start message for user
with open('./bot-splash.txt', 'r') as f:
    bot_splash = f.read()


@send_busy_reply
@send_typing_action
def start(update, context):
    """Starts bot with splash message"""
    g.user = update.message.from_user.first_name
    print(g.user)
    context.bot.send_message(chat_id=68162307, text='{} started a run.'.format(g.user))
    update.message.reply_text('{}, %s'.format(
        update.message.from_user.first_name) % bot_splash, reply_markup=keyboards.state_keyboard)
    return STATE  # <-- this is what will receive the next user input


@send_busy_reply
@send_typing_action
def quick_start(update, context):
    """Starts bot the quick way
       Requests `state` from user
    """
    g.user = update.message.from_user.first_name
    print(g.user)
    context.bot.send_message(chat_id=68162307, text='{} started a run.'.format(g.user))
    update.message.reply_text('What state?', reply_markup=keyboards.state_keyboard)
    return STATE


def update_cities():
    """Dynamically gets city list"""
    cities_temp = functions.create_dict_and_filter(Path(f'./states/{g.state}/city-dictionary.txt'))
    cities = [cities_temp[x:x + 3] for x in range(0, len(cities_temp), 3)]
    return cities


def update_zip_list(city):
    """Dynamically gets zip code list"""
    state_dict = functions.create_dict(Path(f'./states/{g.state}/city-dictionary.txt'))
    zip_temp = functions.get_keys_by_value(state_dict, city)
    g.local_zips = f'./states/{g.state}/city-dictionary.txt'
    zip_codes = [zip_temp[x:x + 4] for x in range(0, len(zip_temp), 4)]
    return zip_codes


@send_typing_action
def get_state(update, context):
    """Gets `state` from user
       Requests `city` from user
    """
    g.state = update.message.text
    cities = update_cities()
    city_keyboard = ReplyKeyboardMarkup(cities, one_time_keyboard=True, resize_keyboard=False)
    update.message.reply_text('What city?', reply_markup=city_keyboard)
    return CITY


@send_typing_action
def get_city(update, context):
    """Gets `city` from user
       Requests `zip code` from user
    """
    city = update.message.text
    zip_codes = update_zip_list(city)
    zip_codes_keyboard = ReplyKeyboardMarkup(zip_codes, one_time_keyboard=True, resize_keyboard=False)
    update.message.reply_text('What zip code?', reply_markup=zip_codes_keyboard)
    return ZIP_CODE


@send_typing_action
def get_zip_code(update, context):
    """Gets `zip code` from user
       Requests `kits` from user
    """
    g.zip_code = update.message.text
    update.message.reply_text('How many kits?', reply_markup=keyboards.kit_keyboard)
    return NUMBERS


@send_typing_action
def generate_new_numbers(update, context):
    """Asks user if they want to generate new member numbers"""
    g.kit_count = int(update.message.text)
    update.message.reply_text('Generate new numbers?', reply_markup=keyboards.generate_keyboard)
    return KIT_COUNT


@send_typing_action
def get_kit_count(update, context):
    """Checks if user files exist
       Gets `generate numbers` response from user

       If user files exist, sends confirmation message

       If user files do not exist, this requests:
       `email` and `password` from user
       `box range` from user
    """
    member_file = f'user_member_numbers/{g.user}/member_numbers.txt'
    print(f'Logging {g.kit_count} kits at {g.zip_code}')
    with open('user_data/users.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if row[0] == g.user:
                user_data = row
                g.email = user_data[1]
                g.password = user_data[2]
                g.group_number = user_data[3]
                if update.message.text == 'Yes':
                    update.message.reply_text(
                        'Send box range.\nExample:\n\n50015000-50015099')
                    return GENERATE
                if not os.stat(member_file).st_size == 0:
                    g.member_numbers = functions.read_and_append(member_file)
                    update.message.reply_text(
                        'Found files with necessary information.', reply_markup=keyboards.log_button)
                    return LOG
                else:
                    update.message.reply_text(
                        'None found. Send box range.\nExample:\n\n50015000-50015099')
                    return GENERATE
            else:
                update.message.reply_text(
                    'Send your email and password.\nExample:\n\n email@gmail.com pAsSworD$&')
                return CREDS


@send_typing_action
def get_creds(update, context):
    """Gets `credentials` from user
       Requests `group number` from user
    """
    creds = update.message.text
    (g.email, g.password) = creds.split()
    update.message.reply_text('Group number?')
    return GROUP


@send_typing_action
def get_group(update, context):
    """Gets `group number` from user
       Requests `box range` from user
    """
    g.group_number = update.message.text
    with open('user_data/users.csv', 'r') as file:
        reader = csv.reader(file)
        users = []
        for row in reader:
            users.append(row[0])
        if g.user not in users:
            with open('user_data/users.csv', 'a', newline='') as nf:
                writer = csv.writer(nf)
                writer.writerow([g.user, g.email, g.password, g.group_number])
    update.message.reply_text('Send box range.\nExample:\n\n50015000-50015099')
    return GENERATE


@send_typing_action
def generate_numbers(update, context):
    """Generates `member numbers` from user input"""
    numbers = update.message.text
    print(numbers)
    (first_number, second_number) = numbers.split('-')
    if len(first_number) != len(second_number):
        update.message.reply_text('You may have entered extra digits, please send them again.')
        if second_number - first_number > 100:
            update.message.reply_text('You may have entered incorrect numbers, please send them again.')
            return GENERATE
        return GENERATE
    g.member_numbers = number_generator.generate_card_numbers(g.user, first_number, second_number)
    update.message.reply_text('Member numbers were generated', reply_markup=keyboards.log_button)
    return LOG


@send_typing_action
def begin_logging(update, context):
    """Executes kit_logger
       Ends conversation
    """
    update.message.reply_text('Spinning up logger session, results will be sent soon.',
                              reply_markup=keyboards.remove_keyboard)
    kit_logger = KitLogger(
        g.user,
        g.member_numbers,
        g.group_number,
        g.email,
        g.password,
        g.state,
        g.zip_code,
        g.kit_count,
        g.local_zips
    )
    time_start = datetime.datetime.now()
    result = kit_logger.activate()
    time_end = datetime.datetime.now() - time_start
    print(str(datetime.timedelta(seconds=round(time_end.seconds))))
    response = f'Results:\nKits logged: {str(result[0])}\nError: {str(result[1])}'
    context.bot.send_document(
        chat_id=update.message.chat_id,
        document=open('data/temp/location_data.txt', 'rb'))
    update.message.reply_text(response, reply_markup=keyboards.quick_keyboard)
    context.bot.send_message(chat_id=68162307, text=response)
    done(update, context)
    print(':>> Ended <<:')
    return ConversationHandler.END


def reset_data():
    """Resets global variables and clears temp file"""
    g.reset_globals()
    open('data/temp/location_data.txt', 'w').close()


def done(update, context):
    """Resets user data"""
    context.bot.send_message(chat_id=68162307, text='{}\'s run has ended.'.format(g.user))
    update.message.reply_text('All session data was cleared, see you later!')
    user_data = context.user_data
    user_data.clear()
    reset_data()


def stop(update, context):
    """Stops bot conversation and resets user data"""
    context.bot.send_message(chat_id=68162307, text='{}\'s run has ended using stop command.'.format(g.user))
    update.message.reply_text('Stopped the session.', reply_markup=keyboards.quick_keyboard)
    user_data = context.user_data
    user_data.clear()
    reset_data()
    print('User hit stop')
    return ConversationHandler.END


def main():
    print('>>BOT STARTED<<')
    updater = Updater(config['SECRET']['token'], use_context=True, workers=8)
    dp = updater.dispatcher
    end_handler = MessageHandler(Filters.regex('^Stop$'), stop)
    conv_handler = ConversationHandler(
        conversation_timeout=5 * 60,
        entry_points=[CommandHandler('start', start), CommandHandler('qstart', quick_start)],

        states={
            KIT_COUNT: [MessageHandler(Filters.regex('^(10|20|30|40|50|60|70|80|90|100|Yes|No)$'), get_kit_count)],
            STATE: [MessageHandler(Filters.regex('^(utah|texas|arizona)$'), get_state)],
            CITY: [MessageHandler(Filters.text, get_city)],
            ZIP_CODE: [MessageHandler(Filters.text, get_zip_code)],
            NUMBERS: [MessageHandler(Filters.text, generate_new_numbers)],
            CREDS: [MessageHandler(Filters.text, get_creds)],
            GROUP: [MessageHandler(Filters.text, get_group)],
            GENERATE: [MessageHandler(Filters.text, generate_numbers)],
            LOG: [MessageHandler(Filters.regex('^(LOG)$'), begin_logging)]
        },

        fallbacks=[end_handler]
    )
    dp.add_handler(conv_handler)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
