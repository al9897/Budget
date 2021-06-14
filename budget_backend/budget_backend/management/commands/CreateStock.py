from django.core.management.base import BaseCommand, CommandError
from budget_backend.models import Stock
import datetime
  



class Command(BaseCommand):
    
    help = 'Create a new stock with default values'

    def handle(self, *args, **options):
        try:
            new_Stock = Create()
            self.stdout.write(self.style.SUCCESS(f'Successfully Created Stock with id {new_Stock.id}'))
        except Exception as E:
            self.stdout.write(self.style.ERROR(f'Stock not created \n {E}'))
            
            

def Create():
    new_Stock = Stock(            
        name = "BITCOIN",
        abbreviation = "BTC",
        current_price = "100",
        frequency = 5
    )
    new_Stock.save()
    return new_Stock
    