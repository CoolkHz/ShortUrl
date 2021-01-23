FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

# Bash
RUN rm /bin/sh && ln -s /bin/bash /bin/sh

# Time
ENV TZ "Asia/Shanghai"
ENV TERM xtermENV TERM xterm

# PIP Mirror
RUN mkdir -p /root/.pip/
ADD /pip.conf /root/.pip/
RUN rm -rf /code/ && mkdir -p /code/
COPY ./requirements.txt /code

WORKDIR /code/

# Log dir
RUN mkdir -p /app/logs/

# Requirements install
RUN pip install --no-cache-dir -r requirements.txt