FROM python:alpine

EXPOSE 5000:80

MAINTAINER Ulrik Djurtoft "ullebe1@gmail.com"

# Prepare app dir
RUN mkdir -p /app/uploads /app/pictures
WORKDIR /app

# Copy flask application
COPY templates ./templates
COPY pictures ./pictures
COPY dagensdatalog.py ./dagensdatalog.py
COPYs slogans.txt ./slogans.txt
COPY requirements.txt ./requirements.txt

# Install packages
RUN pip install --no-cache-dir -r requirements.txt

# Start app
CMD [ "python", "dagensdatalog.py" ]