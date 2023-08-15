from docx import Document
from aiogram import types
import datetime
from main import dp, bot, db, wa
from aiogram.dispatcher.filters.state import State, StatesGroup
from keyboards.keyboards import start_kb, registry_kb, back_kb, houses_kb, meeting_kb, schoise_kb, meeting_list_kb, voting_kb
from pathlib import Path
from aiogram.dispatcher.filters import Text
from utils.voting import start_voting, send_notification, meeting_notify
import os
import re


class Meeting(StatesGroup):
    new = State()
    current = State()
    adress = State()
    new = State()
    name = State()
    date_of_start = State()
    date_of_end = State()
    bullyuten = State()
    notification = State()
    confirm = State()
    select_meeting = State()
    delete_meeting = State()


cur_house = ""
secretary = {"secretary_full_name": "Грайворонский Никита Сергеевич",
             "secretary_phone": "89669303403",
             "secretary_email": "secretaross@yandex.ru"}
bullyuten = ""
notification = ""


@dp.message_handler(Text("Собрания"), state="*")
async def add_user(message: types.Message, state: State):
    markup = await meeting_kb()
    try:
        await state.finish()
    except:
        pass
    await message.answer("Выберите пункт меню", reply_markup=markup)


@dp.callback_query_handler(lambda call: call.data == "new_meeting", state="*")
async def create_meeting(callback: types.CallbackQuery):
    markup = await houses_kb()
    await Meeting.adress.set()
    await callback.message.answer("Выберите адрес дома для создания собрания", reply_markup=markup)


@dp.callback_query_handler(lambda call: call.data in [i[2] for i in db.all_houses()], state=Meeting.adress)
async def imput_number_of_house(callback: types.CallbackQuery, ):
    global cur_house
    cur_house = callback.data
    markup = await back_kb()
    await Meeting.name.set()
    await callback.message.answer("Введите номер собрания", reply_markup=markup)


@dp.message_handler(state=Meeting.name)
async def new_meeting_data(message: types.Message):
    markup = await back_kb()
    global secretary
    secretary["name"] = message.text
    await Meeting.date_of_start.set()
    await message.answer("Введите дату начала собрания\n\
Формат даты: дд-мм-гггг", reply_markup=markup)


@dp.message_handler(state=Meeting.date_of_start)
async def new_meeting_data(message: types.Message):
    match = re.fullmatch(
        r'(\d+(/|-|.){1,2}\d+(/|-|.){1,2}\d{2,4})', message.text)
    markup = await back_kb()
    input_date = message.text.replace(
        "-", ".").replace(",", ".").replace("/", ".")
    input_date = input_date.split(".")
    try:
        if len(input_date[2]) == 2:
            input_date[2] = "20"+input_date[2]
        input_date = ".".join(input_date)
        datetime.datetime.strptime(input_date, "%d.%m.%Y")
        date = True
    except:
        date = False

    if not match or not date:
        await message.answer("Введена некорректная дата.Попробуйте заново\n\
Формат даты: дд-мм-гггг", reply_markup=markup)
        return
    global secretary
    secretary["date_of_start"] = input_date
    await Meeting.new.set()
    await message.answer("Введите дату окончания собрания\n\
Формат даты: дд-мм-гггг", reply_markup=markup)


