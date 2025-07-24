#!/bin/bash
rm -rf authentication/migrations/*
rm -rf profils/migrations/*
rm db.sqlite3

python manage.py makemigrations profils authentification
python manage.py migrate

./populate.sh

python3 manage.py runserver