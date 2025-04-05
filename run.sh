#!/bin/sh

python translator_project/manage.py makemigrations
python translator_project/manage.py migrate
python translator_project/manage.py collectstatic
python translator_project/manage.py runserver 0.0.0.0:8000