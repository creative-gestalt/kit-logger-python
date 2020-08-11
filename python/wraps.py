from telegram.ext import ConversationHandler
from python import keyboards
from functools import wraps


def send_action(action):
    """Sends `action` while processing func command."""
    def decorator(func):
        @wraps(func)
        def command_func(update, context, *args, **kwargs):
            context.bot.send_chat_action(chat_id=update.effective_message.chat_id, action=action)
            return func(update, context, *args, **kwargs)
        return command_func
    return decorator


def busy_reply(user):
    """Stops other users from starting bot when a user is active"""
    def decorator(func):
        @wraps(func)
        def command_func(update, context, *args, **kwargs):
            if user is not None:
                update.message.reply_text('Someone is using the logger, try again later.',
                                          reply_markup=keyboards.quick_keyboard)
                return ConversationHandler.END
            return func(update, context, *args, **kwargs)
        return command_func
    return decorator

