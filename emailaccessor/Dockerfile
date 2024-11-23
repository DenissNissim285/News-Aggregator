
FROM python:3.10.7-slim


WORKDIR /app


COPY emailaccessor/requirements.txt /app/


RUN pip install --no-cache-dir -r /app/requirements.txt


COPY . /app/


EXPOSE 8000

ENV PYTHONPATH=/app

CMD ["python", "/app/emailaccessor/EmailAccessor.py","run"]
