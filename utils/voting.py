# Многокомпонентный объект
from email.mime.multipart import MIMEMultipart
from email.mime.audio import MIMEAudio                      # Аудио
from email.mime.image import MIMEImage                      # Изображения
from email.mime.text import MIMEText                        # Текст/HTML
from email.mime.base import MIMEBase                        # Общий тип
# Импортируем энкодер
from email import encoders
# Импорт класса для обработки неизвестных MIME-типов, базирующихся на расширении файла
import mimetypes
# Функции для работы с операционной системой, не зависящие от используемой операционной системы
import os
# Импортируем библиотеку по работе с SMTP
import smtplib
import datetime
from whatsapp_api_client_python import API
from smtplib import SMTPNotSupportedError, SMTPDataError
from .dock import prepair_dock
import os
from DB.sqlite_connection import Database
db = Database("CC.db")

ID_INSTANCE = "1101817417"
API_TOKEN_INSTANCE = "d6b222197e944ce68cc91ee87dc79353600e841190f0400cbc"

greenAPI = API.GreenApi(ID_INSTANCE, API_TOKEN_INSTANCE)


async def send_message(receiver, text=None, is_email=True):
    phone = receiver[1]
    # phone = "89502213750"
    if phone.startswith("8"):
        phone = "7"+phone[1:]
    elif phone.startswith("+"):
        phone = phone[1:]
    if "-" in phone:
        phone.replace('-', '')
    name_of_oss = receiver[11]
    address = receiver[16]
    mes = greenAPI.serviceMethods.checkWhatsapp(phone).data
    if mes == None or mes["existsWhatsapp"] == False:
        return False
#     text = f"""Уважаемый(ая) {receiver[4]} {receiver[5]} {receiver[6]} !
# В доме {receiver[16]}  проводится общее собрание собственников дома по важным вопросам.
# Подробная информация указана в прилагаемом сообщении. Просим собственников принять участие в голосовании."""
    text = db.get_text_by_id("2").format(receiver[0], name_of_oss, address)
    if is_email == False:
        text = "Укажите пожалуйста адрес вашей электронной почты, чтобы получить уже заполненный бюллетень, который затем нужно просто обратно мне отправить ответным письмом."
        greenAPI.sending.sendMessage(phone+"@c.us", text)
    else:
        greenAPI.sending.sendMessage(
            phone+"@c.us", text)
    return mes


async def send_email(addr_to, msg_subj, msg_text=None, msg_html=None, files=None):
    password = "ELv8vb6pPAayxpGQxQU3"                        # Пароль
    addr_from = "sekretaross@mail.ru"                        # Отправитель
    # addr_from = "fugguri@yandex.ru"
    # password = "Neskazu_038"

    msg = MIMEMultipart()                                   # Создаем сообщение
    msg['From'] = addr_from                                 # Адресат
    msg['To'] = addr_to                                     # Получатель
    msg['Subject'] = msg_subj                               # Тема сообщения

    text = msg_text                                         # Текст сообщения
    html = msg_html
    # Добавляем в сообщение текст
    if msg_text:
        msg.attach(MIMEText(text, 'plain'))
    if msg_html:
        pass
    msg.attach(MIMEText(msg_html, "html"))
    process_attachement(msg, files)

    # ======== Этот блок настраивается для каждого почтового провайдера отдельно ===============================================
    # Создаем объект SMTP
    server = smtplib.SMTP_SSL('smtp.mail.ru', 465)
    # server.starttls()                                      # Начинаем шифрованный обмен по TLS
    # Включаем режим отладки, если не нужен - можно закомментировать
    # server.set_debuglevel(True)
    server.login(addr_from, password)                       # Получаем доступ
    # Отправляем сообщение
    try:
        server.verify(addr_to)
        server.send_message(msg)
        server.quit()                                           # Выходим
        return True
    except Exception as ex:
        print(ex)
        return False

    # ==========================================================================================================================


class Mailer():
    def __init__(self) -> None:
        self.password = "ELv8vb6pPAayxpGQxQU3"                        # Пароль
        self.addr_from = "sekretaross@mail.ru"
        self.server = smtplib.SMTP_SSL('smtp.mail.ru', 465)

    def verify_email(self, email):
        self.server.connect('smtp.mail.ru', 465)
        self.server.login(self.addr_from, self.password)
        try:
            self.server.verify(email)
            self.server.quit()                                           # Выходим
            return True
        except Exception as ex:
            print(ex)
            return False

    async def send_message(receiver, is_email=True):
        phone = receiver[1]
        # phone = "89502213750"
        if phone.startswith("8"):
            phone = "7"+phone[1:]
        elif phone.startswith("+"):
            phone = phone[1:]
        if "-" in phone:
            phone.replace('-', '')

        mes = greenAPI.serviceMethods.checkWhatsapp(phone).data
        if mes == None or mes["existsWhatsapp"] == False:
            return False
    #     text = f"""Уважаемый(ая) {receiver[4]} {receiver[5]} {receiver[6]} !
    # В доме {receiver[16]}  проводится общее собрание собственников дома по важным вопросам.
    # Подробная информация указана в прилагаемом сообщении. Просим собственников принять участие в голосовании."""

        text = "Уважаемый {0}! В доме {1} проводится общее собрание собственников дома по важным вопросам. Подробная информация указана в прилагаемом сообщении. Просим собственников принять участие в голосовании.".format(
            receiver[4], receiver[16])
        if is_email == False:
            text = "Укажите пожалуйста адрес вашей электронной почты, чтобы получить уже заполненный бюллетень, который затем нужно просто обратно мне отправить ответным письмом."
            greenAPI.sending.sendMessage(phone+"@c.us", text)
        else:
            greenAPI.sending.sendFileByUpload(
                phone+"@c.us", path="documents/"+receiver[-5], fileName=receiver[-5], caption=text)
            text = db.get_text_by_id("2").format(receiver[0])
            greenAPI.sending.sendMessage(phone+"@c.us", text)

        return mes

