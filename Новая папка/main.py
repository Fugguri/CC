import gspread
from whatsapp_api_client_python import API
from datetime import datetime 
import logging

logging.basicConfig(filename="main.log",level=logging.DEBUG,
                    format='%(asctime)s %(message)s',
) 
#Creating an object of the logging 
logger=logging.getLogger() 
 
#Setting the threshold of logger to DEBUG 
logger.setLevel(logging.INFO) 

ID_INSTANCE, API_TOKEN_INSTANCE = "1101807848", "3fb8e25cb35c40c9a04ce00768ad69b6f7e151848abf409fa6"

greenAPI = API.GreenApi(ID_INSTANCE, API_TOKEN_INSTANCE)

text_of_good_degree = '''Спасибо за Высокую оценку!
У нас есть для тебя сюрприз 🎁
Оставь пожалуйста отзыв о СУПЕРТЯЖ_Доставка на Яндекс Картах и получи Ролл _ в подарsок 😍
Нужно перейти по этой ссылке https://yandex.com/maps/org/178435528058 оставить отзыв о нас и отправить нам скрин, а мы привезем тебе ролл «Аляска с Лососем» в подарок, к следующему заказу)


Спасибо за уделенное время!'''

text_of_not_good_degree = """Спасибо за обратную связь! 
Приносим извинения за доставленные неудобства. 
Подскажите когда Вам будет удобно чтобы контроль качества с вами связался для того чтобы обсудить сложившуюся ситуацию и разобраться в проблеме. 
Спасибо!
"""

user_data = {}

