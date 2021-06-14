from django.test import TestCase
from .models import WatchList, Buy
from budget_backend.models import User, Stock

import datetime


class InvestmentTests(TestCase):
 
    def setUp(self):
        # Some object for test cases 
        d = datetime.date(1997, 10, 19)
        test_user = User(
                full_name="testyousser",    
                username="testuser",
                password="testpassword",
                dob = d,
                email = "test@gmail",
                phone = "+31604500",
                adress = "NL",
                zipcode = "TEST123",
                country = "NETHERLANDS",
                currency = "EU",
                iban = "TEST"
            )
        test_user.save()
        test_stock = Stock(            
                name = "BTCTEST",
                abbreviation = "TEST",
                current_price = "1000",
                frequency = 5
        )
        test_stock.save()

        
        
    def testAddToWatchList(self):
        #test adding to watchlist
        user = User.objects.get(username="testuser")
        stock = Stock.objects.get(name="BTCTEST")
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(stock.name, 'BTCTEST')
    
    #buy stock 