from django.test import TestCase

from information.models import Company
from information.scripts import import_company_json


class CompanyImportTestCase(TestCase):
    def test_company_import_input_type(self):
        # check no inpur raises exception
        with self.assertRaises(TypeError):
            import_company_json()

        # check wrong data type raises exception
        input_data = {}
        self.assertTrue(isinstance(input_data, dict))
        with self.assertRaises(TypeError):
            import_company_json(input_data)

        # check that valid input returns a valid empty list of issues
        input_data = []
        self.assertTrue(isinstance(input_data, list))
        issues, count = import_company_json(input_data)
        self.assertEqual(issues, [])

    def test_company_import_valid_case(self):
        input_data = [{'index': 0, 'company': 'NETBOOK'}, {'index': 1, 'company': 'PERMADYNE'}]
        issues, count = import_company_json(input_data)
        self.assertEqual(issues, [])
        self.assertEqual(Company.objects.all().count(), 2)
        self.assertEqual(Company.objects.get(index=0).name, 'NETBOOK')
        self.assertEqual(Company.objects.get(index=1).name, 'PERMADYNE')

    def test_company_import_invalid_case(self):
        input_data = [{'index': 0, 'company': 'NETBOOK'}, {'index': 0, 'company': 'NETBOOK'}, {'index': 1}, {'company': 'PERMADYNE'}]
        issues, count = import_company_json(input_data)
        self.assertEqual(set(issues),
                         set(["Company: {'index': 0, 'company': 'NETBOOK'} already exists.",
                              "Company: {'index': 1} missing 'company' key.",
                              "Company: {'company': 'PERMADYNE'} missing 'index' key."]))
        self.assertEqual(Company.objects.all().count(), 1)
        self.assertEqual(Company.objects.get(index=0).name, 'NETBOOK')
