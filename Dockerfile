FROM python:3.7-alpine

COPY . /app

WORKDIR /app

RUN pip3 install -r requirements.txt && \
    chmod +x scheduler.py

ENTRYPOINT [ "python3.7", "./scheduler.py" ]
CMD []
