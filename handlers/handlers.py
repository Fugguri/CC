from aiogram import types
from main import dp, bot
from aiogram.dispatcher.filters.state import State
from keyboards.keyboards import start_kb
from main import db, wa
from models import Tenant

@dp.message_handler(commands=["start"], state="*")
async def start(message: types.Message):
    markup = await start_kb()

    await message.answer("""Это бот-помощник секретаря общих собраний. Он может:
🚀 загрузить данные по помещениям и собственникам
🤳 занести контактные данные жильцов и анкеты собственников
🤖 отправлять сообщения в WhatsApp (виртуальный консьерж дома)
💬 принимать сообщения гостей и жильцов через консьержа дома
📢 информировать всех жильцов об общих собраниях в доме
✅ получать от собственников бюллетени для голосования""", reply_markup=markup)





@dp.callback_query_handler(lambda call: call.data == "add_from_form", state="*")
async def post_registry(callback: types.CallbackQuery, state=State):
    data = callback.message.text.split("\n")
    address = data[5].replace('Адрес: ','')
    cad_num = db.get_house_by_address(address)
    tenant = await _create_tenant_from_form(data,*cad_num)
    text = "Добавляю"
    mes = await callback.message.answer(text)
    try:
        db.add_tenant(tenant.__dict__)
        await callback.message.answer(text)
        await state.finish()
    except Exception as ex:
        await callback.message.answer(ex)
    finally:
        await mes.delete()
        
async def _create_tenant_from_form(data,cad_num):
    date = data[0].replace('Анкета от номера  (','')[:-1]
    name = data[1].replace('ИМЯ: ','')
    phone = data[2].replace('Телефон: ','')[1:].replace(" ",'')
    email = data[3].replace('email: ','').strip()

    address = data[5].replace('Адрес: ','')
    flat_num = data[6].replace('Номер кв: ','').strip()
    status = data[7].replace('Статус: ','').strip()
    has_watsapp = 'Да' if await wa.is_wa_exist(phone[1:]) else 'Нет'
    flat =  db.get_flat_by_num(flat_num,cad_num)
    tenant = Tenant(
    date_of_create = date,
    flat_num = flat_num,
    flat_id = flat[5].replace(":",''),
    flat_status = flat[1],
    name = name,
    phone = phone,
    has_watsapp = has_watsapp,
    status = status,
    owner_full_name = "",
    owner_email = email,
    last_email_date = "",
    last_oss_number = "",
    date_of_sopd = "",
    passport = "",
    mkd_id = cad_num.replace(":",'') ,
    fraction_part = "",
    address = address,
    owner = "",
    cad_num = cad_num
    )
    return tenant