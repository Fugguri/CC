from aiogram import types
from main import dp, bot, db, wa, texts
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from keyboards.keyboards import start_kb, edit_tenant_kb, back_kb, houses_kb, schoise_kb, owners_kb, tenant_status_kb, tenants_menu_kb, email_kb, edit_tenant_tenants_kb, edit_tenant_status_kb
import datetime
from utils.exel import create_tenants_exel
import os
import re


class Add_tenant(StatesGroup):
    adress = State()
    full_name = State()
    status = State()
    phone = State()
    create_tetants_exel = State()
    select_owner = State()
    email = State()
    tenants_list = State()
    add_new_tenant = State()
    update_phone = State()
    representative = State()
    select_address = State()
    number_of_house = State()
    edit_tenant_flat = State()
    edit_tenant_select_tenant = State()
    edit_tenant_name = State()
    edit_tenant_email = State()
    edit_tenant_phone = State()
    edit_tenant_owner = State()
    edit_tenant_status = State()
    delete_tenant = State()


tenants = {}
cur_house = ""
car_name = ""
cur_flat_num = ""
cur_owner = ""
cur_number = ""
cur_owner_email = ""
cur_status = ""
cur_email = ""
cur_phone = ""
cur_address = ""
cur_has_watsapp = ""
cur_edited_tenant_id = ""


@dp.callback_query_handler(lambda call: call.data == "change address", state="*")
@dp.message_handler(Text("Жители"), state="*")
async def add_tenant_start(message: types.Message):
    markup = await houses_kb()
    await Add_tenant.select_address.set()
    try:
        try:
            await message.message.edit_text("Выберите адрес дома", reply_markup=markup)
        except:
            await message.message.answer("Выберите адрес дома", reply_markup=markup)
    except Exception as ex:
        print(ex)
        await message.answer(text="Выберите адрес дома", reply_markup=markup)


@dp.callback_query_handler(lambda call: call.data in [i[2] for i in db.all_houses()], state=Add_tenant.select_address)
async def confirm_address(callback: types.CallbackQuery, re_cad_num=None):
    global cur_house
    if re_cad_num != None:
        cur_house = re_cad_num
    elif callback.data == "add tenant" and re_cad_num == None:
        pass
    elif callback.data == "delete_tenant" and re_cad_num == None:
        pass
    elif callback.data == "change owner" and re_cad_num == None:
        pass
    elif callback.data == "change status" and re_cad_num == None:
        pass
    elif callback.data == "change email" and re_cad_num == None:
        pass
    elif callback.data == "change phone" and re_cad_num == None:
        pass
    elif callback.data == "change name" and re_cad_num == None:
        pass
    else:
        cur_house = callback.data
    markup = await tenants_menu_kb()
    await Add_tenant.select_address.set()
    try:
        await callback.edit_text("Выберите пункт меню", reply_markup=markup)
    except:
        await callback.message.edit_text("Выберите пункт меню", reply_markup=markup)


@dp.callback_query_handler(lambda call: call.data == "tenants list", state="*")
async def tenants_list(callback: types.CallbackQuery):
    markup = await back_kb()

    cur_address = db.get_current_house(cur_house)[1]
    tenants = db.get_tenants_for_exel(cur_house)
    flats = db.get_flats_for_exel(cur_house)
    markup = await tenants_menu_kb()

    if tenants == []:
        await callback.message.answer("Еще нет жителей в этом доме")
    else:
        mes = await callback.message.answer("Формирую, подождите немного.")
        try:
            await create_tenants_exel(f'./exel/Жители_{cur_address}.xlsx', tenants, flats)
            with open(f'./exel/Жители_{cur_address}.xlsx', "rb") as file:
                await callback.message.answer_document(file, reply_markup=markup)
                await callback.message.delete()
            os.remove(f'exel/Жители_{cur_address}.xlsx')
        except Exception as ex:
            await callback.message.answer(f"Произошла ошибка {ex}")
        finally:
            await mes.delete()


