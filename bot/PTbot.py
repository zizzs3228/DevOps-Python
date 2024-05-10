import asyncio
import logging
from logging.handlers import TimedRotatingFileHandler
from aiogram import F
from aiogram import Bot, Dispatcher, Router, types
from aiogram.utils.media_group import MediaGroupBuilder
from aiogram.types.error_event import ErrorEvent
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.filters.exception import ExceptionTypeFilter
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.markdown import hbold
from aiogram.methods.copy_message import CopyMessage
from aiogram.filters.chat_member_updated import ChatMemberUpdatedFilter, ChatMemberUpdated
from aiogram.fsm.state import State, StatesGroup
from aiogram.types.callback_query import CallbackQuery
from aiogram.filters.callback_data import CallbackData
from aiogram.filters import MEMBER, KICKED
import random
from datetime import datetime, timedelta
import paramiko
import time
import re
# from dotenv import load_dotenv
# from pathlib import Path
import os
import psycopg2
from psycopg2 import Error

# load_dotenv()

TOKEN = os.getenv('TOKEN')

host = os.getenv('HOST')
port = os.getenv('PORT')
username = os.getenv('USER')
password = os.getenv('PASSWORD')

hostDB = os.getenv('DBHOST')
portDB = os.getenv('DBPORT')
usernameDB = os.getenv('DBUSER')
passwordDB = os.getenv('DBPASSWORD')
databasename = os.getenv('DBNAME')


bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher()
ADMIN_ID = 468424685


class FindMail(StatesGroup):
    findmail = State()
    writeemail = State()

class FindPhone(StatesGroup):
    findphone = State()
    writephone = State()

class PasswordValidate(StatesGroup):
    verifpass = State()

class YesNoCallback(CallbackData, prefix="YesNo"):
    text:str



## Private users handlers
@dp.message(F.chat.type=='private',CommandStart())
async def command_start_handler(message: Message,state:FSMContext) -> None:
    await message.reply(f'Привет, {message.from_user.username}!')
    async with asyncio.Lock():
        info_logger.info(f"Пользователь {message.from_user.username}({message.from_user.id}) вошел в бота")
    await state.clear()

@dp.message(F.chat.type=='private',Command('verify_password'))
async def find_phone_number(message: Message,state:FSMContext) -> None:
    async with asyncio.Lock():
        info_logger.info(f"Пользователь {message.from_user.username}({message.from_user.id}) запросил валидацию пароля")
    await message.answer('Введите ваш пароль для валидации')
    await state.set_state(PasswordValidate.verifpass)

@dp.message(F.chat.type=='private',PasswordValidate.verifpass)
async def find_phone_number(message: Message,state:FSMContext) -> None:
    text = message.text
    async with asyncio.Lock():
        info_logger.info(f"Пользователь {message.from_user.username}({message.from_user.id}) ввел пароль для валидации. Пароль: {text}")
    pattern = (
        r'^(?=.*[A-Z])'    
        r'(?=.*[a-z])'        
        r'(?=.*\d)'           
        r'(?=.*[!@#$%^&*()?])'  
        r'.{8,}$'              
    )
    
    if re.match(pattern, text):
        await message.answer('Пароль сложный')
    else:
        await message.answer('Пароль простой')


@dp.message(F.chat.type=='private',Command('get_release'))
async def get_release(message: Message) -> None:
    async with asyncio.Lock():
        info_logger.info(f"Пользователь {message.from_user.username}({message.from_user.id}) запросил get_release")
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=host, username=username, password=password, port=port)
    stdin, stdout, stderr = client.exec_command('lsb_release -a')
    data = stdout.read() + stderr.read()
    client.close()
    data = str(data).replace('\\n', '\n').replace('\\t', '\t')[2:-1]
    await message.answer(data)

@dp.message(F.chat.type=='private',Command('get_uname'))
async def get_release(message: Message) -> None:
    async with asyncio.Lock():
        info_logger.info(f"Пользователь {message.from_user.username}({message.from_user.id}) запросил get_uname")
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=host, username=username, password=password, port=port)
    stdin, stdout, stderr = client.exec_command('uname -a')
    data = stdout.read() + stderr.read()
    client.close()
    data = str(data).replace('\\n', '\n').replace('\\t', '\t')[2:-1]
    await message.answer(data)

