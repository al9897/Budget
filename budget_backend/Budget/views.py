import json
from django.forms.models import model_to_dict

from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse, Http404
import random
import datetime
from budget_backend.models import User
from .models import SavingGoal
from .models import Transaction
from .models import Category
from .models import Income
from .serializers import UserSerializer
from .serializers import SavingSerializer
from .serializers import TransactionSerializer
from .serializers import CategorySerializer
from .serializers import IncomeSerializer, IncomeBySourceSerializer
from .serializers import *
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework import mixins
from django.core import serializers
from django.db.models import Avg, Count, Min, Sum
from django.db.models.functions import Coalesce


def UserTransactions(request, id):
    # id : userid
    if request.method == "GET":
        try:
            user = User.objects.get(id=id)
            transactions = Transaction.objects.filter(userId=user)
            data = []
            if len(transactions) == 0:
                return HttpResponse("No transactions", status=200)
            for tran in transactions:
                _tran = model_to_dict(tran)
                _category = model_to_dict(tran.categoryId)
                _tran['categoryId'] = _category
                data.append(_tran)
            return JsonResponse(data, safe=False)
        except Exception as E:
            print(E)
            return HttpResponse("user doesn't exist", status=404)


def UserIncomes(request, id):
    # id : userid
    if request.method == "GET":
        try:
            user = User.objects.get(id=id)
            incomes = Income.objects.filter(userId=user)
            data = []
            if len(incomes) == 0:
                return HttpResponse("No incomes", status=200)
            for i in incomes:
                _income = model_to_dict(i)
                data.append(_income)
            return JsonResponse(data, safe=False)
        except Exception as E:
            print(E)
            return HttpResponse("user doesn't exist", status=404)


def UserSavingGoal(request, id):
    # id : userid
    if request.method == "GET":
        try:
            user = User.objects.get(id=id)
            goals = SavingGoal.objects.filter(userId=user)
            data = []
            if len(goals) == 0:
                return HttpResponse("No goals", status=200)
            for i in goals:
                _goal = model_to_dict(i)
                data.append(_goal)
            return JsonResponse(data, safe=False)
        except Exception as E:
            print(E)
            return HttpResponse("user doesn't exist", status=404)


def UserBudgetGoal(request, id):
    # id : userid
    if request.method == "GET":
        try:
            user = User.objects.get(id=id)
            goals = BudgetGoal.objects.filter(userId=user)
            data = []
            if len(goals) == 0:
                return HttpResponse("No goals", status=200)
            for i in goals:
                _goal = model_to_dict(i)
                data.append(_goal)
            return JsonResponse(data, safe=False)
        except Exception as E:
            print(E)
            return HttpResponse("user doesn't exist", status=404)


def UserSumIncome(request, id):
    if request.method == "GET":
        try:
            print("TEST 1")
            user=User.objects.get(id=id)
            print("TESt")
            incomes = Income.objects.filter(userId=user)
            data = []
        # incomes = Income.objects.all().filter(userId=user).only('source').annotate(
        #     total_income_per_source=Sum('amount')).order_by('source')
        # for income in incomes:
        #     _income = model_to_dict(income)
        #     data.append(_income)
        # data['User'] = model_to_dict(user)
            sources = []
            _amount = 0
            for i in incomes:
                if i.source not in sources:
                    sources.append(i.source)

            for i in sources:
                _amount = 0
                tmp = Income(source=i)
                for j in incomes:
                    if j.source == i:
                        _amount += j.amount
                tmp.amount = _amount
                _tmp = model_to_dict(tmp)
                data.append(_tmp)
            return JsonResponse(data, safe=False)
        except Exception as E:
            return HttpResponse("user doesn't exist", status=404)


def index(request):
    return HttpResponse("Hello, from budget APP")


expens = [
    'AH',
    'JUMBO',
    'ATM',
    'Gas Station',
    'MediaMarks.nl',
    'Bol.com',
    'Amazon.com',
    'ATM Exchange',
    'Coinbase',
    'Transfer',
    'Trading.com',
    'Tikkie',
    'Unknown'
]

categories = [
    'Food & Drink',
    'Transportation',
    'Shopping',
    'Stock',
    'Electronices',
    'Groceries'
]


# Category


