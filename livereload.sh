#!/usr/bin/env bash
find . -regex '\(.*.py\|.*.html\)'  | entr -r env ADMIN_PASSWORD=password ADMIN_USER=admin FLASK_APP=dagensdatalog.py flask run
