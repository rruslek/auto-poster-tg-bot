from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.types.callback_query import CallbackQuery
from aiogram import flags
from aiogram.fsm.context import FSMContext
import utils
import db
from states import Gen

from aiogram import Bot
import config
from aiogram.enums.parse_mode import ParseMode
from datetime import datetime

from apscheduler.schedulers.asyncio import AsyncIOScheduler

import kb
import text

router = Router()
scheduler = AsyncIOScheduler()
@router.message(Command("start"))
async def start_handler(msg: Message):
    await db.add_user(msg.from_user.id)
    await msg.answer(text.greet.format(name=msg.from_user.full_name), reply_markup=kb.menu)


@router.message(F.text == "Меню")
@router.message(F.text == "Выйти в меню")
@router.message(F.text == "◀️ Выйти в меню")
async def menu(msg: Message):
    await msg.answer(text.menu, reply_markup=kb.menu)


@router.callback_query(F.data == "menu")
async def menu(clbck: CallbackQuery):
    await clbck.message.edit_text(text.menu, reply_markup=kb.menu)

@router.message(F.text == "Создать пост")
async def post_creation(msg: Message, state: FSMContext):
    data = await db.user_get_channels(msg.chat.id)
    print(data)
    print(data[0])
    if len(data) == 0:
        await state.set_state(Gen.add_channel)
        await msg.answer(text.no_channels, reply_markup=kb.menu)
    if len(data) == 1:
        data = data[0]
        print(data[0])
        await state.set_state(Gen.new_post)
        await state.update_data(channel=data[0])
        await msg.answer(text.new_post_onech + '<a href=\"https://t.me/' + data[3] + '\">' + data[2] + '</a>', reply_markup=kb.add_channel)

@router.message(Gen.new_post)
async def new_post(msg: Message, state: FSMContext):
    if msg.content_type == 'photo':
        photo = msg.photo[-1].file_id
        await state.set_state(Gen.edit_post)
        await state.update_data(photo=photo)
        await state.update_data(text=msg.caption)
        await msg.answer_photo(photo=photo, caption=msg.caption, reply_markup=kb.edit_post)
    elif msg.content_type == 'text':
        await state.set_state(Gen.edit_post)
        await state.update_data(text=msg.text)
        await msg.answer(msg.text, reply_markup=kb.edit_post)
    elif msg.content_type == 'video':
        video = msg.video.file_id
        await state.set_state(Gen.edit_post)
        await state.update_data(video=video)
        await state.update_data(text=msg.caption)
        await msg.answer_video(video=video, caption=msg.caption, reply_markup=kb.edit_post)

@router.callback_query(F.data == "cancel")
async def cancel_post(clbck: CallbackQuery, state: FSMContext):
    await clbck.message.delete()
    await state.set_state(Gen.new_post)
    await clbck.answer("Создание поста отменено!")



@router.callback_query(F.data == "next")
async def post_settings(clbck: CallbackQuery, state: FSMContext):
    await clbck.message.delete()
    await clbck.message.answer(text.post_settings_text, reply_markup=kb.post_setting)
@router.callback_query(F.data == "schedule_post")
async def schedule_post(clbck: CallbackQuery, state: FSMContext):
    scheduler.add_job(send_message, "date", run_date=datetime(2023, 11, 8, 21, 8), args=(await state.get_data()))
@router.message(Gen.edit_post)
async def edit_post(msg: Message, state: FSMContext):
    scheduler.add_job(send_message, "date", run_date=datetime(2023, 11, 8, 21, 8), args=(await state.get_data()))


@router.callback_query(F.data == "send_post")
async def send_message(clbck: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    if data['photo']:
        await send_photo(data)
    elif data['video']:
        await send_photo(data)
    else:
        await send_text(data)

async def send_text(data):
    bot = Bot(token=config.BOT_TOKEN, parse_mode=ParseMode.HTML)
    await bot.send_message(data['channel'], data['text'])

async def send_photo(data):
    bot = Bot(token=config.BOT_TOKEN, parse_mode=ParseMode.HTML)

    await bot.send_photo(data['channel'], photo=data['photo'], caption=data['text'])

async def send_video(data):
    bot = Bot(token=config.BOT_TOKEN, parse_mode=ParseMode.HTML)
    await bot.send_video(data['channel'], video=data['video'], caption=data['text'])

@router.message(Gen.add_channel)
@router.callback_query(F.data == "add_channel")
async def add_channel(msg: Message, state: FSMContext):
    bot = Bot(token=config.BOT_TOKEN, parse_mode=ParseMode.HTML)
    channel = msg.text
    if 'http' in channel or '@' in channel:
        if 'http' in channel:
            channel = channel.replace('https://', '')
            data = channel.split('/')
            username = '@'+data[1]
        else:
            username = channel
        chat = await bot.get_chat(username)
    else:
        id = msg.forward_from_chat.id
        chat = await bot.get_chat(id)
        print(id)

    if chat.type == 'channel':
        try:
            admin = await bot.get_chat_administrators(chat.id)
            print(admin)
            await db.add_channel(msg.from_user.id, chat.id, chat.title, chat.username)
            await msg.answer(text.channel_added + '<a href=\"https://t.me/' + chat.username + '\">' + chat.title + '</a>', reply_markup=kb.menu, parse_mode="HTML")
        except Exception:
            await msg.answer(text.not_admin, reply_markup=kb.menu)
    else:
        await msg.answer(text.not_channel, reply_markup=kb.menu)