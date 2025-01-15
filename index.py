from telegram import Update, ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import (
    filters, 
    ApplicationBuilder, 
    ContextTypes, 
    CommandHandler, 
    CallbackContext, 
    CallbackQueryHandler,
    MessageHandler,
)
from telegram.constants import ParseMode

from datetime import datetime

from config.config import TOKEN, ADMIN_LIST, logger
from config.functions import make_buttons, clean_data, check_user_data
from config.list import buttons_add, main_menu
from config.db import db
from config.utils import create_conversation_handler
from config.functions_sheets_api import handle_data_for_google_spreadsheet, get_number_from_google_spreadsheet





application = ApplicationBuilder().token(TOKEN).build()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):


    db.add_user(
        update.effective_user.id, 
        update.effective_user.username,
        update.effective_user.first_name,
        update.effective_user.last_name
    )

    if update.message.chat.type != 'private':
        return
    
    member = db.check_user(update.effective_user.id)
    
    
    if member[2] == 1 and member[0] and member[1]:

        await context.bot.send_message(chat_id=update.effective_chat.id, 
                            text=f'Здравствуйте <b>{update.effective_user.first_name}</b> 👋', 
                            parse_mode=ParseMode.HTML,
                            reply_markup=await make_buttons(main_menu))
    

    elif member[2] == 1 and (not member[0] or not member[1]):

        await context.bot.send_message(chat_id=update.effective_chat.id, 
                text=f'Здравствуйте <b>{update.effective_user.first_name}</b> 👋\n'
                      'Процесс регистрации:\nВыберите № Комплекса', 
                parse_mode=ParseMode.HTML, reply_markup=await make_buttons([
                                                ('Евро3', 'evro3'), ('Евро5', 'evro5')
                                            ]))

    else:
        button = KeyboardButton("Поделиться номером", request_contact=True)
        reply_markup = ReplyKeyboardMarkup([[button]], resize_keyboard=True)

        # Отправляем сообщение с клавиатурой
        await update.message.reply_text(
            text=f'Ваш ИД: {update.effective_user.id}',
            reply_markup=reply_markup
        )
    





async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.message.chat.type != 'private':
        return
    
    return await context.bot.send_message(chat_id=update.effective_chat.id, 
                            text=f'Помощь по боту', 
                            parse_mode=ParseMode.HTML)





async def add_member(update: Update, context: ContextTypes.DEFAULT_TYPE):
    
    if not update.effective_user.id in ADMIN_LIST:
        return
    
    print(f'{update.message.text=}')
    member_id = update.message.text.replace('/add', '').replace(' ', '')
    print(f'{member_id=}')

    db.update_user_member(member_id)

    return await context.bot.send_message(chat_id=update.effective_chat.id, 
                            text=f'Пользователь {member_id} добавлен')
    





