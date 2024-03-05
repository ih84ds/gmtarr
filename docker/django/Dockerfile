FROM python:3.7

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE $PORT
CMD gunicorn --bind "0.0.0.0:${PORT}" --workers 1 --threads 4 roundrobin.wsgi