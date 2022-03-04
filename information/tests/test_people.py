# -*- coding: utf-8 -*-
from django.test import TestCase

from information.models import Company, Person
from information.scripts import import_people_json


class PeopleImportTestCase(TestCase):
    def setUp(self) -> None:
        self.company = Company.objects.create(index=0, name="TEST")

    def test_people_import_input_type(self) -> None:
        # check no inpur raises exception
        with self.assertRaises(TypeError):
            import_people_json()  # type: ignore

        # check wrong data type raises exception
        input_data = {}  # type: ignore
        self.assertTrue(isinstance(input_data, dict))
        with self.assertRaises(TypeError):
            import_people_json(input_data)

        # check that valid input returns a valid empty list of issues
        input_data = []  # type: ignore
        self.assertTrue(isinstance(input_data, list))
        issues, count = import_people_json(input_data)
        self.assertEqual(issues, [])

    def test_people_import_valid_case(self) -> None:
        input_data = [
            {
                "_id": "595eeb9cd4f669914b94721e",
                "index": 0,
                "guid": "882f83cd-e211-4fb1-aa19-114a086e2afc",
                "has_died": False,
                "balance": "$2,295.84",
                "picture": "http://placehold.it/32x32",
                "age": 35,
                "eyeColor": "brown",
                "name": "Aisha Davis",
                "gender": "female",
                "company_id": 1,
                "email": "aishadavis@earthmark.com",
                "phone": "+1 (910) 426-2287",
                "address": "828 Navy Street, Ada, Idaho, 8913",
                "about": "Voluptate nisi amet ex enim ullamco.\r\n",
                "registered": "2014-04-08T04:33:44 -10:00",
                "tags": ["nulla", "dolore", "consequat"],
                "friends": [{"index": 0}],
                "greeting": "Hello, Aisha Davis! You have 1 unread messages.",
                "favouriteFood": ["strawberry", "beetroot", "carrot", "celery"],
            }
        ]
        issues, count = import_people_json(input_data)
        self.assertEqual(issues, [])
        self.assertEqual(Person.objects.all().count(), 1)
        person_obj = Person.objects.get(index=0)
        self.assertEqual(person_obj.name, "Aisha Davis")
        self.assertEqual(person_obj.friends.first(), person_obj)
        self.assertEqual(
            person_obj.friends_of.first(), person_obj
        )  # check both sides of friendship relationship
        self.assertEqual(
            set(person_obj.favourite_foods.all().values_list("name", flat=True)),
            set(["strawberry", "beetroot", "carrot", "celery"]),
        )
        self.assertEqual(
            set(person_obj.favourite_foods.all().values_list("type", flat=True)),
            set(["frt", "veg", "veg", "veg"]),
        )
        self.assertEqual(
            set(person_obj.tags.all().values_list("name", flat=True)),
            set(["nulla", "dolore", "consequat"]),
        )

    def test_people_import_invalid_case(self) -> None:
        input_data = [{"_id": "595eeb9cd4f669914b94721e", "company_id": 1}]
        issues, count = import_people_json(input_data)
        self.assertEqual(
            issues,
            [
                "Person: {'_id': '595eeb9cd4f669914b94721e', 'company_id': 1} missing 'index' key."
            ],
        )

        input_data = [{"company_index": 1}]
        issues, count = import_people_json(input_data)
        self.assertEqual(issues, ["Person: {'company_index': 1} missing 'index' key."])
