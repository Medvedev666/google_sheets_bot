from telegram.ext import (
    CommandHandler, 
    MessageHandler, 
    filters, 
    CallbackQueryHandler,
    ConversationHandler
)

from config.converstation import function_map, cancel


# converstation
def make_handler(value):
    entry_points=[CallbackQueryHandler(function_map[value][0], pattern=f'^{value}$')]
    states={
        function_map[value][2]: [MessageHandler(filters.TEXT & ~filters.COMMAND, function_map[value][1])],
    }
    return entry_points, states


def create_conversation_handler(handler_name):
    entry_points, states = make_handler(handler_name)
    return ConversationHandler(
        entry_points=entry_points, states=states,
        fallbacks=[CommandHandler('cancel', cancel)]
    )