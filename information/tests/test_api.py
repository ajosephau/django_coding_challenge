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
        self.person = Person.objects.create(index=1,
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
        self.client = Client()

    def test_get_person_food_likes(self):
        response = self.client.get('/person-food/1/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(json.loads(response.content.decode('UTF-8')),
                             {'username': 'Anthony Joseph', 'age': 34, 'fruits': ['apple', 'banana'], 'vegetables': ['carrot']})