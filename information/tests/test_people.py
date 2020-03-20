from django.test import TestCase

from information.scripts import import_people_json


class PeopleImportTestCase(TestCase):
    def test_people_import_input_type(self):
        # check no inpur raises exception
        with self.assertRaises(TypeError):
            import_people_json()

        # check wrong data type raises exception
        input_data = {}
        self.assertTrue(isinstance(input_data, dict))
        with self.assertRaises(TypeError):
            import_people_json(input_data)

        # check that valid input returns a valid empty list of issues
        input_data = []
        self.assertTrue(isinstance(input_data, list))
        issues, count = import_people_json(input_data)
        self.assertEqual(issues, [])
