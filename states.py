from aiogram.fsm.state import StatesGroup, State

class Gen(StatesGroup):
    add_channel = State()
    new_post = State()
    edit_post = State()
    channel_id = State()
    set_date = State()