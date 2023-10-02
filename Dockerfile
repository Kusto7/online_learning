FROM python:3

WORKDIR /online_learning

COPY ./requirements.txt .

RUN pip install -r requirements.txt

COPY . .