@dp.message(F.chat.type=='private',Command('get_uptime'))
async def get_release(message: Message) -> None:
    async with asyncio.Lock():
        info_logger.info(f"Пользователь {message.from_user.username}({message.from_user.id}) запросил get_uptime")
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=host, username=username, password=password, port=port)
    stdin, stdout, stderr = client.exec_command('uptime')
    data = stdout.read() + stderr.read()
    client.close()
    data = str(data).replace('\\n', '\n').replace('\\t', '\t')[2:-1]
    await message.answer(data)

@dp.message(F.chat.type=='private',Command('get_df'))
async def get_release(message: Message) -> None:
    async with asyncio.Lock():
        info_logger.info(f"Пользователь {message.from_user.username}({message.from_user.id}) запросил get_df")
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=host, username=username, password=password, port=port)
    stdin, stdout, stderr = client.exec_command('df -h')
    data = stdout.read() + stderr.read()
    client.close()
    data = str(data).replace('\\n', '\n').replace('\\t', '\t')[2:-1]
    await message.answer(data)

@dp.message(F.chat.type=='private',Command('get_free'))
async def get_release(message: Message) -> None:
    async with asyncio.Lock():
        info_logger.info(f"Пользователь {message.from_user.username}({message.from_user.id}) запросил get_free")
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=host, username=username, password=password, port=port)
    stdin, stdout, stderr = client.exec_command('free -h')
    data = stdout.read() + stderr.read()
    client.close()
    data = str(data).replace('\\n', '\n').replace('\\t', '\t')[2:-1]
    await message.answer(data)

@dp.message(F.chat.type=='private',Command('get_mpstat'))
async def get_release(message: Message) -> None:
    async with asyncio.Lock():
        info_logger.info(f"Пользователь {message.from_user.username}({message.from_user.id}) запросил get_mpstat")
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=host, username=username, password=password, port=port)
    stdin, stdout, stderr = client.exec_command('mpstat')
    data = stdout.read() + stderr.read()
    client.close()
    data = str(data).replace('\\n', '\n').replace('\\t', '\t')[2:-1]
    await message.answer(data)

@dp.message(F.chat.type=='private',Command('get_w'))
async def get_release(message: Message) -> None:
    async with asyncio.Lock():
        info_logger.info(f"Пользователь {message.from_user.username}({message.from_user.id}) запросил get_w")
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=host, username=username, password=password, port=port)
    stdin, stdout, stderr = client.exec_command('w')
    data = stdout.read() + stderr.read()
    client.close()
    data = str(data).replace('\\n', '\n').replace('\\t', '\t')[2:-1]
    await message.answer(data)

@dp.message(F.chat.type=='private',Command('get_auths'))
async def get_release(message: Message) -> None:
    async with asyncio.Lock(): 
        info_logger.info(f"Пользователь {message.from_user.username}({message.from_user.id}) запросил get_auths")
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=host, username=username, password=password, port=port)
    stdin, stdout, stderr = client.exec_command('journalctl --system -u ssh | grep sshd | tail -n 10')
    data = stdout.read() + stderr.read()
    client.close()
    data = str(data).replace('\\n', '\n').replace('\\t', '\t')[2:-1]
    await message.answer(data)

@dp.message(F.chat.type=='private',Command('get_critical'))
async def get_release(message: Message) -> None:
    async with asyncio.Lock():
        info_logger.info(f"Пользователь {message.from_user.username}({message.from_user.id}) запросил get_critical")
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=host, username=username, password=password, port=port)
    stdin, stdout, stderr = client.exec_command('journalctl --system -p info | tail -n 5')
    data = stdout.read() + stderr.read()
    client.close()
    data = str(data).replace('\\n', '\n').replace('\\t', '\t')[2:-1]
    await message.answer(data)

@dp.message(F.chat.type=='private',Command('get_ps'))
async def get_release(message: Message) -> None:
    async with asyncio.Lock():
        info_logger.info(f"Пользователь {message.from_user.username}({message.from_user.id}) запросил get_ps")
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=host, username=username, password=password, port=port)
    stdin, stdout, stderr = client.exec_command('ps')
    data = stdout.read() + stderr.read()
    client.close()
    data = str(data).replace('\\n', '\n').replace('\\t', '\t')[2:-1]
    if len(data)>3000:
        data = data[:3000]
    await message.answer(data)