@dp.message_handler(state=Meeting.new)
async def new_meeting_data(message: types.Message):
    match = re.fullmatch(
        r'(\d+(/|-|.){1,2}\d+(/|-|.){1,2}\d{2,4})', message.text)
    markup = await back_kb()
    input_date = message.text.replace(
        "-", ".").replace(",", ".").replace("/", ".")
    input_date = input_date.split(".")
    try:
        if len(input_date[2]) == 2:
            input_date[2] = "20"+input_date[2]
        input_date = ".".join(input_date)
        # datetime.datetime.strptime(input_date, "%d.%m.%Y")
        date = True
    except:
        date = False
    if not match or not date:
        await message.answer("Введена некорректная дата.Попробуйте заново\n\
Формат даты: дд-мм-гггг", reply_markup=markup)
        return
    global secretary
    secretary["date_of_end"] = input_date
    await message.answer(text=f'''Проверьте данные:
Номер собрания: {secretary["name"]}
Дата начала: {secretary["date_of_start"]}
Дата окончания: {secretary["date_of_end"]}
ФИО секретаря: {secretary["secretary_full_name"]}
Телефон секретаря: {secretary["secretary_phone"]}
email секретаря: {secretary["secretary_email"]}
Если все верно - загрузите шаблон бюллетеня для голосования''',
                         reply_markup=markup)
    await Meeting.bullyuten.set()


@dp.message_handler(content_types=[types.ContentType.DOCUMENT], state=Meeting.bullyuten)
async def new_meeting_data(message: types.Message):
    filename = message.document.file_name
    global bullyuten
    house = db.get_current_house(cur_house)[1]
    bullyuten = "#_{}_{}_бюллетень.docx".format(secretary["name"], house)
    await message.document.download(destination_file="documents/#_{}_{}_бюллетень.docx".format(secretary["name"], house))

    markup = await back_kb()
    await message.answer(f"Загрузите файл сообщения о собрании № {secretary['name']}", reply_markup=markup)
    await Meeting.notification.set()


@dp.message_handler(content_types=[types.ContentType.DOCUMENT], state=Meeting.notification)
async def new_meeting_data(message: types.Message):
    filename = message.document.file_name
    global notification
    house = db.get_current_house(cur_house)[1]
    notification = "#_{}_{}_сообщение.pdf".format(secretary["name"], house)
    await message.document.download(destination_file="documents/#_{}_{}_сообщение.pdf".format(secretary["name"], house))
    db.add_meeting(secretary["name"],
                   secretary["date_of_start"],
                   secretary["date_of_end"],
                   secretary["secretary_full_name"],
                   secretary["secretary_phone"],
                   secretary["secretary_email"],
                   bullyuten,
                   notification,
                   cur_house,
                   f"tenants{cur_house}",
                   f"owners{cur_house}",
                   "СОЗДАНО")

    markup = await schoise_kb()
    meeting = db.get_meeting(secretary["name"])
    receivers = db.get_receivers(meeting[0])
    for receiver in receivers:
        await wa.send_voting_notification(receiver)
        print(receiver)
    await Meeting.confirm.set()
    await message.answer(f"Собрание создано.Уведомления разосланы.\nЗапустить голосование?", reply_markup=markup)


@dp.callback_query_handler(state=Meeting.confirm)
async def new_meeting_data(callback: types.CallbackQuery, state: State):
    meeting = db.get_meeting_by_name(secretary["name"])
    receivers = db.get_receivers(meeting[0])
    if callback.data == "yes":
        await start_voting(receivers, callback.message, meeting)
        db.update_meeting_status("ИДЕТ ГОЛОСОВАНИЕ", name=secretary["name"])
        markup = await back_kb()
        await callback.message.answer(f'Голосование на ОСС {secretary["name"]} запущено, рассылаются эл.бюллетени на емайл указанный жильцом (собственники/представители)', reply_markup=markup)
    if callback.data == "no":
        markup = await meeting_kb()
        await callback.message.answer("Голосование создано, но не напущено. Можете создать новое или перейти к списку существующих.", reply_markup=markup)
        await state.finish()


@dp.callback_query_handler(lambda call: call.data == "current_meeting", state="*")
async def current_meet(callback: types.CallbackQuery):
    meetings = db.get_all_meetings()
    if len(meetings) == 0:
        markup = await back_kb()
        await callback.message.answer("Нет собраний", reply_markup=markup)
    else:
        markup = await meeting_list_kb(meetings)
        await Meeting.select_meeting.set()
        await callback.message.answer("Выберите собрание", reply_markup=markup)
        await Meeting.select_meeting.set()

