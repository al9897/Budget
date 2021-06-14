from django.contrib import admin
from budget_backend.models import User, Stock, StockScreener
from .models import WatchList, Portfolio

admin.site.register(Stock)
admin.site.register(StockScreener)
admin.site.register(Portfolio)
admin.site.register(WatchList)


#from .models import Stock, StockPrice, WatchList, Portfolio
#from budget_backend.models import User

""" # Register your models here.
admin.site.register(User)

admin.site.register(Stock)
admin.site.register(StockPrice)
admin.site.register(WatchList)
admin.site.register(Portfolio) """
