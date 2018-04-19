FROM python:alpine

MAINTAINER Ulrik Djurtoft "ullebe1@gmail.com"

# Set Timezone
RUN apk add --no-cache tzdata
ENV TZ=Europe/Copenhagen

# Prepare app dir
RUN mkdir -p /app/uploads /app/pictures
WORKDIR /app

# Copy flask application
COPY templates ./templates
COPY pictures ./pictures
COPY dagensdatalog.py ./dagensdatalog.py
COPY slogans.txt ./slogans.txt
COPY requirements.txt ./requirements.txt

# Install packages
RUN pip install --no-cache-dir -r requirements.txt

# Start app
CMD [ "python", "dagensdatalog.py" ]