cur_meet_id = ""


@dp.callback_query_handler(lambda call: call.data == "delete_meeting")
async def delete_meeting(callback: types.CallbackQuery):
    meetings = db.get_all_meetings()
    if len(meetings) == 0:
        markup = await back_kb()
        await callback.message.answer("Нет собраний", reply_markup=markup)
    else:
        markup = await meeting_list_kb(meetings)
        await Meeting.delete_meeting.set()
        await callback.message.answer("Выберите собрание для удаления", reply_markup=markup)


@dp.callback_query_handler(state=Meeting.delete_meeting)
async def delete_meet(callback: types.CallbackQuery):
    meeting = db.get_meeting_by_id(callback.data)
    os.system(f"rm documents/'{meeting[7]}'")
    os.system(f"rm documents/'{meeting[8]}'")
    db.delete_meeting(callback.data)
    meetings = db.get_all_meetings()
    if len(meetings) == 0:
        markup = await back_kb()
        await callback.message.answer("Нет собраний, которые можно удалить", reply_markup=markup)
    else:
        markup = await meeting_list_kb(meetings)
        await Meeting.delete_meeting.set()
        await callback.message.answer("Удалено.\nВыберите собрание для удаления", reply_markup=markup)


@dp.callback_query_handler(lambda call: call.data == "send bulleten",)
async def show_meeting(callback: types.CallbackQuery):
    markup = await back_kb()
    meeting_data = db.get_meeting_by_id(cur_meet_id)
    with open("documents/"+meeting_data[7], "rb") as file:
        await callback.message.answer_document(file, reply_markup=markup)


@dp.callback_query_handler(lambda call: call.data == "send notification")
async def show_meeting(callback: types.CallbackQuery):
    markup = await back_kb()
    meeting_data = db.get_meeting_by_id(cur_meet_id)
    with open("documents/"+meeting_data[8], "rb") as file:
        await callback.message.answer_document(file, reply_markup=markup)


@dp.callback_query_handler(lambda call: call.data == "start_voting")
async def show_meeting(callback: types.CallbackQuery):
    markup = await back_kb()
    receivers = db.get_receivers(cur_meet_id)
    meeting_data = db.get_meeting_by_id(cur_meet_id)
    await callback.message.answer("Голосование запущено")
    try:
        await start_voting(receivers, callback.message, meeting_data)
        await callback.message.answer("Сообщения и эмейлы разосланы", reply_markup=markup)
        db.update_meeting_status("ГОЛОСОВАНИЕ ИДЕТ", id=cur_meet_id)
    except Exception as ex:
        await callback.message.answer(ex, reply_markup=markup)


@dp.callback_query_handler(state=Meeting.select_meeting)
async def show_meeting(callback: types.CallbackQuery, state=State):
    meeting = db.get_meeting_by_id(callback.data)[1:]
    markup = await voting_kb(False)
    global cur_meet_id
    cur_meet_id = callback.data
    date = meeting[2].replace("/", ".").replace(",", ".").replace("-", ".")
    if datetime.datetime.strptime(date, "%d.%m.%Y") < datetime.datetime.today():
        markup = await voting_kb(False)
        db.update_meeting_status("ЗАКОНЧЕНО", id=cur_meet_id)
        meeting = db.get_meeting_by_id(callback.data)[1:]
    print(meeting)
    text = f"""Собрание № {meeting[0]} (Статус: {meeting[-9]})
<b>Адрес дома:</b> {meeting[-1]}
<b>Начало</b> {meeting[1]} <b>Окончание</b> {meeting[2]}

<b>ФИО секретаря:</b> {meeting[3]}
<b>Телефон секретаря:</b> {meeting[4]}
<b>E-mail секретаря:</b> {meeting[5]}"""
    await callback.message.answer(text, reply_markup=markup)
    await state.finish()