@dp.message(F.chat.type=='private',Command('get_ss'))
async def get_release(message: Message) -> None:
    async with asyncio.Lock():
        info_logger.info(f"Пользователь {message.from_user.username}({message.from_user.id}) запросил get_ss")
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=host, username=username, password=password, port=port)
    stdin, stdout, stderr = client.exec_command('netstat -tulpn')
    data = stdout.read() + stderr.read()
    client.close()
    data = str(data).replace('\\n', '\n').replace('\\t', '\t')[2:-1]
    if len(data)>3000:
        data = data[:3000]
    await message.answer(data)

@dp.message(F.chat.type=='private',Command('get_apt_list'))
async def get_release(message: Message) -> None:
    async with asyncio.Lock():
        info_logger.info(f"Пользователь {message.from_user.username}({message.from_user.id}) запросил get_apt_list")
    text = message.text
    splited = text.split(' ')
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=host, username=username, password=password, port=port)
    stdin, stdout, stderr = client.exec_command('apt list')
    data = stdout.read() + stderr.read()
    client.close()
    data = str(data).replace('\\n', '\n').replace('\\t', '\t')[2:-1]
    if len(splited) == 1:  
        if len(data)>3000:
            data = data[:3000]
        await message.answer(data)
    elif len(splited) == 2:
        package = splited[1]
        if package in data:
            tosend = ''
            for line in data.split('\n'):
                if package in line:
                    tosend += line + '\n'
            await message.answer(tosend)
        else:
            await message.answer('Пакет не найден')
    else:
        await message.answer('Неверный формат команды')
        async with asyncio.Lock():
            error_logger.error("Неверный формат команды get_apt_list от юзера %s", message.from_user.username)

@dp.message(F.chat.type=='private',Command('get_services'))
async def get_release(message: Message) -> None:
    async with asyncio.Lock():
        info_logger.info(f"Пользователь {message.from_user.username}({message.from_user.id}) запросил get_services")
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=host, username=username, password=password, port=port)
    stdin, stdout, stderr = client.exec_command('service --status-all | grep +')
    data = stdout.read() + stderr.read()
    client.close()
    data = str(data).replace('\\n', '\n').replace('\\t', '\t')[2:-1]
    if len(data)>3000:
        data = data[:3000]
    await message.answer(data)

@dp.message(F.chat.type=='private',Command('get_repl_logs'))
async def get_release(message: Message) -> None:
    async with asyncio.Lock():
        info_logger.info(f"Пользователь {message.from_user.username}({message.from_user.id}) запросил get_repl_logs")
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=host, username=username, password=password, port=port)
    stdin, stdout, stderr = client.exec_command('docker logs -n 40 db')
    data = stdout.read() + stderr.read()
    client.close()
    data = str(data).replace('\\n', '\n').replace('\\t', '\t')[2:-1]
    text = ''
    for line in data.split('\n'):
        if 'repl' in line:
            text += line + '\n'
    if len(text)==0:
        text = 'Логи репликации не найдены'
        await message.answer(text)
        return None
    if len(text)>3000:
        text = text[:3000]
    await message.answer(text)

@dp.message(F.chat.type=='private',Command('get_emails'))
async def get_emails(message: Message) -> None:
    async with asyncio.Lock():
        info_logger.info(f"Пользователь {message.from_user.username}({message.from_user.id}) запросил get_emails")
    connection = None
    info_logger.info(f"host: {hostDB}, port: {portDB}, username: {usernameDB}, password: {passwordDB}, database: {databasename}")
    try:
        connection = psycopg2.connect(user=usernameDB,
                                    password=passwordDB,
                                    host=hostDB,
                                    port=portDB, 
                                    database=databasename)
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM emails;")
        data = cursor.fetchall()
        tosend = ''
        for row in data:
            tosend += f'ID: {row[0]}, Email: {row[1]}\n'
        if len(tosend)==0:
            tosend = 'Имейлы не найдены'
        await message.answer(tosend)
        async with asyncio.Lock():
            info_logger.info("Команда get_emails успешно выполнена")
    except (Exception, Error) as error:
        async with asyncio.Lock():
            error_logger.error("Ошибка при работе с PostgreSQL: %s", error)
    finally:
        if connection is not None:
            cursor.close()
            connection.close()

