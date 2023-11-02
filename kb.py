from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
menu = [
    [KeyboardButton(text="Создать пост", callback_data="create_post"), KeyboardButton(text="Изменить пост", callback_data="edit_post")],
    [KeyboardButton(text="Контент-план", callback_data="content_plan"), KeyboardButton(text="Настройки", callback_data="settings")],
    [KeyboardButton(text="Шаблон", callback_data="sample"), KeyboardButton(text="Каталог эмодзи", callback_data="emoji_list")],
]

menu = ReplyKeyboardMarkup(keyboard=menu, resize_keyboard=True)

check_sub = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Проверить подписку", callback_data="check_sub")]])
buy_sub = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Купить подписку", callback_data="buy_sub")], [InlineKeyboardButton(text="◀️ Выйти в меню", callback_data="menu")]])

exit_kb = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="◀️ Выйти в меню")]], resize_keyboard=True)
iexit_kb = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="◀️ Выйти в меню", callback_data="menu")]])