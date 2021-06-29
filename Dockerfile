FROM python:3.7-alpine

COPY . /app

WORKDIR /app

RUN pip3 install -r requirements.txt && \
    chmod +x app/scheduler.py

ENTRYPOINT [ "python3.7", "./app/scheduler.py" ]
CMD []
