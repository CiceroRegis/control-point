FROM python:3.6-alpine
WORKDIR /app
ADD . /app/
ENV TZ America/Sao_Paulo
RUN echo "151.101.112.249 dl-cdn.alpinelinux.org" >> /etc/hosts \
    && apk --update add --no-cache tzdata mariadb-dev build-base gcc musl-dev libffi-dev libjpeg zlib tiff-dev \
    && ln -snf /usr/share/zoneinfo/$TZ /etc/localtime \
    && echo $TZ > /etc/timezone \
    && pip install --upgrade pip && pip install --no-cache-dir --trusted-host pypi.python.org -r /app/requirements.txt \
    && addgroup -g 1000 -S app \
    && adduser -u 1000 -S app -G app \
    && mkdir -p /app/media \
    && chown app:app -R /app

USER app

CMD ["/usr/local/bin/gunicorn", "project_config.wsgi:application", \
    "--pid", "/app/logs/app.pid", \
    "--user", "app", \
    "--timeout", "60", \
    "--bind", "0.0.0.0:9010", \
    "--log-level", "warning"]

