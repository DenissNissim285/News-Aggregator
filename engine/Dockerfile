
FROM python:3.10.7-slim


WORKDIR /app

COPY ../hfaccessor /app/hfaccessor


COPY . /app/


RUN pip install --no-cache-dir -r /app/engine/requirements.txt


EXPOSE 8000

ENV PYTHONPATH=/app


CMD ["python", "/app/engine/engine.py"]
