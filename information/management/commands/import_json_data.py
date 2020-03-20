import json
from pathlib import Path

from django.core.management.base import BaseCommand, CommandError

from information.scripts import import_company_json


class Command(BaseCommand):
    help = 'Imports data from JSON files'

    def add_arguments(self, parser):
        parser.add_argument('company_json_path', type=str)
        parser.add_argument('people_json_path', type=str)

    def handle(self, *args, **options):
        company_json_path = options.get('company_json_path')

        # Import company data
        if not company_json_path:
            raise CommandError("Company JSON path required")
        my_file = Path(company_json_path)
        num_companies = 0

        if my_file.is_file():
            self.stdout.write(self.style.NOTICE(f'Starting to import company data...'))
            with open(company_json_path) as company_json_file:
                company_data = json.load(company_json_file)
                num_companies = len(company_data)
                self.stdout.write(self.style.NOTICE(f'Estimated number of companies to be imported: {num_companies}'))

                company_issues, num_companies = import_company_json(company_data)

                for idx, issue in enumerate(company_issues):
                    self.stdout.write(self.style.ERROR(f'Issue {idx+1}/{len(company_issues)}: {issue}'))
                if company_issues:
                    raise CommandError(f"{len(company_issues)} issues detected: stopping import.")
        else:
            raise CommandError(f"Unable to find company file: {company_json_path}")

        self.stdout.write(self.style.SUCCESS(f'Successfully imported {num_companies} companies.'))