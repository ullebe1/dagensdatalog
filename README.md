# Dagensdatalog 

[![Docker Build Status](https://img.shields.io/docker/build/dagensdatalog/dagensdatalog-website.svg?style=flat-square)](https://hub.docker.com/r/dagensdatalog/dagensdatalog-website/builds/)

## Development run

Make a virtual enviroment

```bash
virtualenv venv
```
Activate the virtual enviroment

```bash
source venv/bin/activate
```

install dependencies

```bash
pip install -r requirements.txt
```
run it

```bash
python dagensdatalog.py
```

## Docker

To build the image run

```bash
docker build -t dagensdatalog .
```

To run the image 

```bash
docker run -p 5000:5000 dagensdatalog
```

Persistent data mount points

-   /app/uploads
-   /app/pictures
-   /app/db.json

## Admin login

To login to the admin page use "admin" and "password".
To specify the admin login use the enviroment variables "ADMIN_USER" and "ADMIN_PASSWORD".

## Slogans

Feel free to add new slogans in the slogans.txt file. Slogans are separated by newline.