async def add_tenant(message: types.Message):
    markup = await houses_kb()
    await message.answer("Выберите адрес, который вас интересует.", reply_markup=markup)
    await Add_tenant.adress.set()


@dp.callback_query_handler(lambda call: call.data == "back", state=Add_tenant.full_name)
@dp.callback_query_handler(lambda call: call.data == "back", state=Add_tenant.number_of_house)
@dp.callback_query_handler(lambda call: call.data == "back", state=Add_tenant.phone)
@dp.callback_query_handler(lambda call: call.data == "change_flat", state=Add_tenant.add_new_tenant)
@dp.callback_query_handler(lambda call: call.data == "add tenant", state=Add_tenant.select_address)
async def imput_number_of_house(callback: types.CallbackQuery, re_cad_num=None):
    markup = await back_kb()
    global cur_house
    if callback.data == "add tenant" and re_cad_num == None:
        pass
    elif callback.data == "delete_tenant" and re_cad_num == None:
        pass
    elif callback.data == "change owner" and re_cad_num == None:
        pass
    elif callback.data == "change status" and re_cad_num == None:
        pass
    elif callback.data == "change email" and re_cad_num == None:
        pass
    elif callback.data == "change phone" and re_cad_num == None:
        pass
    elif callback.data == "change name" and re_cad_num == None:
        pass
    elif callback.data == "add tenant" and re_cad_num == None:
        cur_house = callback.data
    else:
        cur_house = re_cad_num

    if callback.data != "change_flat":
        tenants[callback.from_user.id] = {}
        tenants[callback.from_user.id]["date_of_create"] = datetime.datetime.today(
        ).strftime("%Y.%m.%d, %H:%M")
        tenants[callback.from_user.id]["mkd_id"] = cur_house.replace(
            ":", "")
        try:
            tenants[callback.from_user.id]["cad_num"] = cur_house
        except:
            pass
        tenants[callback.from_user.id]["address"] = db.get_current_house(cur_house)[
            1]
    await callback.message.answer("Введите номер помещения", reply_markup=markup)
    await Add_tenant.number_of_house.set()


@dp.message_handler(state=Add_tenant.number_of_house)
async def confirm_flat(message: types.Message, ):
    pattern = r'[нНYyhHxXчЧРр-]'
    td = db.get_house_data(
        tenants[message.from_user.id]["cad_num"], message.text)
    markup = await back_kb()
    if re.search(pattern, message.text) and not td:
        flats = ''
        for flat in db.get_flat_with_letters(
                tenants[message.from_user.id]["cad_num"]):
            flats += "\n"+flat[0]
        await message.answer("Не нашелся такой номер помещения. Вы можете выбрать из следующих.{} \nПросто скопируйте номер помещения ".format(flats), reply_markup=markup)
        return

    if not td:
        await message.answer("Такого номера нет в реестре помещений. \
            Попробуйте еще раз.", reply_markup=markup)
        return
    tenants[message.from_user.id]["flat_num"] = message.text
    tenants[message.from_user.id]["flat_id"] = td[5].replace(":", "")
    tenants[message.from_user.id]["flat_status"] = td[1]
    markup = await schoise_kb()
    text = f"""КВ {td[3]}  ({td[4]} м2 - {td[5]})\n"""
    owners = db.get_owners(
        tenants[message.from_user.id]["cad_num"], tenants[message.from_user.id]["flat_num"])
    for owner in owners:
        text += f"{owner[7]} {owner[8]} {owner[9]} ({owner[18]}%)\n"
    await message.answer(text, reply_markup=markup)


@dp.callback_query_handler(lambda call: call.data in ["yes", "no"], state=Add_tenant.number_of_house)
async def input_name(callback: types.CallbackQuery, state: State):
    if callback.data == "yes":
        markup = await back_kb()
        await callback.message.answer("Введите имя жителя", reply_markup=markup)
        await Add_tenant.full_name.set()
    if callback.data == "no":
        await add_tenant(callback.message)


