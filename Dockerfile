FROM python:3

MAINTAINER "Arnau Mora"

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8080

VOLUME /usr/src/app/cache

CMD [ "python", "./app.py" ]
