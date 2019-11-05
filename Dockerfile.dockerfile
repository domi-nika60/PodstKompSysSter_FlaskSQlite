FROM tiangolo/uwsgi-nginx-flask:python3.7

COPY requirements.txt /

WORKDIR /

RUN pip install -r ./requirements.txt --no-cache-dir

EXPOSE 8080

CMD python && from pkssLogs import db ; db.create_all() ; exit() && python pkssLogs.py