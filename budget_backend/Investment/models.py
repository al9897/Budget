from django.db import models
from budget_backend.models import User, Stock 




class WatchList(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, null=False, on_delete=models.CASCADE)
    stock_id = models.ForeignKey(Stock, null=False, on_delete=models.CASCADE)
    class Meta:
       unique_together = ("stock_id", "user_id")


#model to save bought stock
class Buy(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, null=False, on_delete=models.CASCADE)
    stock_id = models.ForeignKey(Stock, null=False, on_delete=models.CASCADE)
    quantity = models.IntegerField(null=False)
    price_bought = models.FloatField(null=True)
  # git s date = models.DateField(null=False, default=)
    
"""     

"When we open a SELL position, it means we sell to the Market. Therefore, when we close the position, we must BUY it back from the Market."
https://www.etoro.com/news-and-analysis/trading/trading-basics-buy-and-sell-explained/

Model to save sold stock

Note: at the moment not implemented
"""

class Sell(models.Model):
    
    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, null=False, on_delete=models.CASCADE)
    stock_id = models.ForeignKey(Stock, null=False, on_delete=models.CASCADE)
    quantity = models.IntegerField(null=False)
    price = models.FloatField(null=False)

class Order(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, null=False, on_delete=models.CASCADE)
    stock_id = models.ForeignKey(Stock, null=False, on_delete=models.CASCADE)
    quantity = models.IntegerField(null=False)
    price = models.FloatField(null=False)
    order_type = models.CharField(max_length=30, choices=[('SELL','SELL'), ('BUY', 'BUY')], default='BUY')
    
class Portfolio(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, null=False, on_delete=models.CASCADE)
    stock_id = models.ForeignKey(Stock, null=False, on_delete=models.CASCADE)
    quantity = models.IntegerField(null=False)
    average_price = models.FloatField(null=True)