def onEvent(typeWebhook, body):
    """Проверяем тип сообщения входящй или исходящий"""
    if typeWebhook == 'incomingMessageReceived':  # Проверяем, что сообщение входящее
        senderData = body["senderData"]
        """Собираем данные отправителя"""
        chatId = senderData["chatId"]
        sender = senderData["sender"].replace("@c.us", "")
        senderName = senderData["senderName"]
        # print(chatId)
        # print(sender)
        # print(senderName)
        try:
            user_data[sender]
        except:
            user_data[sender] = {}

        messageData = body["messageData"]
        """Собираем данные о сообщении"""
        typeMessage = messageData["typeMessage"]
        messageData = body["messageData"]
        """Собираем данные о сообщении"""
        typeMessage = messageData["typeMessage"]
        try:
            textMessageData = messageData["textMessageData"]
            """получаем данные о сообщении"""
            textMessage = textMessageData["textMessage"]  
            try:
                user_data[sender]["degree"]
                is_degree = True
            except:
                is_degree = False

            # if is_degree and "контакт" in textMessage.lower():
            #     user_data[sender]["contact"] = textMessage
            #     greenAPI.sending.sendMessage(
            #         chatId=chatId, message="Спасибо, мы с вами свяжемся по указанным контактным данным.")
            #     degree, sender, comment, contact = user_data[sender][
            #         "degree"], sender, user_data[sender]["comment"], user_data[sender]["contact"]
            #     sheets_append_row(degree, sender, comment, contact)

            if "5" in textMessage:
                
                a = greenAPI.sending.sendMessage(
                    chatId=chatId, message=text_of_good_degree)
                logger.info(a) 
                logger.info(body)
                sheets_append_row(5, sender,textMessage)
            if "1" in textMessage:
                user_data[sender]["degree"] = 1
                comment = textMessage
                user_data[sender]["comment"] = comment
                
                a = greenAPI.sending.sendMessage(
                    chatId=chatId, message=text_of_not_good_degree)
                logger.info(a) 
                logger.info(body)
                sheets_append_row(1, sender, comment)
            if "2" in textMessage:
                user_data[sender]["degree"] = 2
                comment = textMessage
                user_data[sender]["comment"] = comment
                a = greenAPI.sending.sendMessage(
                    chatId=chatId, message=text_of_not_good_degree)
                logger.info(a) 
                logger.info(body) 
                sheets_append_row(2, sender, comment)
            if "3" in textMessage:
                user_data[sender]["degree"] = 3
                comment = textMessage
                user_data[sender]["comment"] = comment
                a = greenAPI.sending.sendMessage(
                    chatId=chatId, message=text_of_not_good_degree)
                logger.info(a) 
                logger.info(body)
                
                sheets_append_row(3, sender, comment)
            if "4" in textMessage:
                user_data[sender]["degree"] = 4
                comment = textMessage
                user_data[sender]["comment"] = comment
                a = greenAPI.sending.sendMessage(
                    chatId=chatId, message=text_of_not_good_degree)
                logger.info(a) 
                logger.info(body)
                sheets_append_row(4, sender, comment)

            # if "5" in textMessage:
            #     index = textMessage.index("5")
            #     next_simbol = textMessage[index+1]
            #     prev_simbol = textMessage[index-1]
            #     if textMessage == "5":
            #         user_data[sender]["degree"] = 5
            #         comment = textMessage
            #         user_data[sender]["comment"] = comment
            #         greenAPI.sending.sendMessage(
            #             chatId=chatId, message=text_of_good_degree)
            #         sheets_append_row(5, sender, comment)
            #     if len(textMessage) > 2 and next_simbol not in nums and prev_simbol not in nums:
            #         user_data[sender]["degree"] = 5
            #         comment = textMessage
            #         user_data[sender]["comment"] = comment
            #         greenAPI.sending.sendMessage(
            #             chatId=chatId, message=text_of_good_degree)
            #         sheets_append_row(5, sender, comment)

            # elif "1" in textMessage:
            #     index = textMessage.index("1")
            #     next_simbol = textMessage[index+1]
            #     prev_simbol = textMessage[index-1]
            #     if textMessage == "1":
            #         user_data[sender]["degree"] = 1
            #         comment = textMessage
            #         user_data[sender]["comment"] = comment
            #         greenAPI.sending.sendMessage(
            #             chatId=chatId, message=text_of_good_degree)
            #         sheets_append_row(1, sender, comment)
            #     if len(textMessage) > 2 and next_simbol not in nums and prev_simbol not in nums:
            #         user_data[sender]["degree"] = 1
            #         comment = textMessage
            #         user_data[sender]["comment"] = comment
            #         greenAPI.sending.sendMessage(
            #             chatId=chatId, message=text_of_not_good_degree)
            #         sheets_append_row(1, sender, comment)

            # elif "2" in textMessage:
            #     index = textMessage.index("2")
            #     next_simbol = textMessage[index+1]
            #     prev_simbol = textMessage[index-1]
            #     if textMessage == "2":
            #         user_data[sender]["degree"] = 2
            #         comment = textMessage
            #         user_data[sender]["comment"] = comment
            #         greenAPI.sending.sendMessage(
            #             chatId=chatId, message=text_of_good_degree)
            #         sheets_append_row(2, sender, comment)
            #     if len(textMessage) > 2 and next_simbol not in nums and prev_simbol not in nums:
            #         user_data[sender]["degree"] = 2
            #         comment = textMessage
            #         user_data[sender]["comment"] = comment
            #         greenAPI.sending.sendMessage(
            #             chatId=chatId, message=text_of_not_good_degree)
            #         sheets_append_row(2, sender, comment)

            # elif "3" in textMessage:
            #     index = textMessage.index("3")
            #     next_simbol = textMessage[index+1]
            #     prev_simbol = textMessage[index-1]
            #     if textMessage == "3":
            #         user_data[sender]["degree"] = 3
            #         comment = textMessage
            #         user_data[sender]["comment"] = comment
            #         greenAPI.sending.sendMessage(
            #             chatId=chatId, message=text_of_good_degree)
            #         sheets_append_row(3, sender, comment)
            #     if len(textMessage) > 2 and next_simbol not in nums and prev_simbol not in nums:
            #         user_data[sender]["degree"] = 3
            #         comment = textMessage
            #         user_data[sender]["comment"] = comment
            #         greenAPI.sending.sendMessage(
            #             chatId=chatId, message=text_of_not_good_degree)
            #         sheets_append_row(3, sender, comment)

            # elif "4" in textMessage:

        except Exception as ex:
            print(ex)
            pass
        print(sender)

def sheets_append_row(degree, phone, comment, feedback_data=None):
    # Указываем путь к JSON
    gc = gspread.service_account(
        filename='brave-design-383019-841912aaeec5.json')
    # Открываем тестовую таблицу
    sh = gc.open("FeedBack ")
    # print(sh)
    worksheet = sh.get_worksheet(0)
    date = datetime.now()
    str_date = date.strftime( "%d//%m//%Y")
    str_time = date.strftime("%H:%M:%S")
    values = ([degree, phone, comment,str_date,str_time])
    worksheet.append_row(values=values)


if __name__ == "__main__":
    greenAPI.webhooks.startReceivingNotifications(onEvent)

