from telegram import (
    InlineKeyboardButton, 
    InlineKeyboardMarkup, 
    KeyboardButton, 
    ReplyKeyboardMarkup
)





async def make_buttons(buttons_list):
    keyboard = []
    keyboard_second = []

    for button_text, callback_data in buttons_list:
        if 'http' in callback_data:
            button = InlineKeyboardButton(text=button_text, url=callback_data)
        elif 'Порекомендовать бот' in button_text:
            button = InlineKeyboardButton(text=button_text, switch_inline_query=callback_data)
        else:
            button = InlineKeyboardButton(text=button_text, callback_data=callback_data)
        keyboard_second.append(button)
        if callback_data == '#':
            keyboard.append(keyboard_second)
            keyboard_second = []
    keyboard.append(keyboard_second)
    reply_markup = InlineKeyboardMarkup(keyboard)
    return reply_markup





async def keyboard(button_text):
    keyboard = []
    row = []
    for button in button_text:
        if button == '#':
            if row:
                keyboard.append(row)
                row = []
        else:
            row.append(KeyboardButton(button))
    if row:
        keyboard.append(row)
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)





keys = ['table_article', 'quantity', 'description', 'info', 'comment']

async def check_user_data(context):
    for key in keys:
        if key not in context.user_data:
            context.user_data[key] = ''


async def clean_data(context):
    for key in keys:
        context.user_data[key] = ''
