from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Transaction)
admin.site.register(Category)
admin.site.register(SavingGoal)
admin.site.register(BudgetGoal)
admin.site.register(BudgetGoalCategory)
admin.site.register(Income)