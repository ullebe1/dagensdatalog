FROM ubuntu:latest

MAINTAINER Ulrik Djurtoft "ullebe1@gmail.com"

RUN apt-get update -y && \
    apt-get install -y python3-pip python3-dev python3-virtualenv 
RUN pip3 install gunicorn

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
COPY dagensdatalog.py /deploy/app/dagensdatalog.py
COPY templates /deploy/app/templates
COPY ./requirements.txt /deploy/app/requirements.txt
RUN pip3 install -r /deploy/app/requirements.txt
WORKDIR /deploy/app

EXPOSE 80

# Start gunicorn
CMD ["gunicorn", "--config", "/deploy/gunicorn_config.py", "dagensdatalog:app"]
