import json
import uuid
from decimal import Decimal

from datetime import datetime
from django.test import TestCase, Client
from rest_framework import status

from information.models import Person, Company, Food
from information.scripts import import_people_json


class APITestCase(TestCase):
    def setUp(self):
        self.company = Company.objects.create(index=0, name="TEST")
        Company.objects.create(index=1, name="EMPTY")
        self.person = Person.objects.create(index=0,
                                            guid=uuid.uuid4(),
                                            balance=Decimal(123.45),
                                            age=34,
                                            registered=datetime.now(),
                                            name="Anthony Joseph",
                                            company=self.company)
        self.person.favourite_foods.add(Food.objects.create(name="apple", type=Food.FRUIT))
        self.person.favourite_foods.add(Food.objects.create(name="banana", type=Food.FRUIT))
        self.person.favourite_foods.add(Food.objects.create(name="carrot", type=Food.VEGETABLE))
        self.person.save()
        self.person_homer = Person.objects.create(index=1,
                                            guid=uuid.uuid4(),
                                            balance=Decimal(12.45),
                                            age=45,
                                            registered=datetime.now(),
                                            name="Homer Simpson",
                                            company=self.company)
        self.person_marge = Person.objects.create(index=2,
                                            guid=uuid.uuid4(),
                                            balance=Decimal(23.45),
                                            age=56,
                                            registered=datetime.now(),
                                            name="Marge Simpson",
                                            company=self.company)
        self.client = Client()

    def test_get_company(self):
        response = self.client.get('/company/0/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(json.loads(response.content.decode('UTF-8')),
                             {'employees': [{'name': 'Anthony Joseph'}, {'name': 'Homer Simpson'},{'name': 'Marge Simpson'}],
                              'name': 'TEST'})

    def test_get_company_no_employees(self):
        response = self.client.get('/company/1/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(json.loads(response.content.decode('UTF-8')),
                             {'employees': [], 'name': 'EMPTY'})

    def test_get_company_doesnt_exist(self):
        response = self.client.get('/company/2/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_person_food_likes(self):
        response = self.client.get('/person-food/0/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(json.loads(response.content.decode('UTF-8')),
                             {'username': 'Anthony Joseph', 'age': 34, 'fruits': ['apple', 'banana'], 'vegetables': ['carrot']})

    def test_get_person_food_likes_person_doesnt_exist(self):
        response = self.client.get('/person-food/42/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
