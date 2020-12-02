FROM python:3.7-alpine as base
FROM base as builder
WORKDIR /app
COPY ./app_runner.py .
COPY ./config.py .
COPY ./create_vpn.py .
COPY ./requirements.txt .
RUN pip install -r requirements.txt
CMD ["python", "./app_runner.py"]