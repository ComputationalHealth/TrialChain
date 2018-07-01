FROM python:3.6-alpine

RUN adduser -D webportal

WORKDIR /home/webportal
RUN apk --update add alpine-sdk postgresql py-psycopg2 postgresql-dev libffi-dev gmp-dev

COPY requirements.txt requirements.txt

RUN python -m venv venv
RUN venv/bin/pip install -U pip setuptools
RUN venv/bin/pip install -r requirements.txt

COPY app app
COPY migrations migrations
COPY webportal.py config.py boot.sh ./
RUN chmod a+x boot.sh

ENV FLASK_APP webportal.py

RUN chown -R webportal:webportal ./
USER webportal

EXPOSE 5000
ENTRYPOINT ["./boot.sh"]
