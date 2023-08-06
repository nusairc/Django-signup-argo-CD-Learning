FROM ubuntu
WORKDIR /app

COPY . .

RUN apt-get update && \
    apt-get install -y python3 python3-pip && \
    pip3 install Django && \
    pip install psycopg2-binary

ENTRYPOINT ["python3","manage.py","runserver", "0.0.0.0:8010"]