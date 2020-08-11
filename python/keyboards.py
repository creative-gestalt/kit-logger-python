from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove

state_keyboard = [['utah', 'texas', 'arizona'], ['Stop']]
kit_keyboard = [['10', '20', '30'], ['40', '50', '60'], ['70', '80', '90'], ['100']]
quick_start = [['/qstart']]
gen_new = [['No'], ['Yes']]
log_button = [['LOG'], ['Stop']]
state_keyboard = ReplyKeyboardMarkup(state_keyboard, one_time_keyboard=True, resize_keyboard=False)
kit_keyboard = ReplyKeyboardMarkup(kit_keyboard, one_time_keyboard=True)
quick_keyboard = ReplyKeyboardMarkup(quick_start, one_time_keyboard=True, resize_keyboard=True)
generate_keyboard = ReplyKeyboardMarkup(gen_new, one_time_keyboard=True, resize_keyboard=False)
log_button = ReplyKeyboardMarkup(log_button, one_time_keyboard=True, resize_keyboard=False)
remove_keyboard = ReplyKeyboardRemove(remove_keyboard=True)