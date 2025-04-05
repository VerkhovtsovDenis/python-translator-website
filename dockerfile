
FROM python:3.12.3-alpine as app

RUN apk add --no-cache --virtual .build-deps \
    gcc \
    python3-dev \
    musl-dev \
    postgresql-dev \
    && pip install --no-cache-dir --upgrade pip

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

RUN apk del .build-deps

COPY . .

EXPOSE 8000

RUN chmod +x /app/run.sh

# NGINX-образ со статическими файлами.
FROM nginx:stable-alpine as frontend

WORKDIR /www

COPY translator_project/static /app/static

COPY .werf/nginx.conf /etc/nginx/nginx.conf

# ENTRYPOINT ["/app/run.sh"]
