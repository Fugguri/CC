
from aiogram import types
from utils.exel import houses
from main import db


async def start_kb():

    kb = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=4)
    kb.add(
        types.KeyboardButton(text="Дома"),
        types.KeyboardButton(text="Жители"),
        types.KeyboardButton(text="Собрания"),
        types.KeyboardButton(text="Посты")
    )
    return kb


async def posts_menu_kb():
    kb = types.InlineKeyboardMarkup(row_width=1)
    kb.add(types.InlineKeyboardButton(
        text="Реестр сообщений", callback_data="post registry"),
        types.InlineKeyboardButton(
        text="Создать/редактировать сообщение", callback_data="new post"),
    )
    return kb


async def email_kb():
    kb = types.InlineKeyboardMarkup(row_width=1)
    kb.add(types.InlineKeyboardButton(
        text="Да", callback_data="confirm email"),
        types.InlineKeyboardButton(
        text="Изм.эмейл", callback_data="edit email"),
        types.InlineKeyboardButton(
        text="Без эмэйла", callback_data="no email"),
    )
    return kb


async def registry_kb():
    kb = types.InlineKeyboardMarkup(row_width=1)
    kb.add(types.InlineKeyboardButton(
        text="Добавить новый дом", callback_data="add flat"),
        # types.InlineKeyboardButton(
        # text="Показать список домов", callback_data="house list"),
        types.InlineKeyboardButton(
        text="Добавить реестр собственников", callback_data="add onwer"),
        types.InlineKeyboardButton(
        text="QR-код дома", callback_data="qrcode")
    )
    return kb


async def back_kb():
    kb = types.InlineKeyboardMarkup(row_width=2)
    kb.add(types.InlineKeyboardButton(
        text="Назад", callback_data="back"))
    return kb


async def posts_kb(posts):
    kb = types.InlineKeyboardMarkup(row_width=1)
    for post in posts:
        kb.add(types.InlineKeyboardButton(
            text=post[2],
            callback_data=post[0]
        ))
    return kb


async def meeting_kb():
    kb = types.InlineKeyboardMarkup(row_width=2)
    kb.add(types.InlineKeyboardButton(text="Новое собрание",
                                      callback_data="new_meeting"),
           types.InlineKeyboardButton(text="Список собраний",
                                      callback_data="current_meeting"),
           types.InlineKeyboardButton(text="Удалить собрание",
                                      callback_data="delete_meeting"))
    return kb


async def meeting_list_kb(meetings):
    kb = types.InlineKeyboardMarkup(row_width=2)
    for meeting in meetings:
        text = f"ОСС № {meeting[1]} (c {meeting[2]} по {meeting[3]})"
        kb.add(types.InlineKeyboardButton(
            text=text,
            callback_data=meeting[0]
        ))
    return kb


async def tenant_status_kb():
    kb = types.InlineKeyboardMarkup(row_width=3)
    kb.add(types.InlineKeyboardButton(
        text="Собственник",
        callback_data="owner"
    ))
    kb.add(types.InlineKeyboardButton(
        text="Представитель",
        callback_data="representer"
    ))
    kb.add(types.InlineKeyboardButton(
        text="Квартирант/Арендатор",
        callback_data="renter"
    ))
    return kb


async def schoise_kb():
    kb = types.InlineKeyboardMarkup(row_width=2)
    kb.add(types.InlineKeyboardButton(
        text="Да", callback_data="yes"), types.InlineKeyboardButton(
        text="Нет", callback_data="no"))
    return kb


async def houses_kb():
    kb = types.InlineKeyboardMarkup(row_width=2)
    for house in db.all_houses():
        name = house[1].replace("г.Санкт-Петербург, ", "")
        index = house[2]
        kb.add(types.InlineKeyboardButton(
            text=name, callback_data=index))
    return kb


async def voting_kb(is_active=True):
    kb = types.InlineKeyboardMarkup(row_width=2)
    if is_active:
        kb.add(types.InlineKeyboardButton(
            text="Остановить голосование", callback_data="stop_voting"),
            types.InlineKeyboardButton(
            text="Назад", callback_data="back"))
    else:
        kb.add(types.InlineKeyboardButton(
            text="Запустить голосование", callback_data="start_voting"),
            types.InlineKeyboardButton(
            text="Назад", callback_data="back"))
    kb.add(types.InlineKeyboardButton(
        text="Скачать шаблон-бюллетень", callback_data="send bulleten"))
    kb.add(types.InlineKeyboardButton(
        text="Скачать сообщение о собрании", callback_data="send notification"))
    return kb


async def owners_kb(owners):
    kb = types.InlineKeyboardMarkup(row_width=2)
    for owner in owners:
        print(owner)
        full_name = f"{owner[7]} {owner[8]} {owner[9]} ({owner[18]}%)"
        index = owner[0]
        kb.add(types.InlineKeyboardButton(
            text=full_name, callback_data=index))
    return kb


async def edit_tenant_kb():
    kb = types.InlineKeyboardMarkup(row_width=2)
    kb.add(
        types.InlineKeyboardButton(
            text="Изменить имя",
            callback_data="change name"),
        types.InlineKeyboardButton(
            text="Изменить номер телефона",
            callback_data="change phone"),
        types.InlineKeyboardButton(
            text="Изменить email",
            callback_data="change email"))
    kb.add(types.InlineKeyboardButton(
        text="Изменить статус",
        callback_data="change status"),
        types.InlineKeyboardButton(
        text="Изменить собственника",
        callback_data="change owner"),
        types.InlineKeyboardButton(
        text="Удалить жителя",
        callback_data="delete_tenant"),
        types.InlineKeyboardButton(
        text="В меню",
        callback_data="back"))
    return kb


async def edit_tenant_status_kb():
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton(
        text=f"Собственник",
        callback_data="Собственник"),
        types.InlineKeyboardButton(
        text=f"Представитель",
        callback_data="Представитель"),
        types.InlineKeyboardButton(
        text=f"Выехал",
        callback_data="Выехал"),
        types.InlineKeyboardButton(
        text=f"Квартирант/Арендатор",
        callback_data="Квартирант/Арендатор"),
        types.InlineKeyboardButton(
        text=f"Назад",
        callback_data="back"),
    )
    return kb


async def edit_tenant_tenants_kb(tenants):
    kb = types.InlineKeyboardMarkup()
    for tenant in tenants:
        kb.add(types.InlineKeyboardButton(
            text=f"{tenant[1]} ({tenant[3]})",
            callback_data=tenant[0]))
    return kb


async def tenants_menu_kb():
    kb = types.InlineKeyboardMarkup(row_width=2)
    kb.add(
        types.InlineKeyboardButton(
            text="Новый житель",
            callback_data="add tenant"),
        types.InlineKeyboardButton(
            text="Список жителей",
            callback_data="tenants list"))
    kb.add(types.InlineKeyboardButton(
        text="Редактировать жителя",
        callback_data="edit tenant"),
        types.InlineKeyboardButton(
        text="Другой адрес дома",
        callback_data="change address"))
    return kb