@dp.message_handler(state=Add_tenant.full_name)
async def imput_full_name(message: types.Message, ):

    tenants[message.from_user.id]["name"] = message.text

    markup = await back_kb()
    await message.answer("Введите номер телефона жителя", reply_markup=markup)
    await Add_tenant.phone.set()


@dp.message_handler(state=Add_tenant.phone)
async def imput_full_name(message: types.Message, ):
    phone = message.text
    phone = phone.replace(" ", "")
    phone = phone.replace("-", "")
    phone = phone.replace("+", "")
    if phone.startswith("8"):
        phone = "7"+phone[1:]
    tenants[message.from_user.id]["phone"] = phone

    if 10 >= len(phone) <= 11:
        await message.answer("Проверьте номер телефона. Возможно в нем лишние цифры")
        return
    tenant_by_phone = db.get_tenant_by_phone(
        tenants[message.from_user.id]["cad_num"], phone)

    if tenant_by_phone:
        markup = await back_kb()
        markup.add(types.InlineKeyboardButton(
            text="Редактировать", callback_data="edit tenant"))
        await message.answer(f"""ВНИМАНИЕ! Такой телефон уже есть в списке жителей этого дома:
КВ {tenant_by_phone[2]} {tenant_by_phone[5]} ( {tenant_by_phone[8]} - ФИО: {tenant_by_phone[9]} - {tenant_by_phone[16]}% ) {tenant_by_phone[6]} W({tenant_by_phone[7]}) {tenant_by_phone[10]}
Введите другой номер телефона во избежание появления путаницы!""", reply_markup=markup)
        return
    all_tenants = db.get_tenant_by_phone_in_all_house(
        tenants[message.from_user.id]["cad_num"], phone)
    print(all_tenants)
    text = ""
    for i in all_tenants:
        text += f"""ВНИМАНИЕ! Такой телефон уже есть в списке жителей дома с адресом {i[-3]}:
КВ {i[2]} {i[5]} ( {i[8]} - ФИО: {i[9]} - {i[16]}% ) {i[6]} W({i[7]}) {i[10]}\n\n"""
    if text != "":
        await message.answer(text)
    markup = await tenant_status_kb()
    await message.answer("Выберите статус жителя", reply_markup=markup)
    await Add_tenant.status.set()


@dp.callback_query_handler(state=Add_tenant.status)
async def imput_phone(callback: types.CallbackQuery, ):
    global cur_status
    if callback.data == "renter":
        cur_status = "Квартирант/Арендатор"
    if callback.data == "owner":
        cur_status = "Собственник"
    if callback.data == "representer":
        cur_status = "Представитель"
        tenants[callback.from_user.id]["status"] = cur_status
        await callback.message.answer("Введите ФИО представителя")
        await Add_tenant.representative.set()
        return
    tenants[callback.from_user.id]["status"] = cur_status

    owners = db.get_owners(
        tenants[callback.from_user.id]["cad_num"], tenants[callback.from_user.id]["flat_num"])
    markup = await owners_kb(owners)
    if len(owners) == 1:
        tenants[callback.from_user.id]["owner"] = owners[0][0]
        await imput_email(callback)
        return
    await callback.message.answer("Выберите ФИО собственника", reply_markup=markup)
    await Add_tenant.select_owner.set()


@dp.message_handler(state=Add_tenant.representative)
async def set_representative(message: types.Message):
    tenants[message.from_user.id]["representative"] = message.text
    owners = db.get_owners(
        tenants[message.from_user.id]["cad_num"], tenants[message.from_user.id]["flat_num"])
    markup = await owners_kb(owners)
    if len(owners) == 1:
        tenants[message.from_user.id]["owner"] = owners[0][0]
        await imput_email(message)
        return
    await message.answer("Выберите ФИО собственника", reply_markup=markup)
    await Add_tenant.select_owner.set()


