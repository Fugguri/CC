from dataclasses import dataclass, field
from datetime import datetime

class Models:
    @dataclass
    class User_from_googlesheet():
        data: datetime 
        address: str= field(default="")
        phone: str= field(default="")
        name: str= field(default="")
        status: str= field(default="")
        flat_num: str= field(default="")
        email: str= field(default="")


    @dataclass
    class Meeting:
        id:int|str = field(default="")
        house:int|str = field(default="")
        
    @dataclass
    class House:
        id:int|str = field(default="")
        name:str = field(default="")
        cad_num:str = field(default="")
        
@dataclass
class User_from_googlesheet():
    data: datetime
    _ : str
    phone: str
    name: str
    status: str
    flat_num: str
    email: str
    address: str

@dataclass
class Tenant:
    date_of_create: datetime 
    flat_num: str= field(default="")
    flat_id: str= field(default="")
    flat_status: str= field(default="")
    name: str= field(default="")
    phone: str= field(default="")
    has_watsapp: str= field(default="")
    status: str= field(default="")
    owner_full_name: str= field(default="")
    owner_email: str= field(default="")
    last_email_date: str= field(default="")
    last_oss_number: str= field(default="")
    date_of_sopd: str= field(default="")
    passport: str= field(default="")
    mkd_id: str= field(default="")
    fraction_part: str= field(default="")
    address: str= field(default="")
    owner: str= field(default="")
    cad_num: str= field(default="")

@dataclass
class Meeting:
    pass
