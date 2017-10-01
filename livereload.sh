#!/usr/bin/env bash
find . -regex '\(.*.py\|.*.html\)'  | entr -r env FLASK_APP=dagensdatalog.py flask run
