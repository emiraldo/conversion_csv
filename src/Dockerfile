FROM python:3
ENV PYTHONUNBUFFERED 1
ENV C_FORCE_ROOT=1

RUN mkdir /usr/src/app
WORKDIR /usr/src/app

COPY requirements.txt /usr/src/app
RUN pip install -r requirements.txt
COPY . /usr/src/app
EXPOSE 8000