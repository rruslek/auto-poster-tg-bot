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

import kb
import text

router = Router()


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
    await state.set_state(Gen.get_channel)
    await msg.answer(text.no_channels, reply_markup=kb.menu)

@router.message(Gen.get_channel)
async def get_channel(msg: Message, state: FSMContext):
    await msg.answer(text.channel_added, reply_markup=kb.menu)