@dp.callback_query_handler(lambda call: call.data == "edit email", state=Add_tenant.email)
@dp.callback_query_handler(state=Add_tenant.select_owner)
async def imput_email(callback: types.CallbackQuery, ):
    if callback.data not in ["renter", "owner", "representer"] and callback.data != "edit email":
        tenants[callback.from_user.id]["owner"] = callback.data

    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(
        text="Без эмейла",
        callback_data="no email")
    )
    owner = db.get_owner(tenants[callback.from_user.id]
                         ["cad_num"], tenants[callback.from_user.id]["owner"])
    tenants[callback.from_user.id]["fraction_part"] = owner[18]
    tenants[callback.from_user.id]["owner_full_name"] = owner[7] + \
        " " + owner[8]+" " + owner[9]

    await callback.message.answer(f"""Введите email собственника КВ {tenants[callback.from_user.id]["flat_num"]}:
{tenants[callback.from_user.id]["owner_full_name"]} ({tenants[callback.from_user.id]["fraction_part"]} %)
или нажмите [оставьте без эмейла]""", reply_markup=markup)
    await Add_tenant.email.set()


@dp.callback_query_handler(lambda call: call.data == "no email", state=Add_tenant.email)
async def no_email(callback: types.CallbackQuery):
    global cur_email
    cur_email = ""
    tenants[callback.from_user.id]["owner_email"] = ""
    owner = db.get_owner(tenants[callback.from_user.id]
                         ["cad_num"], tenants[callback.from_user.id]["owner"])
    tenants[callback.from_user.id]["fraction_part"] = owner[18]
    try:
        representative = "ФИО представителя: " + \
            tenants[callback.from_user.id]["representative"]
    except:
        representative = ""

    markup = await schoise_kb()
    markup.add(types.InlineKeyboardButton(
        text="Др.телефон", callback_data="edit phone"))
    if await wa.is_wa_exist(tenants[callback.from_user.id]["phone"]):
        tenants[callback.from_user.id]["has_watsapp"] = "Да"
    else:
        tenants[callback.from_user.id]["has_watsapp"] = "Нет"
    await callback.message.answer(text=f"""{tenants[callback.from_user.id]["name"]} ({tenants[callback.from_user.id]["status"]}) +{tenants[callback.from_user.id]["phone"]} W({tenants[callback.from_user.id]["has_watsapp"]}) 
E-mail: {tenants[callback.from_user.id]["owner_email"]} 
КВ{tenants[callback.from_user.id]["flat_num"]}: {tenants[callback.from_user.id]["owner_full_name"]} ({tenants[callback.from_user.id]["fraction_part"]} %)
{representative}
Все верно?""", reply_markup=markup)


@dp.message_handler(state=Add_tenant.email)
async def confirm_email(message: types.Message):
    tenants[message.from_user.id]["owner_email"] = message.text.replace(
        " ", "")
    if db.check_email(tenants[message.from_user.id]["cad_num"], message.text):
        markup = await email_kb()
        await message.answer("ВНИМАНИЕ! Такой емайл уже есть в списке жителей дома.\
Оставить такой, внести другой емайл или ?", reply_markup=markup)
    else:
        markup = await schoise_kb()
        markup.add(types.InlineKeyboardButton(
            text="Др.телефон", callback_data="edit phone"))
        if await wa.is_wa_exist(tenants[message.from_user.id]["phone"]):
            tenants[message.from_user.id]["has_watsapp"] = "Да"
        else:
            tenants[message.from_user.id]["has_watsapp"] = "Нет"
        try:
            representative = "ФИО представителя: " + \
                tenants[message.from_user.id]["representative"]
        except:
            representative = ""
        await message.answer(text=f"""{tenants[message.from_user.id]["name"]} ({tenants[message.from_user.id]["status"]}) +{tenants[message.from_user.id]["phone"]} W({tenants[message.from_user.id]["has_watsapp"]}) 
E-mail: {message.text} 
КВ{tenants[message.from_user.id]["flat_num"]}: {tenants[message.from_user.id]["owner_full_name"]} ({tenants[message.from_user.id]["fraction_part"]} %)
{representative}
Все верно?""", reply_markup=markup)


