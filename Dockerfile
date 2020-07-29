# Base image - python 3.7
FROM python:3.7

# Author who is maintaining this Dockerfile
MAINTAINER Pooja P <pooja.prakash33@gmail.com>

# Creating app(prometheus_service_expose) directory
RUN mkdir -p /opt/prometheus_service_expose/src

# Installing dependencies and copying source app
COPY ./requirements.txt /opt/prometheus_service_expose/
COPY ./src/app.py /opt/prometheus_service_expose/src/
RUN pip install -r /opt/prometheus_service_expose/requirements.txt

# Working directory for this docker image
WORKDIR /opt/prometheus_service_expose/

# Exposing the port
EXPOSE 5000

# Adding path to environment variable PYTHONPATH
ENV PYTHONPATH '/opt/prometheus_service_expose/'

# Command to execute when docker container starts
CMD ["python" , "/opt/prometheus_service_expose/src/app.py"]
