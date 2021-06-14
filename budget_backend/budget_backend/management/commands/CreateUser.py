from django.core.management.base import BaseCommand, CommandError
from budget_backend.models import * 
# importing datetime module
import datetime
  
# creating an instance of 
# datetime.date



class Command(BaseCommand):
    help = 'Closes the specified poll for voting'



    def handle(self, *args, **options):
        try:
            d = datetime.date(1997, 10, 19)
            first_user = User(
                full_name="youssef",
                balance=20.0,
                username="youssef",
                password="password",
                dob = d,
                email = "youssef@gmail",
                phone = "+316000",
                adress = "NL",
                zipcode = "TEST123",
                country = "NETHERLANDS",
                currency = "EU",
                iban = "TEST"
            )
            first_user.save()
            self.stdout.write(self.style.SUCCESS(f'Successfully Created user with id {first_user.id}'))
        except Exception as E:
            self.stdout.write(self.style.ERROR(f'User not created: {E}'))
