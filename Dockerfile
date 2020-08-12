FROM python:3
WORKDIR /usr/src/kit-logger-python/
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD [ "python", "./telegram_bot.py" ]
# ^ CMD must have "<command>" and not '<command>'