@dp.callback_query_handler(lambda call: call.data == "confirm email", state=Add_tenant.email)
async def update_phone_callback(callback: types.CallbackQuery):

    markup = await schoise_kb()
    markup.add(types.InlineKeyboardButton(
        text="Др.телефон", callback_data="edit phone"))

    if await wa.is_wa_exist(tenants[callback.from_user.id]["phone"]):
        tenants[callback.from_user.id]["has_watsapp"] = "Да"
    else:
        tenants[callback.from_user.id]["has_watsapp"] = "Нет"
        try:
            representative = "ФИО представителя: " + \
                tenants[callback.from_user.id]["representative"]
        except:
            representative = ""
    await callback.message.answer(text=f"""{tenants[callback.from_user.id]["name"]} ({tenants[callback.from_user.id]["status"]}) +{tenants[callback.from_user.id]["phone"]} W({tenants[callback.from_user.id]["has_watsapp"]}) 
E-mail: {tenants[callback.from_user.id]["owner_email"]} 
КВ{tenants[callback.from_user.id]["flat_num"]}: {tenants[callback.from_user.id]["owner_full_name"]} ({tenants[callback.from_user.id]["fraction_part"]} %)
{representative}
Все верно?""", reply_markup=markup)


@dp.callback_query_handler(lambda call: call.data == "edit phone", state=Add_tenant.email)
async def update_phone_callback(callback: types.CallbackQuery):
    await Add_tenant.update_phone.set()
    await callback.message.answer("Введите новый номер телефона")


@dp.message_handler(state=Add_tenant.update_phone)
async def update_phone(message: types.Message):
    phone = message.text
    phone = phone.replace(" ", "")
    phone = phone.replace("-", "")
    phone = phone.replace("+", "")
    if phone.startswith("8"):
        phone = "7"+phone[1:]

    tenants[message.from_user.id]["phone"] = phone
    if 10 >= len(phone) <= 11:
        await message.answer("Проверьте номер телефона. Возможно в нем лишние цифры")
        return
    tenant_by_phone = db.get_tenant_by_phone(
        tenants[message.from_user.id]["cad_num"], phone)
    if tenant_by_phone:
        await message.answer(f"""ВНИМАНИЕ! Такой телефон уже есть в списке жителей этого дома:
КВ {tenant_by_phone[2]} {tenant_by_phone[5]} ( {tenant_by_phone[8]} - ФИО: {tenant_by_phone[9]} - {tenant_by_phone[16]}% ) {tenant_by_phone[6]} W({tenant_by_phone[7]}) {tenant_by_phone[10]}
Введите другой номер телефона во избежание появления путаницы!""")
        return
    if tenants[message.from_user.id]["owner_email"] != "":
        email = tenants[message.from_user.id]["owner_email"]
    else:
        email = "Нет"
    markup = await schoise_kb()
    markup.add(types.InlineKeyboardButton(
        text="Др.телефон", callback_data="edit phone"))
    if await wa.is_wa_exist(tenants[message.from_user.id]["phone"]):
        tenants[message.from_user.id]["has_watsapp"] = "Да"
    else:
        tenants[message.from_user.id]["has_watsapp"] = "Нет"
    all_tenants = db.get_tenant_by_phone_in_all_house(
        tenants[message.from_user.id]["cad_num"], phone)
    text = ""
    for i in all_tenants:
        text += f"""ВНИМАНИЕ! Такой телефон уже есть в списке жителей дома с адресом {i[-3]}:
КВ {i[2]} {i[5]} ( {i[8]} - ФИО: {i[9]} - {i[16]}% ) {i[6]} W({i[7]}) {i[10]}\n\n"""
    if text != "":
        await message.answer(text)
    try:
        representative = "ФИО представителя: " + \
            tenants[message.from_user.id]["representative"]
    except:
        representative = ""

    await message.answer(text=f"""{tenants[message.from_user.id]["name"]} \
({tenants[message.from_user.id]["status"]}) +{tenants[message.from_user.id]["phone"]} 
W({tenants[message.from_user.id]["has_watsapp"]}) 
E-mail: {email} 
КВ{tenants[message.from_user.id]["flat_num"]}: {tenants[message.from_user.id]["owner_full_name"]} ({tenants[message.from_user.id]["fraction_part"]} %)
{representative}
Все верно?""", reply_markup=markup)
    await Add_tenant.email.set()


