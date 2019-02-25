#!/bin/bash

echo "Street parking API service start"

cd server;

pip3 install -r requirements.txt

python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py runserver
