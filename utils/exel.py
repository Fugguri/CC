import asyncio
import pandas as pd
from main import db
houses = {}


async def exel_reader(file, sheet_name):

    # Загружаем spreadsheet в объект pandas
    xl = pd.ExcelFile(file)

    # Загрузить лист в DataFrame по его имени: df1
    df1 = xl.parse(sheet_name)

    if sheet_name == "Помещения":
        zipped = zip(df1['Статус помещения / объекта'].keys(),
                     df1['Статус помещения / объекта'],
                     df1['Адрес (местоположение объекта)'],
                     df1["№ помещения"],
                     df1['Площадь объекта из online справки РР'],
                     df1['Кадастровый номер помещения / объекта'],
                     df1['Тип помещения'],
                     df1['Этаж'],
                     df1['Подъезд'],
                     df1['Особые отметки о зарегистрированном праве на объект из он-лайн справки Росреестра']
                     )
        data = tuple(zipped)

        houses[data[0][2].replace("г.Санкт-Петербург, ", "")] = data

        return data

    if sheet_name == "Реестр":
        zipped = zip(df1["СТАТУС"],
                     df1["КАДНОМ"],
                     df1["№ помещения"],
                     df1["Площадь помещ."],
                     df1["Числитель доли"],
                     df1["Знаменатель доли"],
                     df1["Фамилия / Название ЮЛ"],
                     df1["Имя / ИНН ЮЛ"],
                     df1["Отчество / ОГРН ЮЛ"],
                     df1["Тип Собственника"],
                     df1["№ запроса, № выписки"],
                     df1["Дата запроса"],
                     df1["Вид права"],
                     df1["№ государственной регистрации права"],
                     df1["Дата госрегистрации"],
                     df1["Представитель"],
                     df1["Кол-во голосов, кв.м"],
                     df1["Доля голосов,%"],
                     df1["Дата голосования"],
                     df1["Тел. собств"],
                     df1["Эл.почта собств"],
                     df1["ЖНС"],
                     df1["Дата вступления в члены"],
                     df1["Дата выхода из членов"],
                     df1["Тип представителя"],
                     df1["Тел. представителя"],
                     df1["Эл. почта представителя"],
                     df1["Паспорт серия №"],
                     df1["Дата рождения"],
                     df1["Дата СОПД"],
                     df1["Дата окончания полномочий"],
                     df1["Почтовый адрес"],
                     )

        return (list(zipped))


async def create_tenants_exel(filename, data, flat):
    header_tenant = [("Дата время", "№ помещ.",	"ID помещения",	"Статус помещ.",	"Имя жильца",	"Телефон жильца",	"WhatsApp  жильца",	"Статус жильца",
                      "ФИО собственника (доля в ОИ, %)",	"Еmail собственника",	"Дата отправки",	"номер ОСС",	"Дата СОПД", "Паспорт", "ID МКД", "ФИО жильца")]
    header_flat = [("Подьезд", "Этаж",	"Статус",	"№ помещения",	"Доля ИО, %",	"Имя жильца",	"ФИО(статус) жильца",	"Телефон жильца(WA)",
                    "ФИО собственника (доля в ОИ, %)",	"Комментарий",	"Площадь, м2", "Голосов кв.м", "Кадастровый номер",	"Кадастровый номер МКД")]
    data = header_tenant + data
    data2 = header_flat + flat
    df1 = pd.DataFrame(data)
    df2 = pd.DataFrame(data2)
    writer = pd.ExcelWriter(path=filename)
    df1.to_excel(writer,
                 sheet_name="Жители",
                 merge_cells=False,
                 index=False,
                 index_label=False,
                 header=False)
    df2.to_excel(writer,
                 sheet_name="Помещения",
                 merge_cells=False,
                 index=False,
                 index_label=False,
                 header=False)
    writer.save()
    # exel = pd.ExcelWriter()


path = "/home/fugguri/Документы/CC/documents/6411_ОССП_1-В-23_Достоевского_30_ТЕСТ.xls"
if __name__ == "__main__":
    asyncio.run(exel_reader(path, "Реестр"))
