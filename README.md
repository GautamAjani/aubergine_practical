# aubergine_practical


First create virtuenv of python with version 3.6 For that run following command but make sure you have virtualenv is installed on your system

$ virtualenv venv --python=python3.6

Then install all requirements using following command

$ pip install -r requirements.txt

Make sure you have installed Postgres in your system. Then create "aubergine_test db" in postgres. And create its user and password as "root" and "admin" respectively.

# install and setup the Celery and Rabbitmq

open the celery server
$ celery -A django_test  worker -l info

open Rabbitmq server
$ sudo rabbitmq-server

# Run the project
After all setup run project using following command

$ python manage.py runserver