async def callback_handler(update: Update, context: CallbackContext):

    user_id = update.effective_user.id
    callback_data = update.callback_query.data
    call = update.callback_query

    member = db.check_user(user_id)
    if member[2] != 1:
        return
    

    if callback_data == 'evro3' or callback_data == 'evro5':
        member = db.check_user(user_id)
        if member[2] == 1 and member[0] and member[1]:
            return
        
        context.user_data['evro'] = 'Евро3' if callback_data == 'evro3' else 'Евро5'
            
        await context.bot.edit_message_text(chat_id=update.effective_chat.id, message_id=call.message.message_id,
                            text=f'Здравствуйте <b>{update.effective_user.first_name}</b> 👋\n'
                            'Процесс регистрации:\nВыберите машину', 
                            parse_mode=ParseMode.HTML,
                            reply_markup=await make_buttons([
                                ('Харвестер', 'car1'), ('Форвардер', 'car2')
                            ]))


    elif callback_data == 'car1' or callback_data == 'car2':
        member = db.check_user(user_id)
        if member[2] == 1 and member[0] and member[1]:
            return
        
        context.user_data['car'] = 'Харвестер' if callback_data == 'car1' else 'Форвардер'

        db.update_user_data(user_id, context.user_data['evro'], context.user_data['car'])
        
        await context.bot.edit_message_text(chat_id=update.effective_chat.id, message_id=call.message.message_id,
                            text=f'Вы успешно зарегестрированны', 
                            reply_markup=await make_buttons(main_menu))
        
    
    elif member[2] == 1 and (not member[0] or not member[1]):

        await context.bot.send_message(chat_id=update.effective_chat.id, 
                text=f'Здравствуйте <b>{update.effective_user.first_name}</b> 👋\n'
                      'Процесс регистрации:\nВыберите № Комплекса', 
                parse_mode=ParseMode.HTML, reply_markup=await make_buttons([
                                                ('Евро3', 'evro3'), ('Евро5', 'evro5')
                                            ]))
        
    elif callback_data == 'add':
        
        await clean_data(context)
        await context.bot.edit_message_text(chat_id=update.effective_chat.id, message_id=call.message.message_id,
                            text='Новая запись:\n\n\nВыберите ячейку для заполнения\n'
                            'Что бы отправить запись в таблицу, нажмите "Отправить заявку"', 
                            parse_mode=ParseMode.HTML,
                            reply_markup=await make_buttons(buttons_add))
        

    elif callback_data == 'add-complate':

        await check_user_data(context)

        data = datetime.now().strftime("%d.%m.%Y")
        article = context.user_data['table_article']
        quantity = context.user_data['quantity']
        description = context.user_data['description']
        info = context.user_data['info']
        comment = context.user_data['comment']
        evro, car, _, name = db.check_user(user_id)


        values = [
            data, article, quantity, description, 
            info, comment, name, evro, car
        ]

        handle_data_for_google_spreadsheet(values)

        await context.bot.edit_message_text(chat_id=update.effective_chat.id, message_id=call.message.message_id,
                            text=f'Записано:\n\n<b>Дата: {data}\nАртикул: {article}\n'
                                 f'Количество: {quantity}\nОписание: {description}\n'
                                 f'Информация-размеры: {info}\nПояснение о запчасти: {comment}\n'
                                 f'Имя: {name}\nКомплекс: {evro}\n Машина: {car}</b>',
                            parse_mode=ParseMode.HTML)
        await context.bot.send_message(chat_id=update.effective_chat.id,
                            text=f'Запись успешно добавлена', 
                            reply_markup=ReplyKeyboardRemove())
        await context.bot.send_message(chat_id=update.effective_chat.id,
                            text=f'Главное меню', 
                            reply_markup=await make_buttons(main_menu))
        
    
    elif callback_data == 'main-menu':
        await context.bot.send_message(chat_id=update.effective_chat.id,
                            text=f'Главное меню', 
                            reply_markup=await make_buttons(main_menu))




async def message_func(update: Update, context: ContextTypes.DEFAULT_TYPE):
    
    mes = update.message

    
    if mes.contact:
        phone_number = str(mes.contact.phone_number)
        user_id = mes.contact.user_id

        db.update_user_phone(user_id, phone_number)
        results = get_number_from_google_spreadsheet()

        print(results)

        for result in results:
            if phone_number in result:
                print(f'{results=}')
                print(f'{phone_number=}')
                print(f'{result[0]=}')
                
                db.update_user_member(user_id, result[0], result[2], result[3])

                await context.bot.send_message(chat_id=update.effective_chat.id,
                            text=f'Доступ предоставлен\n\nГлавное меню', 
                            reply_markup=await make_buttons(main_menu))




def main():
    start_handler = CommandHandler('start', start)
    help_handler = CommandHandler('help', help)
    add_handler = CommandHandler('add', add_member)
    # converstation
    conv_article = create_conversation_handler('article')
    conv_quantity = create_conversation_handler('quantity')
    conv_description = create_conversation_handler('description')
    conv_info = create_conversation_handler('info')
    conv_comment = create_conversation_handler('comment')
    # inline
    call_back_query = CallbackQueryHandler(callback_handler)
    # message
    mes_henler = MessageHandler(filters.ALL, message_func)

    
    application.add_handler(start_handler)
    application.add_handler(help_handler)
    application.add_handler(add_handler)
    # converstation
    application.add_handler(conv_article)
    application.add_handler(conv_quantity)
    application.add_handler(conv_description)
    application.add_handler(conv_info)
    application.add_handler(conv_comment)
    # inline
    application.add_handler(call_back_query)
    # message
    application.add_handler(mes_henler)

    application.run_polling()

if __name__ == '__main__':
    main()