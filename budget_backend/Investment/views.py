from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
from django.core import serializers
from .models import Buy, WatchList, Portfolio, Order
from budget_backend.models import User, Stock, StockScreener
import json
from django.utils import timezone


def index(request):
    return HttpResponse("Hello, from INVESTMENT APP")


def welcome(request):
    return HttpResponse("Hello, 2 welcome")


def get_stocks(request):
    if request.method == 'GET':
        stocks = Stock.objects.all()
        data_list = []
        for stock in stocks:
            open_price = \
                StockScreener.objects.filter(
                    stock_id=stock,
                    date_time__date=timezone.localtime(timezone.now()).date()) \
                .earliest('date_time').price
            tmp = {
                'id': stock.id,
                'stock_name': stock.name,
                'abbreviation': stock.abbreviation,
                'current_price': stock.current_price,
                'open_price': open_price
            }
            data_list.append(tmp)

        return JsonResponse(data_list, safe=False)


def get_stock(request):
    if request.method == 'GET':
        stock_id = request.GET.get('stock_id', None)

        stock = Stock.objects.get(id=stock_id)
        open_price = \
            StockScreener.objects.filter(
                stock_id=stock_id,
                date_time__date=timezone.localtime(timezone.now()).date()) \
            .earliest('date_time').price

        data = {
            'id': stock.id,
            'stock_name': stock.name,
            'abbreviation': stock.abbreviation,
            'current_price': stock.current_price,
            'open_price': open_price
        }

        return JsonResponse(data)


def get_stock_price(request):
    if request.method == 'GET':
        stock_id = request.GET.get('stock_id', None)

        day_price = \
            StockScreener.objects.filter(
                stock_id=stock_id,
                date_time__date=timezone.localtime(timezone.now()).date())

        stock_prices = day_price.values(
            'price', 'date_time').order_by('date_time')
        stock_prices = list(stock_prices)

        return JsonResponse(stock_prices, safe=False)


def get_watchlist(request):
    # try:
    if request.method == 'GET':
        body = json.loads(request.body)

        user_id = body['user_id']
        user = User.objects.get(id=user_id)
        data = WatchList.objects.filter(user_id=user)

        data_list = []
        for x in data:
            today_prices = StockScreener.objects.filter(
                stock_id=x.stock_id, date_time__date=timezone.localtime(timezone.now()).date())

            tmp = {
                "id": x.stock_id.id,
                "stock_name": x.stock_id.name,
                "abbreviation": x.stock_id.abbreviation,
                "current_price": x.stock_id.current_price,
                "open_price": today_prices.earliest('date_time').price
            }
            data_list.append(tmp)

        final_data = json.dumps(data_list, sort_keys=False, indent=4)
        return HttpResponse(final_data)


def add2watchlist(request):
    try:
        if request.method == 'POST':
            user_id = request.GET.get('user_id', None)
            stock_id = request.GET.get('stock_id', None)

            user = User.objects.get(id=user_id)
            stock = Stock.objects.get(id=stock_id)

            tmp = WatchList(user_id=user, stock_id=stock)
            tmp.save()

            return HttpResponse("WORKED")
        else:
            return HttpResponse("REQUEST FAILED")
    except Exception as E:
        return HttpResponse(E, status=409)


def get_portfolio(request):
    if request.method == 'GET':
        body = json.loads(request.body)

        user_id = body['user_id']
        user = User.objects.get(id=user_id)
        portfolio = Portfolio_process(user)
        return HttpResponse(portfolio)

    return HttpResponse("Works")


def place_order(request):
    if request.method == 'POST':
        user_id = request.GET.get('user_id', None)

        body = json.loads(request.body)
        stock_id = body['stock_id']
        quantity = int(body['quantity'])
        price = float(body['price'])
        order_type = body['order_type']

        user = User.objects.get(id=user_id)
        stock = Stock.objects.get(id=stock_id)

        if order_type == 'BUY' and price * quantity > user.balance:
            return HttpResponseBadRequest("not sufficient balance")

        order = Order(user_id=user, stock_id=stock,
                      quantity=quantity, price=price, order_type=order_type)
        order.save()

        return HttpResponse("Buy order placed")


def cancel_order(request):
    if request.method == 'DELETE':
        user_id = request.GET.get('user_id', None)

        body = json.loads(request.body)
        order_id = body['order_id']

        order = None

        try:
            order = Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            order = None

        if order is not None:
            order.delete()

        return HttpResponse("order canceled")


def get_orders(request):
    if request.method == 'GET':
        user_id = request.GET.get('user_id', None)

        orders = Order.objects.filter(user_id=user_id)

        data = []

        for o in orders:
            data.append({
                'id': o.id,
                'stock_id': o.stock_id.id,
                'stock_name': o.stock_id.name,
                'abbreviation': o.stock_id.abbreviation,
                'quantity': o.quantity,
                'price': o.price,
                'order_type': o.order_type
            })

        data = json.dumps(data)

        return HttpResponse(data, content_type="application/json")


def get_balance(request):
    if request.method == 'GET':
        user_id = request.GET.get('user_id', None)

        user = User.objects.get(id=user_id)
        return JsonResponse(user.balance, safe=False)


def deposit(request):
    if request.method == 'PUT':
        user_id = request.GET.get('user_id', None)

        body = json.loads(request.body)
        balance = float(body['balance'])

        user = User.objects.get(id=user_id)
        user.balance += balance
        user.save()

        return HttpResponse("Success")

# Utils


def Buy_process(user, stock, quantity):
    current = Buy(user_id=user, stock_id=stock, quantity=quantity,
                  price_bought=stock.current_price)
    current.save()
    return True


def Portfolio_process(user):
    portfolio = Portfolio.objects.filter(user_id=user)
    data_list = []

    for investment in portfolio:
        stock = Stock.objects.get(id=investment.stock_id.id)
        data = {
            "stock_id": investment.stock_id.id,
            "stock_name": stock.name,
            "abbreviation": stock.abbreviation,
            "stock_price": stock.current_price,
            "quantity": investment.quantity,
            "average_price": investment.average_price
        }
        data_list.append(data)

    return json.dumps(data_list, sort_keys=False, indent=4)
