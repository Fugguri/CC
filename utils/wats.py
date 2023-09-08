from .texts import Texts
from .google import GoogleSheest
from .telegram import Telegram
from whatsapp_api_client_python import API
from typing import Union
from .shortLinkGenerator import generate_short_link
import re
from DB.sqlite_connection import Database
import smtplib
import os
import mimetypes
from aiogram import Bot, types
from config import db_name, ID_INSTANCE, API_TOKEN_INSTANCE
import asyncio
from apscheduler.schedulers.background import BackgroundScheduler
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
import mammoth
from .utils import Utils
user_state = {}
# Функция по добавлению конкретного файла к сообщению


def prepair_dock(receiver, house=None, owner=None):
    if owner[16] not in ["nan", None]:
        voter = owner[16]
    else:
        voter = {receiver[-11]}
    text = f"""<b>{receiver[-3]}</b><br>
на общем собрании собственников помещений №: {receiver[1]}<br><br>
Прием бюллетеней для голосования: {receiver[4]}, {receiver[6]}<br><br>
<b>Собственник</b>: {receiver[-11]}
<table border="1">
       <tr>
                 <td>
                       Квартира(помещение)(Общая площадь,кв.м - Кадастровый номер):
                 </td>
                 <td>
                       Квартира № {receiver[-18]} ({house[4]}м2 - {house[5]})
                 </td>
       </tr>
       <tr>
                 <td>
                       № и дата государственной регистрации права собственности,№ и дата выписки из ЕГРН
                 </td>
                 <td>
                       № {owner[14]} от {owner[15]},
                       № {owner[11]} от {owner[12]} 
                 </td>
       </tr>

</table><br>
<b>ФИО голосующего</b>: {voter} <b>E-mail</b>: {receiver[-10]}  <b>Телефон</b>: +{receiver[-14][0]} XXX XXX {receiver[-14][-4:]}<br>
<b>Дата голосования</b>: {datetime.datetime.now().strftime("%d.%m.%Y, %H:%M")}<br>"""
    doc = open("documents/"+receiver[7], "rb")
    res = mammoth.convert_to_html(doc).value.replace("{Вставка}", text)
    res = res.replace("<p>", "").replace("</p>", "<br>")
    html = f"""<html><head>
        <style>
        </style>
    </head>
    <body>
    {res}
    </body>
    </html>"""
    return html


class Mailer:
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

    async def send_email(self, addr_to, msg_subj, msg_text=None, msg_html=None, files=None):

        msg = MIMEMultipart()                                   # Создаем сообщение
        msg['From'] = self.addr_from                                 # Адресат
        msg['To'] = addr_to                                     # Получатель
        # Тема сообщения
        msg['Subject'] = msg_subj

        text = msg_text                                         # Текст сообщения
        html = msg_html
        # Добавляем в сообщение текст
        if msg_text:
            msg.attach(MIMEText(text, 'plain'))
        if msg_html:
            pass
        msg.attach(MIMEText(msg_html, "html"))
        self.__process_attachement(msg, files)

        # ======== Этот блок настраивается для каждого почтового провайдера отдельно ===============================================
        # Создаем объект SMTP
        server = smtplib.SMTP_SSL('smtp.mail.ru', 465)
        # server.starttls()                                      # Начинаем шифрованный обмен по TLS
        # Включаем режим отладки, если не нужен - можно закомментировать
        # server.set_debuglevel(True)
        # Получаем доступ
        server.login(self.addr_from, self.password)
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
    def send_sync_email(self, addr_to, msg_subj, msg_text=None, msg_html=None, files=None):

        msg = MIMEMultipart()                                   # Создаем сообщение
        msg['From'] = self.addr_from                                 # Адресат
        msg['To'] = addr_to                                     # Получатель
        # Тема сообщения
        msg['Subject'] = msg_subj

        text = msg_text                                         # Текст сообщения
        html = msg_html
        # Добавляем в сообщение текст
        if msg_text:
            msg.attach(MIMEText(text, 'plain'))
        if msg_html:
            pass
        msg.attach(MIMEText(msg_html, "html"))
        self.__process_attachement(msg, files)

        # ======== Этот блок настраивается для каждого почтового провайдера отдельно ===============================================
        # Создаем объект SMTP
        server = smtplib.SMTP_SSL('smtp.mail.ru', 465)
        # server.starttls()                                      # Начинаем шифрованный обмен по TLS
        # Включаем режим отладки, если не нужен - можно закомментировать
        # server.set_debuglevel(True)
        # Получаем доступ
        server.login(self.addr_from, self.password)
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

    def __attach_file(self, msg, filepath):
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

    def __process_attachement(self, msg, files):
        if not files:
            return
        for f in files:
            if os.path.isfile(f):                               # Если файл существует
                # Добавляем файл к сообщению
                self.__attach_file(msg, f)
            # Если путь не файл и существует, значит - папка
            elif os.path.exists(f):
                # Получаем список файлов в папке
                dir = os.listdir(f)
                for file in dir:                                # Перебираем все файлы и...
                    # ...добавляем каждый файл к сообщению
                    self.__attach_file(msg, f+"/"+file)


