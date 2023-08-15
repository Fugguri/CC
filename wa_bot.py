from utils.wats import Watsapp_bot
from DB.sqlite_connection import Database


if __name__ == "__main__":
    db = Database("CC.db")
    wa = Watsapp_bot()
    wa.start_receive()
