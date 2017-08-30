FROM ubuntu:latest

MAINTAINER Ulrik Djurtoft "ullebe1@gmail.com"

RUN apt-get update -y && \
    apt-get install -y python-pip python-dev python-virtualenv gunicorn

# We copy just the requirements.txt first to leverage Docker cache
#COPY ./requirements.txt /app/requirements.txt
#
#WORKDIR /app
#
#RUN pip install -r requirements.txt
#
#COPY . /app
#
#ENTRYPOINT [ "python" ]
#
#CMD [ "Dagensdatalog.py" ]


# Setup flask application
RUN mkdir -p /deploy/app
COPY gunicorn_config.py /deploy/gunicorn_config.py
COPY Dagensdatalog.py /deploy/app/Dagensdatalog.py
COPY ./requirements.txt /deploy/app/requirements.txt
RUN pip install -r /deploy/app/requirements.txt
WORKDIR /deploy/app

EXPOSE 80

# Start gunicorn
CMD ["/usr/bin/gunicorn", "--config", "/deploy/gunicorn_config.py", "Dagensdatalog:app"]
