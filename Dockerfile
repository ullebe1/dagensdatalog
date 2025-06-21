FROM python:alpine

LABEL maintainer "ullebe1@gmail.com"
LABEL maintainer "jonastranberg93@gmail.com"

# Set Timezone
RUN apk add --no-cache tzdata
ENV TZ=Europe/Copenhagen

# Expose ports
EXPOSE 80/tcp
EXPOSE 80/udp
EXPOSE 5000/tcp
EXPOSE 5000/udp

# Prepare app dir
RUN mkdir -p /app/data
WORKDIR /app

# Copy flask application
COPY templates ./templates
COPY data ./data
COPY dagensdatalog.py ./dagensdatalog.py
COPY slogans.txt ./slogans.txt
COPY requirements.txt ./requirements.txt

# Install packages
RUN pip install --no-cache-dir -r requirements.txt

# Create group and user with UID and GID 1000
RUN addgroup -g 1000 appgroup && adduser -D -u 1000 -G appgroup appuser

# Set permissions
RUN chown -R 1000:1000 /app/data

# Switch to the numeric user
USER 1000:1000

# Start app
CMD [ "python", "dagensdatalog.py" ]
