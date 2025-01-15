from telegram import Update, ReplyKeyboardRemove
from telegram.ext import (
    ContextTypes, 
    ConversationHandler,
)
from telegram.constants import ParseMode


from .functions import keyboard, make_buttons, check_user_data
from .list import buttons_add



ARTICLE, QUANTITY, DESCRIPTION, INFO, COMMENT = range(5)







async def finish_text(context, update, user_data_key):
    await check_user_data(context)

    if user_data_key != '':
        context.user_data[user_data_key] = update.message.text
       
    text=f"""Ваша запись:\n
<b>Артикул: {context.user_data['table_article']}
Количество: {context.user_data['quantity']}
Описание: {context.user_data['description']}
Информация-размеры: {context.user_data['info']}
Пояснение о запчасти: {context.user_data['comment']}</b>\n
Что бы отправить запись, нажмите "Отправить заявку" """
    
    await context.bot.send_message(
        chat_id=update.effective_chat.id, 
        text=text,
        parse_mode=ParseMode.HTML,
        reply_markup=await make_buttons(buttons_add + [('Очистить', 'add')])
    )
    
    return ConversationHandler.END



async def send_text(context, user_id, text, state):

    await context.bot.send_message(
        chat_id=user_id, 
        text=f"{text}:\nВведите '/cancel' для отмены", 
    )
    return state




async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Отмена и завершение диалога."""
    # await context.bot.send_message(chat_id=update.effective_chat.id, 
    #                                text="Отмена",
    #                                reply_markup=ReplyKeyboardRemove())
    await finish_text(context, update, '')





async def make_article(update, context):
    return await send_text(context, update.effective_chat.id, "Введите артикул", ARTICLE)

async def finish_article(update, context):
    return await finish_text(context, update, 'table_article')





async def make_quantity(update, context):
    return await send_text(context, update.effective_chat.id, "Введите количество товара", QUANTITY)

async def finish_quantity(update, context):
    return await finish_text(context, update, 'quantity')





async def make_description(update, context):
    return await send_text(context, update.effective_chat.id, "Введите описание товара", DESCRIPTION)


async def finish_description(update, context):
    return await finish_text(context, update, 'description')





async def make_info(update, context):
    return await send_text(context, update.effective_chat.id, "Введите информацию-размеры", INFO)

async def finish_info(update, context):
    return await finish_text(context, update, 'info')





async def make_comment(update, context):
    return await send_text(context, update.effective_chat.id, "Введите пояснение о запчасти", COMMENT)

async def finish_comment(update, context):
    return await finish_text(context, update, 'comment')




function_map = {
    'article': [make_article, finish_article, ARTICLE],
    'quantity': [make_quantity, finish_quantity, QUANTITY],
    'description': [make_description, finish_description, DESCRIPTION],
    'info': [make_info, finish_info, INFO],
    'comment': [make_comment, finish_comment, COMMENT]
}