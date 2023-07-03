FROM python:3.9-alpine

WORKDIR /app

COPY requirements.txt requirements.txt
RUN apk add --no-cache jpeg-dev zlib-dev
RUN apk add --no-cache --virtual .build-deps build-base linux-headers \
    && pip3 install -r requirements.txt \
    && apk del .build-deps

COPY . .

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
