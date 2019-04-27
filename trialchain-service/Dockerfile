FROM python:3.6.2
MAINTAINER Wade Schulz <wade.schulz@gmail.com>

RUN yes | pip install --upgrade pip
RUN yes | pip install \
		falcon \
		gunicorn \
        savoir \
        requests

ADD src /trialchain
WORKDIR trialchain

CMD ["gunicorn", "-b", "0.0.0.0:80", "trialchain:app"]
