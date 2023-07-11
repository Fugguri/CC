import re
import mammoth
import datetime
from docx.text.paragraph import Paragraph
from docx.oxml.xmlchemy import OxmlElement


def move_table_after(document, table, search_phrase):
    regexp = re.compile(search_phrase)
    for paragraph in document.paragraphs:
        if paragraph.text and regexp.search(paragraph.text):
            tbl, p = table._tbl, paragraph._p
            p.addnext(tbl)
            return paragraph


def insert_paragraph_after(paragraph, text=None, style=None, bold=None):
    """Insert a new paragraph after the given paragraph."""
    new_p = OxmlElement("w:p")
    paragraph._p.addnext(new_p)
    new_para = Paragraph(new_p, paragraph._parent)
    if text:
        text = new_para.add_run(text)
    if bold:
        text.bold = True

    if style is not None:
        new_para.style = style
    return new_para


async def prepair_dock(receiver, path=None):
    if receiver[-1] not in ["nan", None]:
        voter = receiver[-1]
    else:
        voter = f"{receiver[4]} {receiver[5]} {receiver[6]}"
    text = f"""<b>{receiver[16]}</b><br>
на общем собрании собственников помещений №: {receiver[11]}<br><br>
Прием бюллетеней для голосования: {receiver[12]}, {receiver[13]}<br><br>
<b>Собственник</b>: {receiver[4]} {receiver[5]} {receiver[6]}
<table border="1">
       <tr>
                 <td>
                       Квартира(помещение)(Общая площадь,кв.м - Кадастровый номер):
                 </td>
                 <td>
                       Квартира № {receiver[-4]} ({receiver[-3]}м2 - {receiver[2]})
                 </td>
       </tr>
       <tr>
                 <td>
                       № и дата государственной регистрации права собственности,№ и дата выписки из ЕГРН
                 </td>
                 <td>
                       № {receiver[9]} от {receiver[10]},
                       № {receiver[7]} от {receiver[8]} 
                 </td>
       </tr>

</table><br>

<b>ФИО голосующего</b>: {voter}  <b>E-mail</b>: {receiver[0]}  <b>Телефон</b>: +{receiver[1][0]} XXX XXX {receiver[1][-5:]}<br>
<b>Дата голосования</b>: {datetime.datetime.now().strftime("%d.%m.%Y")}<br>

"""
    doc = open("documents/"+receiver[-7], "rb")
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