class Watsapp_utils(Utils):
    async def is_wa_exist(self, phone):
        request = self.greenAPI.serviceMethods.checkWhatsapp(phone).data
        try:
            exist = request["existsWhatsapp"]
        except:
            return False
        return exist

    def set_state(self, phone, state):
        try:
            self.user_state[phone] = state
            return True
        except:
            return False

    def get_state(self, phone):
        try:
            return self.user_state[phone]
        except:
            self.user_state[phone] = ""
            return self.user_state[phone]

    def create_income_message_text(self, body):
        if body["messageData"]["typeMessage"] == "textMessage":

            try:
                message_text = str(body["messageData"]
                                   ["textMessageData"]['textMessage'])
            except:
                message_text = str(body["messageData"]
                                   ["extendedTextMessageData"]['text'])

        else:
            message_text = ""

        return message_text

    def clear_phone(self, body):
        return body["senderData"]["chatId"].replace("@c.us", "")

    def collect_photo(self, body, phone):
        # if body["messageData"]["typeMessage"] == "imageMessage":
        try:
            photo_url = body["messageData"]["fileMessageData"]["downloadUrl"]
            # file_name = body["messageData"]["fileMessageData"]["fileName"]
            # import httplib2
            # h = httplib2.Http()
            # response, content = h.request(photo_url)
            # print(photo_url)
            # with open(f'wa_img/{file_name}', 'wb') as img:
            #     img.write(content)
            try:
                self.receiver_photos[phone]
            except:
                self.receiver_photos[phone] = []
            photos = self.receiver_photos[phone]
            photos.append(photo_url)
            return True
        except:
            return False

    def reset_user_data(self, phone):
        
        try:
            self.missive.pop(phone)
        except:
            pass
        
        try:
            self.receiver.pop(phone)
        except:
            pass
        
        try:
            self.guest.pop(phone)
        except:
            pass
        
        try:
            self.receiver_photos.pop(phone)
        except:
            pass
        
        try:
            self.user_state.pop(phone)
        except:
            pass

    def _convert_number(self, phone):
        if phone.startswith("8"):
            phone = "7"+phone[1:]
        if phone.startswith("+"):
            phone = phone[1:]
        if "-" in phone:
            phone = phone.replace('-', '')
        return phone


