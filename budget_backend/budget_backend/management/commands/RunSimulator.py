from django.core.management.base import BaseCommand, CommandError
import pytz
from budget_backend.models import Stock, StockScreener, User
from Investment.models import Order, Portfolio
from ._priceGenerator import get_new_value
from datetime  import datetime
from django.utils import timezone
import pytz
import time
  
#timezone = pytz.timezone('Europe/Amsterdam')


class Command(BaseCommand):
    
    help = 'Crontab script to change price 5 seconds '

    def handle(self, *args, **options):
        try:
            Run()
        except Exception as E:
            print(E)
                
            



def Run():
    stocks = Stock.objects.all()
    for stock in stocks:
        # get new price
        new_price = get_new_value(stock.current_price)
        
        #Log and save the change
        tmp = StockScreener(stock_id=stock, price=new_price, date_time=timezone.localtime(timezone.now()))
        tmp.save()
        
        # Update the stock price
        stock.current_price = new_price
        stock.save()

def Matcher():
    orders = Order.objects.all()
    
    for o in orders:
        if(o.order_type == 'BUY'):
            process_buy(o)
        else:
            process_sell(o)



def process_buy(order):
    if order.price >= order.stock_id.current_price:
        portfolio = None
        
        try:
            portfolio = Portfolio.objects.get(
                user_id=order.user_id, stock_id=order.stock_id)
        except Portfolio.DoesNotExist:
            portfolio = None

        if portfolio is None:
            portfolio = Portfolio(
                user_id=order.user_id, 
                stock_id=order.stock_id, 
                quantity=order.quantity,
                average_price=order.price)
            portfolio.save()
        else:
            new_total_price = \
                portfolio.quantity * portfolio.average_price + \
                order.price * order.quantity

            portfolio.quantity += order.quantity
            portfolio.average_price = new_total_price / portfolio.quantity
            portfolio.save()
        
        user = User.objects.get(id=order.user_id.id)
        user.balance -= order.price * order.quantity
        
        user.save()
        order.delete()

def process_sell(order):
    if order.price <= order.stock_id.current_price:
        portfolio = None
        
        try:
            portfolio = Portfolio.objects.get(
                user_id=order.user_id, stock_id=order.stock_id)
        except Portfolio.DoesNotExist:
            portfolio = None
            
        if portfolio is None:
            raise Exception("gg")
        else:
            portfolio.quantity -= order.quantity
            portfolio.save()
        
        user = User.objects.get(id=order.user_id.id)
        user.balance += order.price * order.quantity
        
        user.save()
        order.delete()