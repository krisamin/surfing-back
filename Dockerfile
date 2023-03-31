# surfing-back/Dockerfile

FROM python:3.11.1


COPY ./requirements.txt /requirements.txt
RUN pip install --no-cache-dir --upgrade -r /requirements.txt

COPY ./gunicorn.conf.py /gunicorn.conf.py
COPY ./app /app