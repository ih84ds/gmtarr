FROM python:3.7 as dev

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

FROM dev as prod

COPY . .

EXPOSE $PORT
CMD gunicorn --bind "0.0.0.0:${PORT}" --workers 1 --threads 4 roundrobin.wsgi