@dp.callback_query_handler(lambda call: call.data in ["yes", "no"], state=Add_tenant.email)
async def redirect(callback: types.CallbackQuery, state: State):
    temp_data = tenants[callback.from_user.id]

    if callback.data == "yes":
        markup = await schoise_kb()
        markup.add(types.InlineKeyboardButton(
            text="Др. квартира", callback_data="change_flat"))
        await Add_tenant.full_name.set()
        try:
            db.update_owner_representative(temp_data["cad_num"],
                                           temp_data["representative"],
                                           temp_data["owner"]
                                           )
        except:
            pass
        db.add_tenant(tenants[callback.from_user.id])
        await wa.send_tenant_wellcome_message(temp_data["name"], temp_data["address"], temp_data["phone"])

        meetings = db.get_meeting_and_tenant_for_notification_by_cad_num(
            temp_data["cad_num"],
            temp_data["name"],
            temp_data["flat_num"],
            temp_data["phone"],
            temp_data["owner_full_name"],
        )
        notify = 0
        if meetings:
            for meeting in meetings:
                date = meeting[3].replace(
                    "/", ".").replace(",", ".").replace("-", ".")
                # return
                if datetime.datetime.today() <= datetime.datetime.strptime(date, "%d.%m.%Y") and tenants[callback.from_user.id]["status"] in ("Собственник", "Представитель"):
                    if tenants[callback.from_user.id]["owner_email"] == "":
                        await wa.mail_voting_notification(meeting)
                        if not notify:
                            await wa.send_no_email(tenants[callback.from_user.id]["name"],
                                                   tenants[callback.from_user.id]["address"],
                                                   tenants[callback.from_user.id]["phone"])
                        notify = 1
                    else:
                        await wa.send_email_and_notify(meeting)
        await callback.message.answer(f"Жилец успешно добавлен в квартиру № {tenants[callback.from_user.id]['flat_num']} \
в доме {tenants[callback.from_user.id]['address']}. \
\nПродолжить добавление жителей в этой квартире ?", reply_markup=markup)
        await Add_tenant.add_new_tenant.set()
        # except Exception as ex:
        #     await callback.message.answer(ex, reply_markup=markup)
    if callback.data == "no":
        markup = await back_kb()
        await callback.message.answer("Введите имя жителя", reply_markup=markup)
        await Add_tenant.full_name.set()


@dp.callback_query_handler(lambda call: call.data in ["yes", "no"], state=Add_tenant.add_new_tenant)
async def redirect(callback: types.CallbackQuery, state: State):
    if callback.data == "yes":
        await input_name(callback, state)
    if callback.data == "no":
        markup = await start_kb()
        await callback.message.answer("Вы в главном меню", reply_markup=markup)


@dp.callback_query_handler(lambda call: call.data == "back", state="*")
async def back(callback: types.CallbackQuery, state: State):
    markup = await start_kb()
    await state.finish()
    await callback.message.answer("Выберите пункт меню", reply_markup=markup)


