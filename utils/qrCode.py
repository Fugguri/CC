import qrcode
from aiogram.types import InputFile
from io import BytesIO

def generate_qrcode(text):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    buf = BytesIO()
    qr.add_data(text)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img.save(buf, format='PNG')
    buf.seek(0)
    return InputFile(buf, "qrcode.png")
