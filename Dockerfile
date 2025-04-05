
FROM python:3.12.3-alpine

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

ENTRYPOINT ["/app/run.sh"]