class Watsapp(Watsapp_utils):

    def __init__(self):
        self.greenAPI = API.GreenApi(ID_INSTANCE, API_TOKEN_INSTANCE)
        self.db = Database(db_name)
        self.gs = GoogleSheest()
        self.emailer = Mailer()
        self.create_text = Texts()
        self.tg = Telegram()
        self.sending = self.greenAPI.sending
        self.startReceivingNotifications = self.greenAPI.webhooks.startReceivingNotifications

    async def send_message(self, text, phone):
        phone = self._convert_number(phone)
        self.greenAPI.sending.sendMessage(phone+"@c.us", text)

    def send_sync_message(self, text, phone,img_path=None):
        phone = self._convert_number(phone)
        
        if img_path:
            name = img_path.split("/")[-1]
            self.greenAPI.sending.sendFileByUpload(phone+"@c.us",path=img_path,fileName=name,caption=text)
        else:
            self.greenAPI.sending.sendMessage(phone+"@c.us", text)

    async def send_tenant_wellcome_message(self, cur_name: str, cur_address: str, phone: Union[str, int]):
        text = self.db.get_text_by_id("1").format(
            cur_name, cur_address)
        phone = self._convert_number(str(phone))
        request = self.greenAPI.sending.sendMessage(phone+"@c.us", text)
        return request

    async def send_no_email(self, cur_name: str, cur_address: str, phone: Union[str, int]):
        text = "Укажите пожалуйста адрес вашей электронной почты, чтобы получить уже заполненный бюллетень, который затем нужно просто обратно мне отправить ответным письмом."
        phone = self._convert_number(str(phone))
        request = self.greenAPI.sending.sendMessage(phone+"@c.us", text)
        return request

    async def mail_voting_notification(self, receiver):
        phone = self._convert_number(str(receiver[-14]))
        text = self.db.get_text_by_id("3").format(receiver[-15], receiver[-3])
        print(receiver)
        res = self.sending.sendFileByUpload(
            phone+"@c.us", path="documents/"+receiver[8], fileName=receiver[8], caption=text)
        return res

    async def send_voting_notification(self, receiver):
        phone = self._convert_number(str(receiver[1]))
        text = self.db.get_text_by_id("3").format(receiver[-2], receiver[-5])
        res = self.sending.sendFileByUpload(
            phone+"@c.us", path="documents/"+receiver[-6], fileName=receiver[-6], caption=text)
        if receiver[0] == "":
            text = self.db.get_text_by_id("20")
            self.sending.sendMessage(phone+"@c.us", text)
        return res

    async def send_email_and_notify(self, receiver):
        phone = self._convert_number(str(receiver[-14]))
        house = self.db.get_house_data(receiver[-1], receiver[-18])
        full_name = receiver[-11].split(" ")
        owner = self.db.get_owner_by_full_name(receiver[-1],
                                               full_name[0], full_name[1], full_name[2])
        dock = prepair_dock(receiver, house, owner)
        notification = "documents/"+receiver[8]
        text = self.db.get_text_by_id("3").format(receiver[-15], receiver[-3])
        self.sending.sendFileByUpload(
            phone+"@c.us", path="documents/"+receiver[8], fileName=receiver[8], caption=text)

        email = await self.emailer.send_email(receiver[-10], f"Ваше голосование на общем собрании {receiver[1]}", msg_html=dock, files=[notification,])
        name_of_oss = receiver[1]
        address = receiver[-3]
        date = datetime.datetime.now().strftime("%d.%m.%Y %H:%M")
        self.db.update_tenant_mailing_data(
            receiver[-1], date, receiver[1], receiver[-20])

        text = self.db.get_text_by_id("2").format(
            receiver[-10], name_of_oss, address)
        self.sending.sendMessage(phone+"@c.us", text)


