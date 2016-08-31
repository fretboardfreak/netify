FROM tiangolo/uwsgi-nginx:python3.5

MAINTAINER Curtis Sand <curtissand@gmail.com>

# Clean up Tiangolo's example app
RUN rm -rf /app/*
RUN mkdir -p /app

# Add NGINX Configuration
COPY docker/nginx.conf /etc/nginx/conf.d/nginx.conf

# Add the UWSGI ini file
# Application must go into "/app" with a "/app/uwsgi.ini" configured.
COPY docker/uwsgi.ini /app/uwsgi.ini

# Install the python dependencies
COPY requirements.txt /tmp/requirements.txt
RUN pip install -U -r /tmp/requirements.txt
RUN rm /tmp/requirements.txt

# Add the flask application
COPY src/netify /app/netify

# The UWSGI Setup looks for the object "app" in "/app/main.py"
COPY docker/uwsgi.py /app/main.py

# Add the Netify Config File
COPY docker/netify.cfg /etc/netify.cfg