@dp.callback_query_handler(lambda call: call.data == "edit tenant", state="*")
async def select_fla_for_edit_tenant(callback: types.CallbackQuery, state: State):
    markup = await back_kb()
    await callback.message.answer("Введите номер помещения", reply_markup=markup)
    await Add_tenant.edit_tenant_flat.set()


@dp.message_handler(state=Add_tenant.edit_tenant_flat)
async def edit_tenant_secelt_tenant(message: types.Message):
    cad_num = cur_house
    flat_num = message.text
    global cur_flat_num
    cur_flat_num = flat_num
    tenants = db.get_tenant_by_flat(cad_num, flat_num)
    markup = await edit_tenant_tenants_kb(tenants)
    tenants_text = ''
    for tenant in tenants:
        tenants_text += f"id: {tenant[0]} Имя: {tenant[1]} Телефон: {tenant[2]} Статус: {tenant[3]}\n "
    await message.answer(f"Выберите жителя в квартире {message.text}\n{tenants_text}", reply_markup=markup)
    await Add_tenant.edit_tenant_select_tenant.set()


@dp.callback_query_handler(state=Add_tenant.edit_tenant_select_tenant)
async def edit_tenant_menu(callback: types.CallbackQuery):
    global cur_edited_tenant_id
    if callback.data == "delete_tenant":
        db.delete_tenant(cur_house, cur_edited_tenant_id)
        await callback.message.answer("Житель удален")
        await confirm_address(callback, cur_house)
        return
    if callback.data == "change owner":
        owners = db.get_owners(cur_house, cur_flat_num)
        markup = await owners_kb(owners)
        await callback.message.answer("Выберите нового владельца из списка", reply_markup=markup)
        await Add_tenant.edit_tenant_owner.set()
        return
    if callback.data == "change status":
        markup = await edit_tenant_status_kb()
        await callback.message.answer("Выберите новый статус", reply_markup=markup)
        await Add_tenant.edit_tenant_status.set()
        return
    if callback.data == "change email":
        await callback.message.answer("Введите новый email")
        await Add_tenant.edit_tenant_email.set()
        return
    if callback.data == "change phone":
        await callback.message.answer("Введите новый телефон")
        await Add_tenant.edit_tenant_phone.set()
        return
    if callback.data == "change name":
        await callback.message.answer("Введите новое имя")
        await Add_tenant.edit_tenant_name.set()
        return
    cur_edited_tenant_id = callback.data
    markup = await edit_tenant_kb()
    text = await create_edit_tenant_text()
    await callback.message.answer("Выберите пункт меню\n"+text, reply_markup=markup)


async def create_edit_tenant_text():
    tenant = db.get_tenant_by_id(cur_house, cur_edited_tenant_id)
    text = f"""Данные жителя: 
Имя: {tenant[1]}
Телефон: +{tenant[2]} WA({tenant[8]})
email: {tenant[3]}
Собственник: {tenant[4]}
Адрес: {tenant[5]}
Номер кв: {tenant[6]}
Статус: {tenant[7]}
    """
    return text


@dp.callback_query_handler(state=Add_tenant.edit_tenant_owner)
async def edit_tenant_menu(callback: types.CallbackQuery):
    try:
        owner_id = callback.data
        owner_data = db.get_owner(cur_house, owner_id)
        full_name = f"{owner_data[7]} {owner_data[8]} {owner_data[9]} "
        db.update_tenant_owner(
            cur_house, cur_edited_tenant_id, owner_id, full_name)
        await callback.message.answer("Успено обновлено!")
        text = await create_edit_tenant_text()
        markup = await edit_tenant_kb()
        await Add_tenant.edit_tenant_select_tenant.set()
        await callback.message.answer("Выберите пункт меню\n"+text, reply_markup=markup)
    except Exception as ex:
        print(ex)
        markup = await back_kb()
        await callback.message.edit_text("Не получилось обновить, попробуйте заново", reply_markup=markup)


