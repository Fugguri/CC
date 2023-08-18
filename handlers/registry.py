import datetime
from aiogram import types
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text

from keyboards.keyboards import start_kb, registry_kb, back_kb, houses_kb, schoise_kb

from main import dp, bot, db, wa
from utils import generate_qrcode, generate_short_link

from utils.exel import exel_reader
from utils.texts import Texts
texts = Texts()
cur_cad_num = ""


class AddWord(StatesGroup):
    number = State()
    add_registry = State()
    add_onwer = State()
    add_flat = State()
    get_file = State()
    update_house = State()
    want_add_tenants = State()
    qrcode = State()


user_filename = {}
user_file_id = {}
user_info_message = {}


@dp.message_handler(Text("Дома"), state="*")
async def add_user(message: types.Message):
    text = "Список домов:"
    houses = db.get_all_houses()
    if houses:
        for house in houses:
            filing = db.get_house_filling(house[3], house[4], house[5])
            if filing and filing[5] and datetime.datetime.today() > datetime.datetime.strptime(filing[5], "%d.%m.%Y"):
                db.update_meeting_status("ЗАКОНЧЕНО", name=filing[3])
                filing = db.get_house_filling(house[3], house[4], house[5])
            if filing and filing[0]:
                flats = filing[0]
            else:
                flats = "Нет"

            if filing and filing[1]:
                owners_count = filing[1]
            else:
                owners_count = "Нет"
            if filing and filing[2]:
                tenants_count = filing[2]
            else:
                tenants_count = "Нет"
            if filing and filing[3] != None:
                meeting = f"\nСобрание №{filing[3]} c {filing[4]} до {filing[5]}\n{filing[6]}"
            else:
                meeting = ''
            text += f"""\nМКД: {house[1]} (КадНом {house[2]}) помещений - {flats}, собственников - {owners_count}, жителей - {tenants_count} {meeting}\n"""
    else:
        text += "Пока нет добавленных домов"
    markup = await registry_kb()
    await message.answer(text, reply_markup=markup)
    await message.delete()


@dp.callback_query_handler(lambda call: call.data == "house list", state="*")
async def houses_list(callback: types.CallbackQuery):
    markup = await houses_kb()
    db.get_houses_list()
    await callback.message.edit_text("Выберите дом, к которому добавляется реестр", reply_markup=markup)

@dp.callback_query_handler(lambda call: call.data == "qrcode", state="*")
async def add_user(callback: types.CallbackQuery):
    markup = await houses_kb()
    await AddWord.qrcode.set()
    await callback.message.edit_text("Выберите дом", reply_markup=markup)
    
    
@dp.callback_query_handler(lambda call: call.data in [i[2] for i in db.all_houses()], state=AddWord)
async def add_owners(callback: types.CallbackQuery, state: State):
    house = db.get_house_by_id(callback.data)
    
    
    link = texts.create_house_link(house)
    short_link = generate_short_link(link)
    image = generate_qrcode(short_link)
    text = texts.create_qr_code_caption(house,short_link)
    
    

    await callback.message.answer_photo(photo=image,caption=short_link) 
    await callback.message.answer(text)
    
    await callback.message.delete()

    

@dp.callback_query_handler(lambda call: call.data == "add onwer", state="*")
async def add_user(callback: types.CallbackQuery):
    markup = await houses_kb()
    await AddWord.add_onwer.set()
    await callback.message.edit_text("Выберите дом, к которому добавляется реестр", reply_markup=markup)


@dp.callback_query_handler(lambda call: call.data in [i[2] for i in db.all_houses()], state=AddWord)
async def add_owners(callback: types.CallbackQuery, state: State):
    markup = await back_kb()
    if callback.data != "yes":
        global cur_cad_num
        await AddWord.get_file.set()
        cur_cad_num = callback.data
    owners = db.get_all_owners(cur_cad_num)
    if owners:
        await callback.message.edit_text(f"""Внимание! По этому адресу уже загружено {len(owners)} собственник. Хотите продолжить загрузку собственников?\nЗагрузите excel-файл с реестром всех собственников в доме.
Шаблон файла запросите по ссылке @ShkolaUpravdoma""", reply_markup=markup)
        return
    await callback.message.edit_text("""Загрузите excel-файл с реестром всех собственников в доме.
Шаблон файла запросите по ссылке @ShkolaUpravdoma""", reply_markup=markup)


@dp.message_handler(content_types=[types.ContentType.DOCUMENT], state=AddWord.add_onwer)
async def receiving_owner_registry(message: types.Message):
    markup = await houses_kb()
    await message.answer("Внимание! Вы не выбрали адрес дома для ввода реестра собственников", reply_markup=markup)