class Watsapp_bot(Watsapp, Utils):
    def __init__(self):
        super().__init__()
        self.user_state = dict()
        self.missive = dict()
        self.receiver = dict()
        self.guest = dict()
        self.receiver_photos = dict()
        self.scheduler = BackgroundScheduler(timezone='Europe/Moscow')
    def start_receive(self):
        self.scheduler.start()
        self.startReceivingNotifications(self.__onIncomingMessage)

    def _goodbye(self,phone):
        text = "Было приятно поболтать. Хорошего Вам дня!"
        self.send_sync_message(text,phone)
        self.reset_user_data(phone)
    
    def _create_reminder(self,phone):
        next_run = datetime.datetime.now() + datetime.timedelta(minutes=1)
        # run_rime = datetime.datetime.strftime(next_run,"%d/%m/%Y, %H:%M:%S")
        try:
            self.scheduler.remove_job(phone)
        except:
            pass
        self.scheduler.add_job(self._goodbye,
                               trigger='date',
                               next_run_time= next_run,
                               name=phone,
                               id=phone,
                               args=(phone,))

    def __onIncomingMessage(self, typeWebhook, body):

        if typeWebhook != 'incomingMessageReceived':
            return

        phone = self.clear_phone(body)
        is_tenant = self.db.is_phone_exist(str(phone))
        state = self.get_state(phone)
        message_text = self.create_income_message_text(body)
        print(is_tenant,phone)
        return
        self._create_reminder(phone)
        
        if self.collect_photo(body, phone):
            text = "Если это все фото - отправьте 0"
            self.send_sync_message(text, phone)
            return

        if self.register_email(message_text,phone):
            return

        if "МКД:" in message_text and "Кад.Ном:" in message_text and not is_tenant:
            a= message_text.replace("МКД:","")
            a = a.replace("Кад.Ном:","")
            address, cad_num = a.split("\n")
            is_house_exist = self.db.get_house_by_cad_num(cad_num=cad_num.strip())
            try:
                self.guest[phone]['address'] = address.strip()
                self.guest[phone]['cad_num'] = cad_num.strip()
            except:
                self.guest[phone] = {}
                self.guest[phone]['address'] = address.strip()
                self.guest[phone]['cad_num'] = cad_num.strip()
                
            if is_house_exist :
                self.guest[phone]['address'] = is_house_exist[0]
                self.guest[phone]['cad_num'] = is_house_exist[1]
            else:
                address = "#"
                self.guest[phone]['cad_num'] = cad_num
                
            wellcome_text = f"""Приветствую!
Меня зовут Домиант, я бот-помощник, работаю виртуальным консъержем в доме
{address}
Я могу передать сообщения жителей и гостей управляющему, председателю (старшему по дому) или секретарю собраний."""
                
            self.send_sync_message(wellcome_text, phone,img_path="mics/cons.jpg")
            text = "Как могу к вам обращаться?"
            self.send_sync_message(text, phone)
            self.set_state(phone, "name")
            self.missive[phone] = message_text
            return
        
        if state == "wait_form" or not state:
            if message_text.lower() == "заполнил":
                try:
                    address = self.guest[phone]['address'] 
                    cad_num = self.guest[phone]['cad_num'] 
                    gf_link = self.create_gf_link(phone,address)
                except Exception as ex:
                    print(ex)
                self.gs.new_form_notify(phone)
                text = "Спасибо, уточните пожалуйста ваш вопрос"
                self.send_sync_message(text, phone)                
                return
                
        if not state:
            if self.wellcome_tenant(phone,is_tenant,message_text):
                return
            
            wellcome_text = f"""Приветствую!
Меня зовут Домиант, я бот-помощник, работаю виртуальным консъержем в доме
#
Я могу передать сообщения жителей и гостей управляющему, председателю (старшему по дому) или секретарю собраний."""
                
            self.send_sync_message(wellcome_text, phone,img_path="mics/cons.jpg")
            text = "Как могу к вам обращаться?"
            self.send_sync_message(text, phone)
            self.set_state(phone, "name")
            self.guest[phone]={}
            self.guest[phone]['missive'] = message_text
            self.missive[phone] = message_text
            
            return
        
        if state == "wait_missive":
            if self.has_cyrillic(message_text):
                comu = """Кому Вы хотите передать это обращение?
Управляющему (заявку, запрос или жалобу) - введите 1
Председателю (заявление или предложение) - введите 2
Секретарю собрания (опрос или голосование) - введите 3
"""
                self.greenAPI.sending.sendMessage(
                    phone+"@c.us", comu)
                self.user_state[phone] = "comu"
                self.missive[phone] = message_text
            else:
                text = "Не совсем понял ваше сообщение, уточните пожалуйста ваш вопрос"
                self.send_sync_message(text, phone)
            return
        
        if state == "name":            
            try:
                address = self.guest[phone]['address'] 
                cad_num = self.guest[phone]['cad_num'] 
                gf_link = self.create_gf_link(phone,address)
                short_link= generate_short_link(gf_link)
            except Exception as ex:
                gf_link = self.create_gf_link(phone,"")
                short_link= generate_short_link(gf_link)
            
            self.send_sync_message(
                "Очень приятно, {}. Момент…".format(message_text), phone)
            try:
                self.guest[phone]['name'] = message_text
            except:
                self.guest[phone] = {}
                self.guest[phone]['name'] = message_text
            try:
                if self.guest[phone]['missive']:
                    # text = "Не совсем понял ваше сообщение, уточните пожалуйста ваш вопрос"
                    # self.send_sync_message(text, phone)
                    # self.set_state(phone, "wait_missive")
                    comu = """Кому Вы хотите передать это обращение?
    Управляющему (заявку, запрос или жалобу) - введите 1
    Председателю (заявление или предложение) - введите 2
    Секретарю собрания (опрос или голосование) - введите 3
    """
                    self.greenAPI.sending.sendMessage(phone+"@c.us", comu)
                    self.user_state[phone] = "comu"
                    # self.missive[phone] = message_text
                
                    return
            except:
                pass
            text = f"""К сожалению Вас пока нет в моём списке жителей дома.
 Заполните пожалуйста регистрационную анкету по ссылке {short_link}. 
 После этого Ваши данные будут внесены в реестр жителей дома и я смогу передать Ваш вопрос по назначению."""

            self.send_sync_message(text, phone)
            self.set_state(phone, "wait_form")
            self.scheduler.remove_job(phone)
            
            return

        if state == "comu":
            if message_text in ["1", "2", "3"]:
                self.receiver[phone] = ""
                if message_text == "1":
                    self.receiver[phone] = "Управляющий"
                if message_text == "2":
                    self.receiver[phone] = "Председатель"
                if message_text == "3":
                    self.receiver[phone] = "Секретарь собрания"
                text = "Понятно. Пожалуйста для большей ясности приложите сюда фото (или скан документа на который вы ссылаетесь). Если не будет фото/скан - нажмите 0"
                self.send_sync_message(text, phone)
                return

            if message_text == "0":
                text = "Что-нибудь еще нужно передать?\nДа/Нет"
                self.send_sync_message(text, phone)
                return

            if message_text.lower() == "нет":
                is_guest = "гостя" 
                now = datetime.datetime.strftime(datetime.datetime.now(), "%d/%m/%Y, %H:%M:%S")
                if is_tenant:
                    is_guest="жителя"
                if is_tenant:
                    name = is_tenant[0][5]
                else:
                    name = self.guest[phone]['name']
                reply_message = f"Сообщение {is_guest} {phone} ({now})\n{name}:\n{self.missive[phone]}"

                try:
                    media = self.receiver_photos[phone]
                    self.tg.send_telegram_notification(reply_message, media)
                except Exception as ex:
                    print(ex)
                    self.tg.send_telegram_notification(reply_message)
                text = "Было приятно поболтать.\nХорошего Вам дня!"
                self.scheduler.remove_job(phone)
                
                self.send_sync_message(text, phone)
                self.set_state(phone,False)
                return
            
            else:
                text = "Отправьте текст обращения"
                self.send_sync_message(text, phone)
                self.reset_user_data(phone)

    def wellcome_tenant(self,phone,is_tenant,message_text):
            if is_tenant :
                self.send_sync_message(
                        "{0}, приветствую Вас! ".format(is_tenant[0][5]), phone)
                self.set_state(phone, "comu")

                if self.has_cyrillic(message_text):
                    comu = """Кому Вы хотите передать это обращение?
Управляющему (заявку, запрос или жалобу) - введите 1
Председателю (заявление или предложение) - введите 2
Секретарю собрания (опрос или голосование) - введите 3
"""
                    self.greenAPI.sending.sendMessage(phone+"@c.us", comu)
                    self.user_state[phone] = "comu"
                    self.missive[phone] = message_text

                return True
            return False

    def register_email(self,message_text,phone):
        if "@" in message_text:
            
            if self.emailer.verify_email(message_text.replace(" ", "")):
                text = "Корректный эмейл. Сохраняю"
                self.sending.sendMessage(text, phone)

                self.db.update_email(phone, message_text)

                receivers = self.db.get_tenant_by_phone_for_email(phone)

                for receiver in receivers:
                    # if (receiver[12] == 'ИДЕТ ГОЛОСОВАНИЕ' and receiver[-8] != '') or receiver[12] != 'ИДЕТ ГОЛОСОВАНИЕ':
                    #     continue
                    cad_num = receiver[-1]
                    flat_num = receiver[-18]
                    phone = str(receiver[-14])
                    full_name = receiver[-11].split(" ")
                    notification = "documents/"+receiver[8]
                    house = self.db.get_house_data(cad_num, flat_num)
                    email = receiver[-10]
                    # if email != "":
                    #     continue
                    mailer_name = receiver[-15]
                    address = receiver[-3]
                    tenant_id = receiver[-20]
                    name_of_oss = receiver[1]
                    meeting_end_date = receiver[3].replace(
                        "/", ".").replace(",", ".").replace("-", ".")
                    owner = self.db.get_owner_by_full_name(cad_num,
                                                        full_name[0],
                                                        full_name[1],
                                                        full_name[2],)
                    # return
                    text = self.db.get_text_by_id("3")
                    text = text.format(mailer_name, address)
                    email_title = f"Ваше голосование на общем собрании {name_of_oss}"
                    sender_email_text = self.db.get_text_by_id(
                        "2").format(email, name_of_oss, address)
                    date = datetime.datetime.now().strftime("%d.%m.%Y %H:%M")
                    phone = self._convert_number(phone)
                    self.db.update_tenant_mailing_data(
                        cad_num, date, name_of_oss, tenant_id)
                    if datetime.datetime.strptime(meeting_end_date, "%d.%m.%Y") < datetime.datetime.today():
                        print(2)
                        continue
                    try:
                        dock = prepair_dock(receiver, house, owner)
                        self.emailer.send_sync_email(email,
                                                    email_title,
                                                    msg_html=dock,
                                                    files=[notification,])
                        self.sending.sendMessage(
                            phone+"@c.us", sender_email_text)
                    except Exception as ex:
                        print(ex)

                return True

            else:
                text = "Некорректный эмейл попробуйте заново"
                self.send_sync_message(text, phone)
                return True
        else:
            return False
        
if __name__ == "__main__":
    pass
