FROM python:latest

COPY / /app
ADD requirements.txt /app/
WORKDIR /app

RUN pip install -r requirements.txt

CMD ["python", "app.py"]