@dp.message(F.chat.type=='private',Command('get_phones'))
async def get_emails(message: Message) -> None:
    async with asyncio.Lock():  
        info_logger.info(f"Пользователь {message.from_user.username}({message.from_user.id}) запросил get_phones")
    connection = None
    try:
        connection = psycopg2.connect(user=usernameDB,
                                    password=passwordDB,
                                    host=hostDB,
                                    port=portDB, 
                                    database=databasename)
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM phones;")
        data = cursor.fetchall()
        tosend = ''
        for row in data:
            tosend += f'ID: {row[0]}, Phone: {row[1]}\n'
        if len(tosend)==0:
            tosend = 'Телефоны не найдены'
        await message.answer(tosend)
        async with asyncio.Lock():
            info_logger("Команда get_phones успешно выполнена")
    except (Exception, Error) as error:
        logging.error("Ошибка при работе с PostgreSQL: %s", error)
    finally:
        if connection is not None:
            cursor.close()
            connection.close()

@dp.message(F.chat.type=='private', Command('find_email')) 
async def find_email(message: Message,state:FSMContext) -> None:
    async with asyncio.Lock():
        info_logger.info(f"Пользователь {message.from_user.username}({message.from_user.id}) запросил find_email")
    await message.answer('Введите текст, в котором нужно найти email')
    await state.set_state(FindMail.findmail)

@dp.message(F.chat.type=='private',FindMail.findmail)
async def find_email(message: Message,state:FSMContext) -> None:
    async with asyncio.Lock():
        info_logger.info(f"Пользователь {message.from_user.username}({message.from_user.id}) ввел текст для поиска email")
    await state.clear()
    text = message.text
    emails = re.findall(r'[\w\.-]+@[\w\.-]+', text)
    if len(emails)>0:
        inlinebuttons1 = [InlineKeyboardButton(text="Да", callback_data=YesNoCallback(text='Да').pack()),
                    InlineKeyboardButton(text="Нет", callback_data=YesNoCallback(text='Нет').pack())]
        inlinesupportkeyboard = InlineKeyboardMarkup(row_width=1, inline_keyboard=[inlinebuttons1])
        messagetosend = 'Найденные email: \n'
        for email in emails:
            messagetosend += email + '\n'
        await message.answer(messagetosend,reply_markup=inlinesupportkeyboard)
        await state.set_data({'emails':emails})
        await state.set_state(FindMail.writeemail)
    else:
        await message.answer('Email не найдены') 
    
@dp.callback_query(YesNoCallback.filter(F.text=='Да'),FindMail.writeemail)
async def write_email_to_db_yes(call: CallbackQuery,state:FSMContext) -> None:
    async with asyncio.Lock():
        info_logger.info("Пользователь согласился записать email в базу данных")
    data = await state.get_data()
    emails = data['emails']
    connection = None
    try:
        connection = psycopg2.connect(user=usernameDB,
                                    password=passwordDB,
                                    host=hostDB,
                                    port=portDB, 
                                    database=databasename)
        cursor = connection.cursor()
        cursor.execute("SELECT MAX(id) FROM emails;")
        currid = cursor.fetchone()[0]
        if currid is None:
            currid = 0
        for email in emails:
            currid+=1
            cursor.execute(f"INSERT INTO emails (id,email) VALUES ({currid},'{email}');")
        connection.commit()
        await call.message.answer('Email записаны в базу данных')
        async with asyncio.Lock():
            info_logger.info("Email записаны в базу данных")
    except (Exception, Error) as error:
        async with asyncio.Lock():
            error_logger.error("Ошибка при работе с PostgreSQL: %s", error)
        await call.message.answer('Ошибка при записи в базу данных')
    finally:
        if connection is not None:
            cursor.close()
            connection.close()
    await state.clear()

@dp.callback_query(YesNoCallback.filter(F.text=='Нет'))
async def write_email_to_db_no(call: CallbackQuery,state:FSMContext) -> None:
    async with asyncio.Lock():
        info_logger.info("Пользователь отказался записать в базу данных")
    await call.message.answer('На нет и суда нет...')
    await state.clear()






@dp.message(F.chat.type=='private',Command('find_phone_number'))
async def find_phone_number(message: Message,state:FSMContext) -> None:
    async with asyncio.Lock():
        info_logger.info(f"Пользователь {message.from_user.username}({message.from_user.id}) запросил find_phone_number")
    await message.answer('Введите текст, в котором нужно найти номер телефона')
    await state.set_state(FindPhone.findphone)

