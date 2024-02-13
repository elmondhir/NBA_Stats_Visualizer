FROM python:3.10

ENV PYTHONUNBUFFERED = 1

WORKDIR /code

COPY . .

RUN apt-get update && apt-get install -y \
    libgeos-dev

RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["sh", "-c", "python -B manage.py runserver 0.0.0.0:8000"]