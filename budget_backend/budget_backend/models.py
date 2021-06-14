from django.db import models


class User(models.Model):
    id = models.AutoField(primary_key=True)
    balance = models.FloatField(default=0.00)
    full_name = models.CharField(max_length=30, null=False)
    dob = models.DateField(max_length=8, null=False)
    username = models.CharField(max_length=30, null=False, unique=True)
    password = models.CharField(max_length=30, null=False, default="password")
    email = models.CharField(max_length=30, null=False)
    phone = models.CharField(max_length=30, null=False)
    adress = models.CharField(max_length=30, null=False)
    zipcode = models.CharField(max_length=8, null=False)
    country = models.CharField(max_length=20, null=False)
    currency = models.CharField(max_length=2, null=False)
    iban = models.CharField(max_length=34, null=False)


class Auth(models.Model):
    token = models.CharField(max_length=32, primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    expiry_date = models.DateTimeField(null=False, unique=False)
    
    
class Stock(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30, null=False)
    abbreviation = models.CharField(max_length=8, null=False)
    current_price = models.FloatField(null=False)
    frequency = models.IntegerField(default=5, null=False) # how often to change price
    
    
class StockScreener(models.Model):
    id = models.AutoField(primary_key=True)
    stock_id = models.ForeignKey(Stock, null=False, on_delete=models.CASCADE)
    price = models.FloatField(null=False)
    date_time = models.DateTimeField(null=False, unique=True)
    
    
#Store each stock price per day
class StockLogs(models.Model):
    id = models.AutoField(primary_key=True)
    stock_id = models.ForeignKey(Stock, null=False, on_delete=models.CASCADE)
    date = models.DateField(null=False, unique=True)
    avg = models.FloatField(null=False)
    max = models.FloatField(null=False)
    mix = models.FloatField(null=False)
    