@dp.message_handler(content_types=[types.ContentType.DOCUMENT], state=AddWord.get_file)
async def receiving_owner_registry(message: types.Message, state: State):
    filename = message.document.file_name
    await message.document.download(destination_file="documents/"+filename)
    mes = await message.answer("Загружаю собственников. Это может занять некоторое время")
    # try:
    result = await exel_reader(f"./documents/{filename}", "Реестр")
    for res in result:
        db.add_owner(cur_cad_num,
                     res[0],
                     res[1],
                     res[2],
                     res[3],
                     res[4],
                     res[5],
                     res[6],
                     res[7],
                     res[8],
                     res[9],
                     res[10],
                     res[11],
                     res[12],
                     res[13],
                     res[14],
                     res[15],
                     res[16],
                     res[17],
                     res[18],
                     res[19],
                     res[20],
                     res[21],
                     res[22],
                     res[23],
                     res[24],
                     res[25],
                     res[26],
                     res[27],
                     res[28],
                     res[29],
                     res[30],
                     res[31],
                     )
    house = db.get_house_by_cad_num(cur_cad_num)
    markup = await schoise_kb()
    info_message = user_info_message[message.from_user.id]
    print(info_message, info_message.from_user.id)
    await info_message.edit_text(f"""Добавлены собственники по адресу: 
{house[0]} (КадНом {cur_cad_num})
Помещений - {house[1]}. Загружнено собственников - {len(result)}.""")
    await message.answer("Хотите добавить жителей?", reply_markup=markup)
    await AddWord.want_add_tenants.set()
    # except Exception as ex:
    #     print(ex)
    #     await message.answer(ex+" Обратитесь к администратору")
    await mes.delete()
    await message.delete()


@dp.callback_query_handler(lambda call: call.data == "add flat", state="*")
async def add_user(callback: types.CallbackQuery):
    markup = await back_kb()
    await AddWord.add_flat.set()
    await callback.message.edit_text("""Загрузите excel-файл со всеми помещениями дома.
Шаблон файла запросите по ссылке @ShkolaUpravdoma""", reply_markup=markup)


@dp.callback_query_handler(state=AddWord.update_house)
async def update_flat(callback: types.CallbackQuery, state=State):
    if callback.data == "yes":
        filename = user_filename[callback.from_user.id]
        file_id = user_file_id[callback.from_user.id]
        await bot.download_file_by_id(file_id, destination="documents/"+filename)
        # await callback.message.document.download(destination_file="documents/"+filename)
        mes = await callback.message.answer("Загружаю помещения. Это может занять некоторое время")
        try:
            result = await exel_reader(f"./documents/{filename}", "Помещения")
            print(result)
            for i in result:
                db.add_house_data(result[0][5], i[1], i[2],
                                  i[3], i[4], i[5], i[6], i[7], i[8], i[9])
            owners = db.get_all_owners(result[0][5])
            markup = await schoise_kb()
            user_info = await callback.message.edit_text(f"""Добавлен реест помещений для адреса: 
    МКД: {result[0][2]} (КадНом {result[0][5]}) \nпомещений - {len(result)} \nсобственников - {len(owners)}""",)
            user_info_message[callback.from_user.id] = user_info

            global cur_cad_num
            cur_cad_num = result[0][5]
            await callback.message.answer(f"""Хотите занести собственников в этом доме?""", reply_markup=markup)
            await AddWord.add_flat.set()
        except Exception as ex:
            print(ex)
            markup = await back_kb()
            await callback.message.edit_text("Убедитесь, что отправлен эксель файл и попробуйте заново", reply_markup=markup)
        finally:
            await mes.delete()

    else:
        from .handlers import back
        await back(callback.message, state)


@dp.message_handler(content_types=[types.ContentType.DOCUMENT], state=AddWord.add_flat)
async def receiving_owner_registry(message: types.Message, state: State):
    filename = message.document.file_name
    await message.document.download(destination_file="documents/"+filename)

    mes = await message.answer("Загружаю помещения. Это может занять некоторое время")
    global user_info_message

    try:
        result = await exel_reader(f"./documents/{filename}", "Помещения")

        if db.get_house_by_cad_num(result[0][5]):
            markup = await schoise_kb()
            await message.answer("Внимание, такой дом с помещениями уже существует. Хотите продолжить?", reply_markup=markup)
            global user_filename
            user_filename[message.from_user.id] = filename
            user_file_id[message.from_user.id] = message.document.file_id
            await AddWord.update_house.set()
            return

        db.add_house(result[0][2], result[0][5], f"house"+result[0]
                     [5], "tenants"+result[0][5], "owners"+result[0][5])

        for i in result:
            db.add_house_data(result[0][5], i[1], i[2],
                              i[3], i[4], i[5], i[6], i[7], i[8], i[9])
        owners = db.get_all_owners(result[0][5])
        markup = await schoise_kb()
        message_to_edit = await message.answer(f"""Добавлен реест помещений для адреса: 
МКД: {result[0][2]} (КадНом {result[0][5]}) \nпомещений - {len(result)} \nсобственников - {len(owners)}""",)
        global cur_cad_num
        cur_cad_num = result[0][5]
        await message.answer(f"""Хотите занести собственников в этом доме?""", reply_markup=markup)
    except Exception as ex:
        print(ex)
        markup = await back_kb()
        await message.answer("Убедитесь, что отправлен эксель файл и попробуйте заново", reply_markup=markup)
    finally:
        await message.delete()
        await mes.delete()
        user_info_message[message.from_user.id] = message_to_edit


@dp.callback_query_handler(state=AddWord.add_flat)
async def add_user(callback: types.CallbackQuery, state=State):
    if callback.data == "yes":
        state = await AddWord.get_file.set()
        await add_owners(callback, state)
    else:
        from .handlers import back
        await back(callback.message, state)


@dp.callback_query_handler(state=AddWord.want_add_tenants)
async def add_user(callback: types.CallbackQuery, state=State):
    if callback.data == "yes":
        await state.finish()
        from .add_tenant import imput_number_of_house
        await imput_number_of_house(callback, cur_cad_num)
    else:
        from .handlers import back
        await back(callback.message, state)
