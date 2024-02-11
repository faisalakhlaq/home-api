# ===========
# DEVELOPMENT
# ===========

FROM python:3.10.6-alpine AS dev-api
LABEL authors="Faisal Akhlaq & Rahim Ismaili"

# Prevents Python from writing pyc files to disc (equivalent to python -B option)
ENV PYTHONDONTWRITEBYTECODE=1 
# Prevents Python from buffering stdout and stderr (equivalent to python -u option)
ENV PYTHONUNBUFFERED=1

WORKDIR /homeapi
RUN addgroup -S homeapiuser && adduser -S homeapiuser -G homeapiuser

RUN apk update --no-cache
# Install dependencies for requirements
RUN apk add --no-cache --virtual .tmp-build-deps \
    gcc libc-dev linux-headers postgresql-dev musl-dev \
    zlib zlib-dev 
RUN apk add --no-cache --virtual .tmp-lxml-deps \
    libxml2 libxml2-dev libxslt-dev libxslt

RUN pip install --upgrade pip

# Copy the requirement over to the working directory and install
COPY requirements.txt /homeapi/
COPY requirements-dev.txt /homeapi/
RUN pip install --prefix /usr/local --no-warn-script-location --no-cache-dir -r requirements.txt
RUN pip install --prefix /usr/local --no-warn-script-location --no-cache-dir -r requirements-dev.txt

RUN apk del .tmp-build-deps
RUN apk del .tmp-lxml-deps

USER homeapiuser

CMD sh

# ==========
# PRODUCTION
# ==========
# FROM python:3.10-alpine AS prod-api

# ENV PYTHONDONTWRITEBYTECODE=1 
# ENV PYTHONUNBUFFERED=1

# WORKDIR /homeapi
# RUN addgroup -S homeapiuser && adduser -S homeapiuser -G homeapiuser

# RUN apk update --no-cache
# # Install dependencies for requirements
# RUN apk add --no-cache --virtual .tmp-build-deps \
#     gcc libc-dev linux-headers postgresql-dev musl-dev \
#     zlib zlib-dev 
# RUN apk add --no-cache --virtual .tmp-lxml-deps \
#     libxml2 libxml2-dev libxslt-dev libxslt

# RUN pip install --upgrade pip
