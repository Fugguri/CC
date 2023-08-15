from dataclasses import dataclass
from datetime import datetime


@dataclass
class User_from_googlesheet():
    data: datetime
    address: str
    phone: str
    name: str
    status: str
    flat_num: str
    email: str
