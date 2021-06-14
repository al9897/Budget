#
# This is not a django command, file name starting by "_" is ignored 
#


from django.core.management.base import BaseCommand, CommandError
from budget_backend.models import * 
import time
from random import gauss, seed
from math import sqrt, exp

def create_GBM(s0, mu, sigma):
    """
    Generates a price following a geometric brownian motion process based on the input of the arguments:
    - s0: Asset inital price.
    - mu: Interest rate expressed annual terms.
    - sigma: Volatility expressed annual terms. 
    """
    st = s0
    st *= exp((mu - 0.5 * sigma ** 2) * (1. / 365.) + sigma * sqrt(1./365.) * gauss(mu=0, sigma=1))
    return st

def get_new_value(current_price):
    
    # Some randomness
    seed(time.time())
    
    gbm = create_GBM(current_price, 0.1, 0.05)
    return gbm




