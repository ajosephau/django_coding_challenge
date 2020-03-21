# Paranuara API Challenge
By Anthony Joseph

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

## Notes
* (Design decision) Django REST framework was used to add API support to this project due to its popularity and my familiarity with the framework.
* (Design decision) Under normal circumstances, I would discuss whether fixtures should be included in the repo or not with the development team and stakeholders (depending on the business need, and whether personally-identifiable information (PII) is stored in the fixtures). For convenience, the fixtures are included.
* (Design decision) The data import policy is conservative: for example, duplicate data is detected. Data imports happen within a transaction block, so if an exception is raised than the entire operation fails.
* (Design decision) No API authentication is assumed to be  required, as the problem statement did not indicate the way that this API would be accessed. To that end, Django REST framework supports a variety of a [authentication methods](https://www.django-rest-framework.org/api-guide/authentication/).
* (Design decision) Model fields may differ from the fields in the source data where the names don't conform to Python standards (eg. ```eyeColor``` in the ```people.json``` file, compared to ```eye_colour``` in the ```Person```model.
* (Assumption) For simplicity, I treated addresses as a text field as the structure of Paranuaran addresses is unknown. In a real solution I would look to properly parse the address into an appropriate structure.
* (Assumption) Person balances are conveniently expressed in USD, despite living in Paranuara.
* (Assumption) that it's valid for a person to not belong to a company, especially if a company is deleted.
* (Assumption) ```company_id``` in file ```people.json``` appears to be offset by one compared to the ```index``` value in ```companies.json```. The file ```information\scripts.py``` does this transformation.
* (Improvement) Some duplicated logic can be abstracted into helper functions - due to the limited time to complete this exercise I left this as a future task.
* (Improvement) There isn't as much testing around the person import validation that there is in the company input validation.