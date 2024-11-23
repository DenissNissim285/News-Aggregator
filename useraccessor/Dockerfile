
FROM python:3.10.7-slim


WORKDIR /app


COPY . /app/


RUN pip install --no-cache-dir -r /app/useraccessor/requirements.txt


EXPOSE 8000

ENV PYTHONPATH=/app


CMD ["python", "/app/useraccessor/UserAccessor.py"]
