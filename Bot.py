from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.utils.markdown import link

import asyncio
from config import TOKEN, GROUP_ID, OWNER_ID

from Buttons import start_markup

from db import add_user, update_user_pay, is_payed, get_user_data

from time import time, sleep

from qiwi import get_last_history

import sys

loop = asyncio.get_event_loop()

bot = Bot(token=TOKEN, parse_mode=types.ParseMode.MARKDOWN)
dp = Dispatcher(bot, loop=loop)
sub_amount_rub = 50
sub_amount_uah = 20
waiting_time = 0.1
bg = [time()]


async def wait_qiwi():
    while True:
        hist = get_last_history()
        # print(hist)
        for i in hist:
            if i[0]:
                a = get_user_data(i[0])
                # print(a)
                if a:
                    try:
                        url = link('Ссылка', 'channel_link')
                        if i[5] == 643:
                            # print(i[0])
                            # print((a[2] == 0 or a[2] == 'False'), round(i[1]) >= sub_amount_rub)
                            if (a[2] == 0 or a[2] == 'False') and round(i[1]) >= sub_amount_rub:
                                update_user_pay(int(i[0]), 1)
                                await bot.send_message(int(i[0]),
                                                       f'Вы подписались!\n{url}')
                                await bot.unban_chat_member(GROUP_ID, int(i[0]))
                        elif i[5] == 980:
                            if (a[2] == 0 or a[2] == 'False') and i[1] >= float(sub_amount_uah):
                                update_user_pay(int(i[0]), 1)
                                await bot.send_message(int(i[0]),
                                                       f'Вы подписались!\n{url}')
                                await bot.unban_chat_member(GROUP_ID, int(i[0]))
                    except Exception:
                        e = sys.exc_info()
                        await bot.send_message(OWNER_ID, f'Произошла ошибка! {e}')
        await asyncio.sleep(5)


loop.create_task(wait_qiwi())


@dp.message_handler(commands='start')
async def start_mes(msg: types.Message):
    if time() - bg[0] > waiting_time:
        bg[0] = time()
        if msg.from_user.id != OWNER_ID:
            await bot.unban_chat_member(GROUP_ID, msg.from_user.id)
            add_user(msg.from_user.username, msg.from_user.id)
            await msg.answer('Привет👋🏻', reply_markup=start_markup)
        else:
            await msg.answer('Чего пожелаете, хозяин?👀')


@dp.message_handler(commands='help')
async def help_mes(msg: types.Message):
    if time() - bg[0] > waiting_time:
        bg[0] = time()
        await msg.answer(
            'Нажмите на конпку Доступ внизу или напишите слово Доступ боту, чтобы получить доступ.',
            reply_markup=start_markup)


@dp.message_handler()
async def buttons_updater(msg: types.Message):
    if time() - bg[0] > waiting_time:
        bg[0] = time()
        if msg.text.lower() == 'доступ':
            await msg.answer(
                f'Для доступа в группу переведите 50 рублей на киви:'
                f'\nqiwi_link'
                f'\nНЕ ЗАБУДЬТЕ НАПИСАТЬ В КОММЕНТАРИИ КОД: {msg.from_user.id}!'
                f'\nИначе вы не получите доступ.'
                f'\nКроме кода ничего не пишите!')
        elif msg.text == 'Расценка':
            await msg.answer(
                f'Вход в приватку стоит 50 рублей. При покупке не забудьте указать личный код, который выдаст бот.')
        else:
            await msg.reply('Я не понял, что вы имели ввиду :(\nИспользуйте команду /help')


@dp.message_handler(content_types=types.ContentTypes.NEW_CHAT_MEMBERS)
async def handler_new_member(msg: types.Message):
    if time() - bg[0] > waiting_time:
        bg[0] = time()
        us = msg.new_chat_members[0]
        await msg.delete()
        if not is_payed(us['id']):
            await bot.kick_chat_member(GROUP_ID, us['id'])
            await bot.send_message(us['id'], 'Вы ещё не оплатили вход!')
        # print(us)


@dp.message_handler(content_types=types.ContentTypes.NEW_CHAT_TITLE)
async def del_mes_title(msg: types.Message):
    await msg.delete()


@dp.message_handler(content_types=types.ContentTypes.NEW_CHAT_PHOTO)
async def del_mes_photo(msg: types.Message):
    await msg.delete()


@dp.message_handler(content_types=types.ContentTypes.LEFT_CHAT_MEMBER)
async def handler_left_member(msg: types.Message):
    await msg.delete()


# @dp.channel_post_handler()
# async def gfsd(msg: types.chat_member_updated):
#     print(msg.text)
#     await bot.send_message(GROUP_ID, msg.text)

# @dp.my_chat_member_handler()
# async def some_handler(chat_member: types.ChatMemberUpdated):
#     print(chat_member)


if __name__ == '__main__':
    executor.start_polling(dp, loop=loop)
