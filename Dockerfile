FROM ubuntu:20.04 AS docker_supervisor_backend

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -y && apt-get install -y supervisor nginx uwsgi python3 python3-pip uwsgi-plugin-python3 && rm -rf /var/lib/apt/lists/*
RUN mkdir -p /var/log/supervisor

EXPOSE 80

FROM docker_supervisor_backend

COPY app/requirements.txt /app/requirements.txt
WORKDIR /app
RUN python3 -m pip install -r requirements.txt
COPY app /app

COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf
COPY uwsgi.ini /app/uwsgi.ini
COPY nginx.conf /etc/nginx/nginx.conf

CMD ["/usr/bin/supervisord"]