@dp.message(F.chat.type=='private',FindPhone.findphone)
async def find_phone_number(message: Message,state:FSMContext) -> None:
    async with asyncio.Lock():
        info_logger.info(f"Пользователь {message.from_user.username}({message.from_user.id}) ввел текст для поиска номера телефона")
    await state.clear()
    text = message.text
    phones = re.findall(r'(?:8|\+7)[\s\-]?(?:\(\d{3}\)|\d{3})[\s\-]?\d{3}[\s\-]?\d{2}[\s\-]?\d{2}', text)
    if len(phones)>0:
        inlinebuttons1 = [InlineKeyboardButton(text="Да", callback_data=YesNoCallback(text='Да').pack()),
                    InlineKeyboardButton(text="Нет", callback_data=YesNoCallback(text='Нет').pack())]
        inlinesupportkeyboard = InlineKeyboardMarkup(row_width=1, inline_keyboard=[inlinebuttons1])
        messagetosend = 'Найденные телефоны: \n'
        for phone in phones:
            messagetosend += phone + '\n'
        await message.answer(messagetosend,reply_markup=inlinesupportkeyboard)
        await state.set_data({'phones':phones})
        await state.set_state(FindPhone.writephone) 
    else:
        await message.answer('Номера телефонов не найдены')
    

@dp.callback_query(YesNoCallback.filter(F.text=='Да'),FindPhone.writephone)
async def write_phone_to_db_yes(call: CallbackQuery,state:FSMContext) -> None:
    async with asyncio.Lock():
        info_logger.info("Пользователь согласился записать телефоны в базу данных")
    data = await state.get_data()
    phones = data['phones']
    connection = None
    try:
        connection = psycopg2.connect(user=usernameDB,
                                    password=passwordDB,
                                    host=hostDB,
                                    port=portDB, 
                                    database=databasename)
        cursor = connection.cursor()
        cursor.execute("SELECT MAX(id) FROM phones;")
        currid = cursor.fetchone()[0]
        if currid is None:
            currid = 0
        for phone in phones:
            currid+=1
            cursor.execute(f"INSERT INTO phones (id,phone) VALUES ({currid},'{phone}');")
        connection.commit()
        await call.message.answer('Телефоны записаны в базу данных')
        async with asyncio.Lock():
            info_logger.info("Телефоны записаны в базу данных")
    except (Exception, Error) as error:
        async with asyncio.Lock():
            error_logger.error("Ошибка при работе с PostgreSQL: %s", error)
        await call.message.answer('Ошибка при записи в базу данных')
    finally:
        if connection is not None:
            cursor.close()
            connection.close()
    await state.clear()





















#Error handlers
@dp.error(F.update.message.as_("message"))
async def handle_my_custom_exception(event: ErrorEvent, message: Message,state:FSMContext):
    text = ''
    if message.text is not None:
        text = message.text
    elif message.caption is not None:
        text = message.caption
    async with asyncio.Lock():
        error_logger.error(f"Ошибка: {event.exception} \n\nСообщение: {text} \n\nПользователь: {message.from_user.username}({message.from_user.id}, {message.from_user.username})")
    await bot.send_message(ADMIN_ID,f"Ошибка: {event.exception} \n\nПользователь: {message.from_user.username}({message.from_user.id})")
    await state.clear()

async def on_startup():
    print('Bot has been started')
    async with asyncio.Lock():
        info_logger.info('Bot has been started')

async def on_shutdown():
    print('Shutting down...')
    async with asyncio.Lock():
        info_logger.info('Shutting down...')
    logging.shutdown()

async def notify(message:str):
    if len(message)>3000:
        message = message[:3000]
    await bot.send_message(ADMIN_ID,message)

async def main() -> None:
    await on_startup()
    await dp.start_polling(bot,on_startup=on_startup)


if __name__ == "__main__":
    info_logger = logging.getLogger("info")
    info_handler = TimedRotatingFileHandler("./logs/info.log", when="midnight", interval=1, backupCount=60,errors='replace')
    info_logger.setLevel(logging.INFO)  # Изменено на INFO
    info_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    info_handler.setFormatter(info_formatter)
    info_logger.addHandler(info_handler)

    # Создание логгера для ошибок
    error_logger = logging.getLogger("error")
    error_hd = TimedRotatingFileHandler("./logs/error.log", when="midnight", interval=1, backupCount=60,errors='replace')
    error_logger.setLevel(logging.ERROR)
    error_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    error_hd.setFormatter(error_formatter)
    error_logger.addHandler(error_hd)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        asyncio.run(on_shutdown())
    except Exception as e:
        error_logger.error(f"Ошибка: {e}")
        asyncio.run(notify(f"Ошибка: {e}"))