@dp.callback_query_handler(state=Add_tenant.edit_tenant_status)
async def edit_tenant_menu(callback: types.CallbackQuery):
    try:
        status = callback.data
        db.update_tenant_status(cur_house, cur_edited_tenant_id, status)
        await callback.message.answer("Успено обновлено!")
        text = await create_edit_tenant_text()
        markup = await edit_tenant_kb()
        await Add_tenant.edit_tenant_select_tenant.set()
        await callback.message.answer("Выберите пункт меню\n"+text, reply_markup=markup)
    except Exception as ex:
        print(ex)
        markup = await back_kb()
        await callback.message.edit_text("Не получилось обновить, попробуйте заново", reply_markup=markup)


@dp.message_handler(state=Add_tenant.edit_tenant_name)
async def edit_tenant_menu(message: types.Message):
    try:
        name = message.text
        db.update_tenant_name(cur_house, cur_edited_tenant_id, name)
        await message.answer("Успено обновлено!")
        text = await create_edit_tenant_text()
        markup = await edit_tenant_kb()
        await Add_tenant.edit_tenant_select_tenant.set()
        await message.answer("Выберите пункт меню\n"+text, reply_markup=markup)
    except Exception as ex:
        print(ex)
        markup = await back_kb()
        await message.edit_text("Не получилось обновить, попробуйте заново", reply_markup=markup)


@dp.message_handler(state=Add_tenant.edit_tenant_email)
async def edit_tenant_menu(message: types.Message):
    if db.check_email(cur_house, message.text):
        markup = await email_kb()
        await message.answer("ВНИМАНИЕ! Такой емайл уже есть в списке жителей дома.\
Оставить такой, внести другой емайл или ?", reply_markup=markup)
        return
    try:
        email = message.text
        db.update_tenant_email(cur_house, cur_edited_tenant_id, email)
        await message.answer("Успено обновлено!")
        text = await create_edit_tenant_text()
        markup = await edit_tenant_kb()
        await Add_tenant.edit_tenant_select_tenant.set()
        await message.answer("Выберите пункт меню\n"+text, reply_markup=markup)
    except Exception as ex:
        print(ex)
        markup = await back_kb()
        await message.edit_text("Не получилось обновить, попробуйте заново", reply_markup=markup)


@dp.message_handler(state=Add_tenant.edit_tenant_phone)
async def edit_tenant_menu(message: types.Message):
    phone = message.text
    phone = phone.replace(" ", "")
    phone = phone.replace("-", "")
    phone = phone.replace("+", "")
    if phone.startswith("8"):
        phone = "7"+phone[1:]
    if 10 >= len(phone) <= 11:
        await message.answer("Проверьте номер телефона. Возможно в нем лишние цифры")
        return
    all_tenants = db.get_tenant_by_phone_in_all_house(cur_house, phone)
    if all_tenants != None:
        text = ""
        for i in all_tenants:
            text += f"""ВНИМАНИЕ! Такой телефон уже есть в списке жителей дома с адресом {i[-3]}:
    КВ {i[2]} {i[5]} ( {i[8]} - ФИО: {i[9]} - {i[16]}% ) {i[6]} W({i[7]}) {i[10]}\n\n"""
        if text != "":
            await message.answer(text)
    try:
        has_wasapp = "Да" if await wa.is_wa_exist(phone) else "Нет"
        db.update_tenant_phone(
            cur_house, cur_edited_tenant_id, phone, has_wasapp)
        await message.answer("Успено обновлено!")
        text = await create_edit_tenant_text()
        markup = await edit_tenant_kb()
        await Add_tenant.edit_tenant_select_tenant.set()
        await message.answer("Выберите пункт меню\n"+text, reply_markup=markup)
    except Exception as ex:
        print(ex)
        markup = await back_kb()
        await message.edit_text("Не получилось обновить, попробуйте заново", reply_markup=markup)