# Функция по обработке списка, добавляемых к сообщению файлов


def process_attachement(msg, files):
    if not files:
        return
    for f in files:
        if os.path.isfile(f):                               # Если файл существует
            # Добавляем файл к сообщению
            attach_file(msg, f)
        # Если путь не файл и существует, значит - папка
        elif os.path.exists(f):
            # Получаем список файлов в папке
            dir = os.listdir(f)
            for file in dir:                                # Перебираем все файлы и...
                # ...добавляем каждый файл к сообщению
                attach_file(msg, f+"/"+file)


# Функция по добавлению конкретного файла к сообщению
def attach_file(msg, filepath):
    # Получаем только имя файла
    filename = os.path.basename(filepath)
    # Определяем тип файла на основе его расширения
    ctype, encoding = mimetypes.guess_type(filepath)
    if ctype is None or encoding is not None:               # Если тип файла не определяется
        # Будем использовать общий тип
        ctype = 'application/octet-stream'
    # Получаем тип и подтип
    maintype, subtype = ctype.split('/', 1)
    if maintype == 'text':                                  # Если текстовый файл
        with open(filepath) as fp:                          # Открываем файл для чтения
            # Используем тип MIMEText
            file = MIMEText(fp.read(), _subtype=subtype)
            # После использования файл обязательно нужно закрыть
            fp.close()
    elif maintype == 'image':                               # Если изображение
        with open(filepath, 'rb') as fp:
            file = MIMEImage(fp.read(), _subtype=subtype)
            fp.close()
    elif maintype == 'audio':                               # Если аудио
        with open(filepath, 'rb') as fp:
            file = MIMEAudio(fp.read(), _subtype=subtype)
            fp.close()
    else:                                                   # Неизвестный тип файла
        with open(filepath, 'rb') as fp:
            # Используем общий MIME-тип
            file = MIMEBase(maintype, subtype)
            # Добавляем содержимое общего типа (полезную нагрузку)
            file.set_payload(fp.read())
            fp.close()
            # Содержимое должно кодироваться как Base64
            encoders.encode_base64(file)
    file.add_header('Content-Disposition', 'attachment',
                    filename=filename)  # Добавляем заголовки
    # Присоединяем файл к сообщению
    msg.attach(file)


async def send_notification_message(receiver, text):
    phone = receiver[1]
    if phone.startswith("8"):
        phone = "7"+phone[1:]
    elif phone.startswith("+"):
        phone = phone[1:]
    if "-" in phone:
        phone.replace('-', '')

    mes = greenAPI.serviceMethods.checkWhatsapp(phone).data
    if mes == None or mes["existsWhatsapp"] == False:
        return False

    else:
        greenAPI.sending.sendMessage(phone+"@c.us", text)
        return True

    return mes


async def send_notification(receivers, message=None):

    for receiver in receivers:
        try:
            mes = await send_message(receiver, message.format(receiver[-1], receiver[-4]))
            if mes == False:
                await message.answer(f"Внимание!!!\nУ жильца {receiver[-1]} в квартире №{receiver[3]} с номером {receiver[1]} нет WatsApp \nСобственник {receiver[4]} {receiver[5]} {receiver[6]}")
        except SMTPDataError:
            pass


async def meeting_notify(receivers, message=None, meeting_data=None):
    for receiver in receivers:

        tenant = db.get_tenant_by_phone(meeting_data[-4], receiver[1])
        if tenant[-9] != "":
            return
        # text=
        greenAPI.sending.sendFileByUpload(
            receiver[1]+"@c.us", path="documents/"+receiver[-5], fileName=receiver[-5], caption=message.format(receiver[-1], receiver[-4]))


async def start_voting(receivers, message=None, meeting_data=None):
    for receiver in receivers:
        print(meeting_data)
        tenant = db.get_tenant_by_phone(meeting_data[-6], receiver[1])
        if receiver[0] == "":
            await send_message(receiver, is_email=False)
        if tenant[-9] != meeting_data[1]:
            try:
                dock = await prepair_dock(receiver)
                notification = "documents/"+receiver[-6]
                email = await send_email(receiver[0],
                                         f"Ваше голосование на общем собрании {receiver[11]}",
                                         msg_html=dock,
                                         files=[notification,])
                date = datetime.datetime.now().strftime("%d.%m.%Y %H:%M")
                db.update_tenant_mailing_data(
                    meeting_data[-6], date, meeting_data[1], tenant[0])
                if email == False:
                    await message.answer(f"Внимание!!!\nУ жильца {receiver[-2]} в квартире №{receiver[3]} с email {receiver[0]} несуществующий эмейл  \nСобственник {receiver[4]} {receiver[5]} {receiver[6]}")
                    mes = await send_message(receiver, email)
                else:
                    mes = await send_message(receiver, is_email=email)
                if mes == False:
                    await message.answer(f"Внимание!!!\nУ жильца {receiver[-2]} в квартире №{receiver[3]} с номером {receiver[1]} нет WatsApp \nСобственник {receiver[4]} {receiver[5]} {receiver[6]}")
            except SMTPNotSupportedError:
                await message.answer(f"Неверный email: {receiver[0]}\n Собственник: {receiver[4]} {receiver[5]} {receiver[6]}")
            except SMTPDataError:
                pass
            # return
