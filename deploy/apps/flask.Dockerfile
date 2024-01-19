FROM python:3.10-slim

ENV PROJECT_ROOT /project
ENV SRC_DIR /src
ENV FLASK_DIR flask_wines

ARG SERVICE_NUMBER

RUN mkdir $PROJECT_ROOT

RUN apt-get update && \
    apt-get install -y build-essential libpq-dev python3-dev && \
    apt-get clean

COPY ./$SRC_DIR/requirements.txt $PROJECT_ROOT

WORKDIR $PROJECT_ROOT
RUN pip install -r requirements.txt

COPY ./$SRC_DIR/$FLASK_DIR $PROJECT_ROOT

RUN echo "SERVICE_NUMBER=$SERVICE_NUMBER" >> $PROJECT_ROOT/.env
