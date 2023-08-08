FROM python:3.8-slim

WORKDIR /usr/src/app

COPY requirements.txt /usr/src/app/

RUN pip install --no-cache-dir -r requirements.txt

COPY . /usr/src/app/

EXPOSE 5000

CMD [ "python","app.py" ]

