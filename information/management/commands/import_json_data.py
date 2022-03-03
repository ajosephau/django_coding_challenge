# -*- coding: utf-8 -*-
import json
from pathlib import Path

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from information.scripts import import_company_json, import_people_json


class Command(BaseCommand):
    help = "Imports data from JSON files"

    def add_arguments(self, parser):
        parser.add_argument("company_json_path", type=str)
        parser.add_argument("people_json_path", type=str)

    def handle(self, *args, **options):
        company_json_path = options.get("company_json_path")
        people_json_path = options.get("people_json_path")

        # Check JSON files exist
        if not company_json_path:
            raise CommandError("Company JSON path required")
        company_file = Path(company_json_path)
        if not company_file.is_file():
            raise CommandError(f"Unable to find company file: {company_json_path}")

        if not people_json_path:
            raise CommandError("Person JSON path required")
        person_file = Path(people_json_path)
        if not person_file.is_file():
            raise CommandError(f"Unable to find person file: {people_json_path}")

        with transaction.atomic():
            # Import company data
            self.stdout.write(self.style.NOTICE("Starting to import company data..."))
            with open(company_json_path) as company_json_file:
                company_data = json.load(company_json_file)
                num_companies = len(company_data)
                self.stdout.write(
                    self.style.NOTICE(
                        f"Estimated number of companies to be imported: {num_companies}"
                    )
                )

                company_issues, num_companies = import_company_json(company_data)

                for idx, issue in enumerate(company_issues):
                    self.stdout.write(
                        self.style.ERROR(
                            f"Issue {idx+1}/{len(company_issues)}: {issue}"
                        )
                    )
                if company_issues:
                    raise CommandError(
                        f"{len(company_issues)} issues detected: stopping import."
                    )

                self.stdout.write(
                    self.style.SUCCESS(
                        f"Successfully imported {num_companies} companies."
                    )
                )

            # Import people data
            self.stdout.write(self.style.NOTICE("Starting to import people data..."))
            with open(people_json_path) as people_json_file:
                people_data = json.load(people_json_file)
                num_people = len(people_data)
                self.stdout.write(
                    self.style.NOTICE(
                        f"Estimated number of people to be imported: {num_people}"
                    )
                )

                people_issues, num_people = import_people_json(people_data)

                for idx, issue in enumerate(people_issues):
                    self.stdout.write(
                        self.style.ERROR(f"Issue {idx+1}/{len(people_issues)}: {issue}")
                    )
                if people_issues:
                    raise CommandError(
                        f"{len(people_issues)} issues detected: stopping import."
                    )

                self.stdout.write(
                    self.style.SUCCESS(f"Successfully imported {num_people} people.")
                )
