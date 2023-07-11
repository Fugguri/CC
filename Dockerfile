FROM python:3.11

COPY . .


RUN pip install --no-cache-dir -r requirements.txt

CMD ["python","main.py","&&","python","wa_bot.py"]