from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
menu = [
    [KeyboardButton(text="Создать пост", callback_data="create_post"), KeyboardButton(text="Изменить пост", callback_data="edit_post")],
    [KeyboardButton(text="Контент-план", callback_data="content_plan"), KeyboardButton(text="Настройки", callback_data="settings")],
    [KeyboardButton(text="Шаблон", callback_data="sample"), KeyboardButton(text="Каталог эмодзи", callback_data="emoji_list")],
]

post_media_text = [
    [InlineKeyboardButton(text="Изменить текст", callback_data="edit_text")],
    [InlineKeyboardButton(text="Добавить медиа", callback_data="add_media")],
    [InlineKeyboardButton(text="Со звуком", callback_data="sound_on"), InlineKeyboardButton(text="URL-кнопки", callback_data="url_buttons")],
    [InlineKeyboardButton(text="Комментарии", callback_data="comments"), InlineKeyboardButton(text="Закрепить", callback_data="pin")],
    [InlineKeyboardButton(text="Ответный пост: не задан", callback_data="reply_post")],
    [InlineKeyboardButton(text="<- Отменить", callback_data="cancel"), InlineKeyboardButton(text="Далее ->", callback_data="next")],
]

post_setting_ready = [
    [InlineKeyboardButton(text="Таймер автоудаления: нет", callback_data="auto_delete")],
    [InlineKeyboardButton(text="Автоповтор: нет", callback_data="auto_repeat")],
    [InlineKeyboardButton(text="Копировать", callback_data="copy_post"), InlineKeyboardButton(text="Переслать", callback_data="forward_post")],
    [InlineKeyboardButton(text="Отложить", callback_data="schedule_post"), InlineKeyboardButton(text="Опубликовать", callback_data="post_confirm")],
    [InlineKeyboardButton(text="<- Назад", callback_data="cancel")],
]

post_publication_confirm = [
    [InlineKeyboardButton(text="Да, опубликовать", callback_data="send_post")],
    [InlineKeyboardButton(text="<- Назад", callback_data="cancel")],
]

post_dates_btn = [
    [InlineKeyboardButton(text="<- Вс, 26 ноября", callback_data="data1"),
     InlineKeyboardButton(text="Пн, 27 ноября", callback_data="data1"),
     InlineKeyboardButton(text="Вт, 28 ноября ->", callback_data="data2")]
]

post_dates_post = [
    [InlineKeyboardButton(text="<- Вс, 26 ноября", callback_data="data1"),
     InlineKeyboardButton(text="Пн, 27 ноября", callback_data="data1"),
     InlineKeyboardButton(text="Вт, 28 ноября ->", callback_data="data2")],
    [InlineKeyboardButton(text="", callback_data="post")],
]

menu = ReplyKeyboardMarkup(keyboard=menu, resize_keyboard=True)
edit_post = InlineKeyboardMarkup(inline_keyboard=post_media_text, resize_keyboard=True)
post_setting = InlineKeyboardMarkup(inline_keyboard=post_setting_ready, resize_keyboard=True)
post_confirmation = InlineKeyboardMarkup(inline_keyboard=post_publication_confirm, resize_keyboard=True)

post_dates = InlineKeyboardMarkup(inline_keyboard=post_dates_btn, resize_keyboard=True)


add_channel = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="+ Добавить новый канал", callback_data="add_channel")]])

check_sub = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Проверить подписку", callback_data="check_sub")]])
buy_sub = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Купить подписку", callback_data="buy_sub")], [InlineKeyboardButton(text="◀️ Выйти в меню", callback_data="menu")]])

exit_kb = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="◀️ Выйти в меню")]], resize_keyboard=True)
iexit_kb = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="◀️ Выйти в меню", callback_data="menu")]])