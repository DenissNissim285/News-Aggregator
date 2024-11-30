
FROM python:3.9-slim


WORKDIR /app


COPY ../useraccessor /app/useraccessor

COPY ../newsaccessor /app/newsaccessor

COPY ../emailaccessor /app/emailaccessor

COPY ../engine /app/engine

COPY ../hfaccessor /app/hfaccessor


COPY manager /app/manager


COPY ./templates /app/templates


RUN pip install --no-cache-dir -r /app/manager/requirements.txt
#RUN pip install pika aio_pika

ENV PYTHONPATH="/app"


COPY .env /app/.env

RUN pip install python-dotenv

EXPOSE 8000


CMD ["uvicorn", "manager.manager:app", "--host", "0.0.0.0", "--port", "8000"]

