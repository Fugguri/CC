from utils.wats import Watsapp
from DB_connectors.sqlite_connection import Database
from config import TOKEN_API, ID_INSTANCE, API_TOKEN_INSTANCE


if __name__ == "__main__":
    db = Database("CC.db")
    wa = Watsapp(ID_INSTANCE, API_TOKEN_INSTANCE, db)
    wa.start_receive()
