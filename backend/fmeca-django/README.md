# Backend
This is the backend part of the project. \
Here you can find the implementation of the database and the api.

## How to run

This guide takes for granted that the backend is capable of connecting to an\
external database and shows how to update the django database models for \
the api. 

- **python3 manage.py makemigrations**\
Creates new models based on django code in _/api/models.py_

- **python3 manage.py migrate**\
Pushes the models made by the previous command to a database \
specified in _/backend/settings.py_ making them available for use

- **python3 manage.py runserver**\
Starts a local development-server for the rest api and thus make \
it possible to use as endpoints for data-transfer between parser \
and database
