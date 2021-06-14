from django.core.management.base import BaseCommand, CommandError
from budget_backend.models import Stock
import datetime


class Command(BaseCommand):
    help = 'Create a new stock with default values'

    list_stocks = [
        Stock(name="GameStop", abbreviation="GME", current_price=110),
        Stock(name="Tesla", abbreviation="TSLA", current_price=700),
        Stock(name="Advanced Micro Devices", abbreviation="AMD", current_price=77.44),
        Stock(name="Royal Dutch Shell", abbreviation="RDSA", current_price=16.49),
        Stock(name="Palantir Technologies", abbreviation="PLTR", current_price=21.23),
        Stock(name="AMC Entertainment", abbreviation="AMC", current_price=13.68),
        Stock(name="Apple ", abbreviation="AAPL", current_price=127.10),
        Stock(name="Microsoft", abbreviation="MSFT", current_price=250.78),
        Stock(name="Amazon", abbreviation="AMZN", current_price=3245),
        Stock(name="Alphabet (Google)", abbreviation="GOOG", current_price=2407),
        Stock(name="Facebook", abbreviation="FB", current_price=324.63),
        Stock(name="Tencent", abbreviation="TCEHY", current_price=75.74),
    ]

    def handle(self, *args, **options):
        try:
            populated_stocks = Create(self.list_stocks)
            self.stdout.write(self.style.SUCCESS(
                f'Successfully Created Stock with id {len(populated_stocks)}'))
        except Exception as E:
            self.stdout.write(self.style.ERROR(f'Stock not created \n {E}'))


def Create(list_stocks):
    population = []

    for stock in list_stocks:
        stock.save()
        population.append(stock)


    return population
