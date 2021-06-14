from django.core.management.base import BaseCommand, CommandError
import pytz
from budget_backend.models import Stock, StockLogs, StockScreener
from ._priceGenerator import get_new_value
from datetime  import date
from django.utils import timezone
import pytz
import time
  
timezone = pytz.timezone('Europe/Amsterdam')


class Command(BaseCommand):
    
    help = 'Command to save records to logs and clean up the screener'

    def handle(self, *args, **options):
        try:
            for x in Log():
                self.stdout.write(self.style.SUCCESS(f'LOG {x.id}'))
            
        except Exception as E:
            print(E)
                
                
def Log():
    stocks = Stock.objects.all()
    for stock in stocks:
        logs = StockScreener.objects.filter(stock_id=stock, date_time=date.today())
        return logs

            




    