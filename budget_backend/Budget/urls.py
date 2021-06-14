from django.urls import path, include

from . import views
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('', views.index, name='index'),
    # path(r'trans', views.trans, name='trans'),
    # transaction
    path(r'transactions/user/<int:id>', views.UserTransactions, name='UserTransactions'),
    path(r'transactions', views.TransactionList.as_view(), name='transactions'),
    path(r'transactions/edit/<int:pk>', views.TransactionDetail.as_view(), name='Edit Transaction'),
    # category
    path(r'categories', views.CategoryList.as_view(), name='GET/POST Categories'),
    path(r'categories/edit/<str:pk>', views.CategoryDetail.as_view(), name='Edit Categories'),
    # Income
    path(r'income/user/<int:id>', views.UserIncomes, name='UserIncome'),
    path(r'income', views.IncomeList.as_view(), name='GET/POST Income'),
    path(r'income/edit/<str:pk>', views.IncomeDetail.as_view(), name='Edit Income'),
    path(r'income/incomebysource', views.IncomeListBySource.as_view(), name='Group Income By Source'),
    path(r'income/incomebysource/user/<int:id>', views.UserSumIncome, name='Group Income By Source'),
    # Budget goal
    path(r'budgetgoal/user/<int:id>', views.UserBudgetGoal, name='BudgetGoal'),
    path(r'budgetgoal', views.BudgetGoalList.as_view(), name='GET/POST Budget Goal'),
    path(r'budgetgoal/edit/<int:pk>', views.BudgetGoalDetail.as_view(), name='Edit Categories'),
    path(r'budgetgoalcategories', views.BudgetGoalCategoryList.as_view(), name='GET/POST Categories'),
    path(r'budgetgoalcategories/edit/<int:pk>', views.BudgetGoalCategoryDetail.as_view(), name='Edit Categories'),
    # Saving goal
    path(r'savinggoal/user/<int:id>', views.UserSavingGoal, name='UserTransactions'),
    path(r'savinggoal', views.SavingGoalList.as_view(), name='GET/POST Saving Goal'),
    path(r'savinggoal/edit/<int:pk>', views.SavingGoalDetail.as_view(), name='Edit Saving Goal'),
    # path(r'welcome', views.welcome, name='welcome'),
    path('api-auth/', include('rest_framework.urls')),
]
