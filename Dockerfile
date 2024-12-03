FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt
RUN pip install psycopg2-binary


COPY . /app/

ENV FLASK_APP=app.py
ENV FLASK_ENV=prod

CMD ["flask", "run", "--host=0.0.0.0"]
