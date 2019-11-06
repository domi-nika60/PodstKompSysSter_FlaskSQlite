FROM python:3-alpine
WORKDIR /

COPY ./requirements.txt ./requirements.txt
COPY ./pkssLogs.py ./pkssLogs.py

RUN \
 apk add --no-cache postgresql-libs && \
 apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev && \
 python3 -m pip install -r requirements.txt --no-cache-dir && \
 apk --purge del .build-deps

RUN pip install -r ./requirements.txt --no-cache-dir

EXPOSE 5000

CMD env FLASK_APP=pkssLogs.py flask run --host=0.0.0.0