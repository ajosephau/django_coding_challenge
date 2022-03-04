# Paranuara API Challenge
[![Run Django testing w/ coverage](https://github.com/ajosephau/django_coding_challenge/actions/workflows/django.yml/badge.svg)](https://github.com/ajosephau/django_coding_challenge/actions/workflows/django.yml)
[![codecov](https://codecov.io/gh/ajosephau/django_coding_challenge/branch/master/graph/badge.svg?token=L64OL9ZNK6)](https://codecov.io/gh/ajosephau/django_coding_challenge)

By Anthony Joseph

## Briefing

Paranuara is a `class-m` planet. Those types of planets can support human life, for that reason the president of the Checktoporov decides to send some people to colonise this new planet and
reduce the number of people in their own country. After 10 years, the new president wants to know how the new colony is growing, and wants some information about his citizens. Hence he hired you to build a rest API to provide the desired information.

The government from Paranuara will provide you two json files (located at resource folder) which will provide information about all the citizens in Paranuara (name, age, friends list, fruits and vegetables they like to eat...) and all founded companies on that planet.
Unfortunately, the systems are not that evolved yet, thus you need to clean and organise the data before use.
For example, instead of providing a list of fruits and vegetables their citizens like, they are providing a list of favourite food, and you will need to split that list (please, check below the options for fruits and vegetables).

### New Features
Your API must provides these end points:
- Given a company, the API needs to return all their employees. Provide the appropriate solution if the company does not have any employees.
- Given 2 people, provide their information (Name, Age, Address, phone) and the list of their friends in common which have brown eyes and are still alive.
- Given 1 people, provide a list of fruits and vegetables they like. This endpoint must respect this interface for the output: `{"username": "Ahi", "age": "30", "fruits": ["banana", "apple"], "vegetables": ["beetroot", "lettuce"]}`

## Installation
* Install Python 3 if not installed
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
* (optional) Change the `DEBUG`in `ParanuaraAPI/settings.py` to False if running in production context.

## Documentation

Once the server is running, [OpenAPI/Swagger documentation is available](http://127.0.0.1:8000/swagger/), assuming the server was started up as above.

## Testing
 To run the unit tests, use
```console
$ python manage.py test
```

Or pytest with coverage reporting

```console
$ DJANGO_SETTINGS_MODULE=ParanuaraAPI.settings pytest . --cov . --cov-report term -s --annotate-output=./annotations.json
```

### Type checking

To automatically insert type checks, please run the following commands:

```console
$ DJANGO_SETTINGS_MODULE=ParanuaraAPI.settings pytest . --cov . --cov-report term -s --annotate-output=./annotations.json
$ DJANGO_SETTINGS_MODULE=ParanuaraAPI.settings pyannotate -w --py3 --type-info ./annotations.json information/
$ mypy --install-types information/
```

## Quality Assurance
 To run the quality assurance checks, run
```console
$ pre-commit run --all-files
```

Pre-commit settings are managed in `.pre-commit-config.yaml` and are run on each commit.

## Automated processes
 [Github Actions](https://github.com/ajosephau/django-coding-challenge/actions/workflows/django.yml) run on all commits, with the test suite running with code coverage reports being uploaded as a zipped artifact on each run.

## Notes
### Design decisions
* Django REST framework (DRF) was used to add API support to this project due to its popularity and my familiarity with the framework.
* Under normal circumstances, I would discuss whether fixtures should be included in the repo or not with the development team and stakeholders (depending on the business need, and whether personally-identifiable information (PII) is stored in the fixtures). For convenience, the fixtures are included.
* The data import policy is conservative: for example, duplicate data is detected. Data imports happen within a transaction block, so if an exception is raised than the entire operation fails.
* No API authentication is assumed to be  required, as the problem statement did not indicate the way that this API would be accessed. To that end, Django REST framework supports a variety of a [authentication methods](https://www.django-rest-framework.org/api-guide/authentication/).
* Model fields may differ from the fields in the source data where the names don't conform to Python standards (eg. ```eyeColor``` in the ```people.json``` file, compared to ```eye_colour``` in the ```Person```model.
### Assumptions
* For simplicity, I treated addresses as a text field as the structure of Paranuaran addresses is unknown. In a real solution I would look to properly parse the address into an appropriate structure.
* Person balances are conveniently expressed in USD, despite living in Paranuara.
* That it's valid for a person to not belong to a company, especially if a company is deleted.
* ```company_id``` in file ```people.json``` appears to be offset by one compared to the ```index``` value in ```companies.json```. The file ```information\scripts.py``` does this transformation.
### Improvements
* Some duplicated logic can be abstracted into helper functions - due to the limited time to complete this exercise I left this as a future task.
* There isn't as much testing around the person import validation that there is in the company input validation.
### TODOs
* Rename the main Django project from "information" to something more meaningful
* Implement RESTful endpoints for the models: these endpoints weren't exposed as it wasn't a requirement for the task, but these endpoints are easily added with DRF.
