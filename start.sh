#!/bin/bash

echo "Street parking API service start"

cd server;

python3 manage.py runserver
