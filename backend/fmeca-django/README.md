# Backend
This is the backend part of the project, here you can find the implementation
of the database and the api.

## How to run

- sudo /etc/init.d/mysql start
to start the local database.

- python3 manage.py makemigrations
to create new models defined in api/models.py.

- python3 manage.py migrate
to push the models into the mysql database.

- python3 manage.py runserver
starts a development-server and makes the api go live.
