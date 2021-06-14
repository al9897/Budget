from django.core.management.base import BaseCommand, CommandError
import pytz
from budget_backend.models import Stock, StockScreener
from ._priceGenerator import get_new_value
from datetime  import datetime, tzinfo
from django.utils import timezone
import pytz
import time
  
timezone = pytz.timezone('Europe/Amsterdam')


class Command(BaseCommand):
    help = 'Generate new price for stock x times'

    def add_arguments(self , parser):
         parser.add_argument('--times', type=int, help="How many times to generate price")

    def handle(self, *args, **options):
        
        times = 0
        if options['times']:
            times = options['times']
             
        try:
            stock = Stock.objects.get(id=1)
            self.stdout.write(f"Current price {stock.current_price}")
            self.stdout.write("New price")
            
            for _ in range(times):
                new_price = get_new_value(stock.current_price)
                tmp = StockScreener(stock_id=stock, price=new_price, date_time=datetime.now(timezone))
                tmp.save()
                self.stdout.write(self.style.SUCCESS(f'{new_price}'))
                time.sleep(1) #testing 
                
        except Exception as E:
            self.stdout.write(self.style.ERROR('Could not get new price'))
            self.stdout.write(self.style.ERROR(f'{E}'))

