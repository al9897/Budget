from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('welcome', views.welcome, name='welcome'),
    path('portfolio', views.get_portfolio, name='portfolio'),
    path('getstocks', views.get_stocks, name='getstocks'),
    path('watchlist', views.get_watchlist, name='watchlist'),
    path('add2watchlist', views.add2watchlist, name='addtowatchlist'),
    path('stock', views.get_stock, name='stock'),
    path('stocks', views.get_stocks, name='stocks'),
    path('stockprice', views.get_stock_price, name='stockprice'),
    path('balance', views.get_balance, name='balance'),
    path('deposit', views.deposit, name='deposit'),
    path('orders', views.get_orders, name='orders'),
    path('placeorder', views.place_order, name='placeorder'),
    path('cancelorder', views.cancel_order, name='cancelorder')
]
