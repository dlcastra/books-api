from django.core.management.base import BaseCommand
from faker import Faker

from books.models import Author

fake = Faker()


class Command(BaseCommand):
    help = "Add the specified number of teachers to the database"

    def add_arguments(self, parser):
        parser.add_argument("number", type=int, nargs="?", default=100)

    def handle(self, *args, **options):
        number = options["number"]
        if number < 1:
            self.stdout.write(
                self.style.ERROR("The number to be generated must be greater than 0")
            )

        for i in range(number):
            author = Author.objects.create(
                name=fake.first_name(),
                surname=fake.last_name(),
                birth_date=fake.date(),
            )

            self.stdout.write(
                self.style.SUCCESS(
                    "The teacher has been successfully added to the database, his id: '%s'"
                    % author
                )
            )
