FROM python:alpine

ENV PYTHONDONTWRITEBYCODE 1
ENV PYTHONUNBUFFERED 1
ENV DJANGO_SUPERUSER_PASSWORD admin

RUN mkdir /app
WORKDIR /app

RUN apk update
RUN apk add --no-cache gcc python3-dev musl-dev mariadb-dev

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

RUN apk del gcc python3-dev musl-dev

CMD while ! python3 manage.py sqlflush > /dev/null 2>&1 ; do sleep 1 ; done && \
    python3 manage.py makemigrations --noinput && \
    python3 manage.py migrate --noinput && \
    python3 manage.py collectstatic --input && \
    python3 manage.py createsuperuser --user admin --email admin@gmail.com --input; \
    gunicron -b 0.0.0.0:8000 sib_cafe.wsgi