class CategoryList(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()

    # permission_classes = [IsAuthenticated]

    def get(self, request, *arg, **kwargs):
        return self.list(request, *arg, **kwargs)

    def post(self, request, *arg, **kwargs):
        return self.create(request, *arg, **kwargs)


class CategoryDetail(mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.DestroyModelMixin,
                     generics.GenericAPIView):
    """
    Retrieve, update or delete a code snippet.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


# Transaction
class TransactionList(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    serializer_class = TransactionSerializer
    queryset = Transaction.objects.all()

    # permission_classes = [IsAuthenticated]

    def get(self, request, *arg, **kwargs):
        return self.list(self, request, *arg, **kwargs)

    def post(self, request, *arg, **kwargs):
        return self.create(request, *arg, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)


class TransactionDetail(mixins.RetrieveModelMixin,
                        mixins.UpdateModelMixin,
                        mixins.DestroyModelMixin,
                        generics.GenericAPIView):
    """
    Retrieve, update or delete a code snippet.
    """
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


def trans(request):
    data = []
    count = 10

    for x in range(0, count):
        amount = random.randint(5, 125)
        start_date = datetime.date.today()
        end_date = datetime.date(2022, 1, 1)

        time_between_dates = end_date - start_date
        days_between_dates = time_between_dates.days
        random_number_of_days = random.randrange(days_between_dates)
        random_date = start_date + datetime.timedelta(days=random_number_of_days)

        choice = random.choice(expens)
        choice1 = random.choice(categories)

        one = {
            'amount': "-" + str(amount),
            'date': start_date,
            'to': choice,
            'category': choice1
        }

        data.append(one)

    return JsonResponse(data, safe=False, json_dumps_params={'indent': 2})


def welcome(request):
    return HttpResponse("Hello, 2 welcome")


# Saving goal
class SavingGoalList(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    # permission_classes = [IsAuthenticated]

    def get(self, request, *arg, **kwargs):
        return self.list(request, *arg, **kwargs)

    def post(self, request, *arg, **kwargs):
        return self.create(request, *arg, **kwargs)


class SavingGoalDetail(mixins.RetrieveModelMixin,
                       mixins.UpdateModelMixin,
                       mixins.DestroyModelMixin,
                       generics.GenericAPIView):
    """
    Retrieve, update or delete a code snippet.
    """
    queryset = SavingGoal.objects.all()
    serializer_class = SavingSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    def post(self, request, *arg, **kwargs):
        return self.create(request, *arg, **kwargs)


# User
class UserList(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    # permission_classes = [IsAuthenticated]

    def get(self, request, *arg, **kwargs):
        return self.list(request, *arg, **kwargs)

    def post(self, request, *arg, **kwargs):
        return self.create(request, *arg, **kwargs)


class UserDetail(mixins.RetrieveModelMixin,
                 mixins.UpdateModelMixin,
                 mixins.DestroyModelMixin,
                 generics.GenericAPIView):
    """
    Retrieve, update or delete a code snippet.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


# Income
class IncomeList(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    serializer_class = IncomeSerializer
    queryset = Income.objects.all()

    def get(self, request, *arg, **kwargs):
        return self.list(request, *arg, **kwargs)

    def post(self, request, *arg, **kwargs):
        return self.create(request, *arg, **kwargs)


class BudgetGoalCategoryList(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    serializer_class = BudgetGoalCategorySerializer
    queryset = BudgetGoalCategory.objects.all()

    # permission_classes = [IsAuthenticated]

    def get(self, request, *arg, **kwargs):
        return self.list(request, *arg, **kwargs)

    def post(self, request, *arg, **kwargs):
        return self.create(request, *arg, **kwargs)


class IncomeDetail(mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.DestroyModelMixin,
                   generics.GenericAPIView):
    """
    Retrieve, update or delete a code snippet.
    """
    queryset = Income.objects.all()
    serializer_class = IncomeSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class BudgetGoalCategoryDetail(mixins.RetrieveModelMixin,
                               mixins.UpdateModelMixin,
                               mixins.DestroyModelMixin,
                               generics.GenericAPIView):
    """
    Retrieve, update or delete a code snippet.
    """
    queryset = BudgetGoalCategory.objects.all()
    serializer_class = BudgetGoalCategorySerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


# Group income by source
class IncomeListBySource(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    serializer_class = IncomeBySourceSerializer
    queryset = (
        Income.objects.all().values('source').annotate(total_income_per_source=Sum('amount')).order_by('source'))

    def get(self, request, *arg, **kwargs):
        return self.list(request, *arg, **kwargs)


class BudgetGoalList(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    serializer_class = BudgetGoalSerializer
    queryset = BudgetGoal.objects.all()

    # permission_classes = [IsAuthenticated]

    def get(self, request, *arg, **kwargs):
        return self.list(request, *arg, **kwargs)

    def post(self, request, *arg, **kwargs):
        return self.create(request, *arg, **kwargs)


class BudgetGoalDetail(mixins.RetrieveModelMixin,
                       mixins.UpdateModelMixin,
                       mixins.DestroyModelMixin,
                       generics.GenericAPIView):
    """
    Retrieve, update or delete a code snippet.
    """
    queryset = BudgetGoal.objects.all()
    serializer_class = BudgetGoalSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


# Saving Goal
class SavingGoalList(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    serializer_class = SavingGoalSerializer
    queryset = SavingGoal.objects.all()

    # permission_classes = [IsAuthenticated]

    def get(self, request, *arg, **kwargs):
        return self.list(request, *arg, **kwargs)

    def post(self, request, *arg, **kwargs):
        return self.create(request, *arg, **kwargs)


class SavingGoalDetail(mixins.RetrieveModelMixin,
                       mixins.UpdateModelMixin,
                       mixins.DestroyModelMixin,
                       generics.GenericAPIView):
    """
    Retrieve, update or delete a code snippet.
    """
    queryset = SavingGoal.objects.all()
    serializer_class = SavingGoalSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
