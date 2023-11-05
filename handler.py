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

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime

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


@router.callback_query(F.data == "balance")
async def menu(clbck: CallbackQuery):
    balance = await db.get_balance(clbck.message.chat.id)
    await clbck.message.edit_text(text.balance + str(balance) + " кредита", reply_markup=kb.balance)


@router.callback_query(F.data == "kb")
async def menu(clbck: CallbackQuery):
    await clbck.message.edit_text(text.menu, reply_markup=kb.menu)


@router.callback_query(F.data == "generate_image")
@flags.chat_action("choose_room")
async def room_type(clbck: CallbackQuery, state: FSMContext):
    balance = await db.get_balance(clbck.message.chat.id)
    if int(balance) > 0:
        await state.set_state(Gen.room_type)
        await clbck.message.edit_text(text.choose_room, reply_markup=kb.room_types)
    else:
        await clbck.message.edit_text(text.low_balance, reply_markup=kb.iexit_kb)


@router.callback_query(F.data == "bedroom")
@router.callback_query(F.data == "living room")
@router.callback_query(F.data == "kitchen")
@router.callback_query(F.data == "bathroom")
async def input_room_type(clbck: CallbackQuery, state: FSMContext):
    await state.update_data(room_type=clbck.data)
    await clbck.message.edit_text(text.choose_style, reply_markup=kb.room_styles)


@router.callback_query(F.data == "minimalism")
@router.callback_query(F.data == "modern")
@router.callback_query(F.data == "neo-industrial")
@router.callback_query(F.data == "scandinavian")
@router.callback_query(F.data == "loft")
@router.callback_query(F.data == "bohemian")
@router.callback_query(F.data == "japanese")
@router.callback_query(F.data == "farmhouse")
@router.callback_query(F.data == "coastal")
@router.callback_query(F.data == "zen")
async def input_room_type(clbck: CallbackQuery, state: FSMContext):
    await state.update_data(room_style=clbck.data)
    await state.set_state(Gen.get_img)
    await clbck.message.edit_text(text.gen_image, reply_markup=kb.iexit_kb)


@router.message(Gen.get_img)
async def input_image_prompt(msg: Message, state: FSMContext):
    bot = Bot(token=config.BOT_TOKEN, parse_mode=ParseMode.HTML)
    prompt = msg.photo[-1].file_id
    await state.update_data(img_prompt=prompt)
    mesg = await msg.answer(text.gen_wait)
    try:
        data = await state.get_data()
        file_id = data['img_prompt']
        type = data['room_type']
        style = data['room_style']
        file = await bot.get_file(file_id)
        resp = await utils.generate_image(file.file_path, type, style)
        await mesg.delete()
        await msg.answer_photo(photo=resp, caption=text.img_watermark)
        await msg.answer(text.menu, reply_markup=kb.menu)
        await db.change_balance('-1', msg.chat.id)
    except Exception:
        await mesg.delete()
        await msg.answer(text.err, reply_markup=kb.iexit_kb)


@router.callback_query(F.data == "free_credit")
async def get_free_credit(clbck: CallbackQuery):
    status = await db.user_get_status(clbck.message.chat.id)
    if status == '0':
        await clbck.message.edit_text(text.channel_subscribe, reply_markup=kb.check_sub)
    else:
        await clbck.message.edit_text(text.subscribe_sorry, reply_markup=kb.iexit_kb)


@router.callback_query(F.data == "check_sub")
async def get_free_credit(clbck: CallbackQuery):
    bot = Bot(token=config.BOT_TOKEN, parse_mode=ParseMode.HTML)
    user_channel_status = await bot.get_chat_member(chat_id=-1001506387417, user_id=clbck.message.chat.id)
    if user_channel_status.status != 'left':
        await clbck.message.delete()
        await db.change_balance('+5', clbck.message.chat.id)
        await db.user_set_status(1, clbck.message.chat.id)
        await clbck.message.answer(text.subscribe_success, reply_markup=kb.iexit_kb)
    else:
        await clbck.answer("Вы не подписаны на канал!")


@router.callback_query(F.data == "subscribe")
async def get_free_credit(clbck: CallbackQuery):
    await clbck.message.edit_text(text.buy_sub, reply_markup=kb.buy_sub)