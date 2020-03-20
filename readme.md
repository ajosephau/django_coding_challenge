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
* Setup initial database and dataset
```console
$ python manage.py migrate
$ python manage.py import_json_data "fixtures/example/companies.json" "fixtures/example/people.json"
``` 
* Run server on port 8000
```console
$ python manage.py runserver 8000
``` 
* (optional) Change the `SECRET_KEY`in `ParanuaraAPI/settings.py`.

## Documentation

Once the server is running, [OpenAPI/Swagger documentation is available](www.tbd.com).

## Testing
 To run the unit tests, use 
```console
$ python manage.py test
``` 

## Design decisions
* Django REST framework was used to add API support to this project due to its popularity and my familiarity with the framework.
* Under normal circumstances, I would discuss whether fixtures should be included in the repo or not with the development team and stakeholders (depending on the business need, and whether PII is stored in the fixtures). For convenience, the fixtures are included.
* The data import policy is conservative: for example, duplicate data is detected. Data imports happen within a transaction block, so if an exception is raised than the entire operation fails.
* No API authentication is assumed to be  required, as the problem statement did not indicate the way that this API would be accessed. To that end, Django REST framework supports a variety of a [authentication methods](https://www.django-rest-framework.org/api-guide/authentication/).
