# -*- coding: utf-8 -*-
import json
import uuid
from datetime import datetime, timezone
from decimal import Decimal

from django.test import Client, TestCase
from rest_framework import status

from information.models import Company, Food, Person


class APITestCase(TestCase):
    def setUp(self) -> None:
        self.company = Company.objects.create(index=0, name="TEST")
        Company.objects.create(index=1, name="EMPTY")
        self.person = Person.objects.create(
            index=0,
            guid=uuid.uuid4(),
            balance=Decimal(123.45),
            age=34,
            registered=datetime.now(timezone.utc),
            name="Anthony Joseph",
            company=self.company,
        )
        self.person.favourite_foods.add(
            Food.objects.create(name="apple", type=Food.FRUIT)
        )
        self.person.favourite_foods.add(
            Food.objects.create(name="banana", type=Food.FRUIT)
        )
        self.person.favourite_foods.add(
            Food.objects.create(name="carrot", type=Food.VEGETABLE)
        )
        self.person.save()
        self.person_homer = Person.objects.create(
            index=1,
            guid=uuid.uuid4(),
            balance=Decimal(12.45),
            age=45,
            registered=datetime.now(timezone.utc),
            name="Homer Simpson",
            company=self.company,
            address="742 Evergreen Terrace, Springfield",
            phone="+123456789",
        )
        self.person_marge = Person.objects.create(
            index=2,
            guid=uuid.uuid4(),
            balance=Decimal(23.45),
            age=56,
            registered=datetime.now(timezone.utc),
            name="Marge Simpson",
            company=self.company,
            address="742 Evergreen Terrace, Springfield",
            phone="+123456789",
        )
        self.person_ned = Person.objects.create(
            index=4,
            guid=uuid.uuid4(),
            balance=Decimal(23.45),
            age=65,
            registered=datetime.now(timezone.utc),
            name="Ned Flanders",
            has_died=False,
            eye_colour="brown",
            address="740 Evergreen Terrace, Springfield",
            phone="+134567890",
        )
        self.person_maude = Person.objects.create(
            index=5,
            guid=uuid.uuid4(),
            balance=Decimal(43.45),
            age=65,
            registered=datetime.now(timezone.utc),
            name="Maude Flanders",
            has_died=False,
            eye_colour="brown",
            address="740 Evergreen Terrace, Springfield",
            phone="+134567890",
        )
        self.person_homer.friends.add(self.person_maude)
        self.person_homer.save()

        self.person_marge.friends.add(self.person_ned)
        self.person_marge.friends.add(self.person_maude)
        self.person_marge.save()

        self.client = Client()

    def test_get_company(self) -> None:
        response = self.client.get("/company/0/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(
            json.loads(response.content.decode("UTF-8")),
            {
                "employees": [
                    {"name": "Anthony Joseph"},
                    {"name": "Homer Simpson"},
                    {"name": "Marge Simpson"},
                ],
                "name": "TEST",
            },
        )

    def test_get_company_no_employees(self) -> None:
        response = self.client.get("/company/1/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(
            json.loads(response.content.decode("UTF-8")),
            {"employees": [], "name": "EMPTY"},
        )

    def test_get_company_doesnt_exist(self) -> None:
        response = self.client.get("/company/2/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_person_food_likes(self) -> None:
        response = self.client.get("/person-food/0/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(
            json.loads(response.content.decode("UTF-8")),
            {
                "username": "Anthony Joseph",
                "age": 34,
                "fruits": ["apple", "banana"],
                "vegetables": ["carrot"],
            },
        )

    def test_get_person_food_likes_person_doesnt_exist(self) -> None:
        response = self.client.get("/person-food/42/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_getmutual_friends_alive_with_brown_eyes(self) -> None:
        response = self.client.get("/mutual-friends-alive-brown-eyes/1/2/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(
            json.loads(response.content.decode("UTF-8")),
            {
                "mutual_friends": [{"name": "Maude Flanders"}],
                "person_one": {
                    "address": "742 Evergreen Terrace, Springfield",
                    "age": 45,
                    "name": "Homer Simpson",
                    "phone": "+123456789",
                },
                "person_two": {
                    "address": "742 Evergreen Terrace, Springfield",
                    "age": 56,
                    "name": "Marge Simpson",
                    "phone": "+123456789",
                },
            },
        )

    def test_getmutual_friends_alive_with_brown_eyes_no_mutual_friends(self) -> None:
        response = self.client.get("/mutual-friends-alive-brown-eyes/4/1/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(
            json.loads(response.content.decode("UTF-8")),
            {
                "mutual_friends": [],
                "person_one": {
                    "address": "740 Evergreen Terrace, Springfield",
                    "age": 65,
                    "name": "Ned Flanders",
                    "phone": "+134567890",
                },
                "person_two": {
                    "address": "742 Evergreen Terrace, Springfield",
                    "age": 45,
                    "name": "Homer Simpson",
                    "phone": "+123456789",
                },
            },
        )

    def test_getmutual_friends_alive_with_brown_eyes_person_doesnt_exist(self) -> None:
        response = self.client.get("/mutual-friends-alive-brown-eyes/42/0/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
