# Paranuara Challenge API
By Anthony Joseph

## Installation
* Install Python 3 if otherwise not installed
* Create a virtual environment:
```console
$ python3 -m venv ~/.virtualenvs/paranuara_api
$ source ~/.virtualenvs/paranuara_api/bin/activate
``` 
* Install dependencies
```console
$ pip install -r requirements.txt
``` 
* Setup initial dataset
```console
$ python manage.py migrate
$ python manage.py TBD
``` 
* Run server on port 8000
```console
$ python manage.py runserver 8000
``` 
* (optional) Change the `SECRET_KEY`in `ParanuaraAPI/settings.py`.
* (optional) View [API documentation](www.tbd.com).

## Design decisions
* Django REST framework was used to add API support to this project.

## Assumptions
* No API authentication is required, as the problem statement did not indicate the way that this API would be accessed. 
To that end, Django REST framework supports a variety of a [authentication methods](https://www.django-rest-framework.org/api-guide/authentication/).
* The data import policy is rather permissive: the import script will do its best to import data into the database, but will warn if a particular action is not possible.
