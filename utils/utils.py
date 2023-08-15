import re
from config import gf_link


class Utils:
    def __init__(self) -> None:
        pass

    def valid_email(self, email):
        return bool(re.search(r"^[\w\.\+\-]+\@[\w]+\.[a-z]{2,3}$", email))

    def has_cyrillic(self, text):
        return bool(re.search('[а-яА-Я]', text))

    def _convert_number(self, phone):
        if phone.startswith("8"):
            phone = "7"+phone[1:]
        if phone.startswith("+"):
            phone = phone[1:]
        if "-" in phone:
            phone = phone.replace('-', '')
        return phone

    def create_gf_link(self,phone:str,address:str):
        
        return gf_link.format(address.replace(" ","+"),phone)
