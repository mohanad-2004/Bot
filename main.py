from rembg import remove
from PIL import Image
import os
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
from telegram import Update
import asyncio

token = "6522430097:AAHwaoj4iSA-hIKidgLnZW5SjNr02j0V2ug"async def bg_photo(name: str):
    Name, _ = os.path.splitext(name)
    output_path = f'./bg/{Name}.png'    input = Image.open(f"./temp/{name}")
    output = remove(input)
    output.save(output_path)
    remove(f'./temo/{name}')
    remove(output_path)
    return output_path


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text='رجاءا قم بارسال الصورة')


async def photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if filters.PHOTO.check_update(update):
        file_id = update.message.photo[-1].file_id
        unique_name = update.message.photo[-1].file_unique_id
        name = f'{unique_name}.jpg'    elif filters.Document.IMAGE.check_update(update):
        file_id = update.message.document.file_id
        unique_name = update.message.document.file_unique_id
        _, f_ext = os.path.splitext(update.message.document.file_name)
        name = f'{unique_name}{f_ext}'        photo_file = await context.bot.get_file(file_id)
        await photo_file.download_to_drive(custom_path=f'./temp/{name}')
        await context.bot.send_message(chat_id=update.effective_chat.id, text='جاري المعالجة...]')
        # await context.bot.send_message(chat_id=update.effective_chat.id, document = bg_photo(name) )if __name__ == '__main__':
    # Handlers    application = ApplicationBuilder().token(token).build()
    start_handler = CommandHandler('start', start)
    message_handler = MessageHandler(filters.PHOTO | filters.Document.IMAGE, photo)

    # Register    application.add_handler(start_handler)
    application.add_handler(message_handler)

    print('running')
    application.run_polling()