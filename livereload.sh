#!/usr/bin/env bash
find . -name \*.py | entr -r env FLASK_APP=Dagensdatalog.py flask run
