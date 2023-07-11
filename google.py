import gspread


def google_sheet_update(degree, phone, comment, feedback_data=None):
    # Указываем путь к JSON
    gc = gspread.service_account(
        filename='brave-design-383019-841912aaeec5.json')
    # Открываем тестовую таблицу
    sh = gc.open("degree")
    # print(sh)
    worksheet = sh.get_worksheet(0)

    values = ([degree, phone, comment, feedback_data])

    worksheet.append_row(values=values)


def google_sheet_upda(degree=None, phone=None, comment=None, feedback_data=None):
    # Указываем путь к JSON
    gc = gspread.service_account(
        filename='brave-design-383019-841912aaeec5.json')
    # Открываем тестовую таблицу
    sh = gc.open("degree")
    # print(sh)
    worksheet = sh.get_worksheet(0)

    values = ([degree, phone, comment, feedback_data])

    cell = worksheet.find("79502213750@c.us")

    print(cell.row, cell.coll)


google_sheet_upda()
