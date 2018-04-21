FROM nginx:1.11

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

RUN rm -rf /etc/nginx/conf.d
COPY docker/nginx/conf.d /etc/nginx/conf.d
COPY docker/nginx/ssl /etc/nginx/ssl
COPY frontend /usr/src/app/frontend
COPY backend/static /usr/src/app/backend/static
