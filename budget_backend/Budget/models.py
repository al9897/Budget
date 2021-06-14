import datetime

import django
from django.db import models
from django.core.validators import EmailValidator, MinValueValidator
from django.utils.timezone import now
from budget_backend.models import User


# Create your models here.


class Income(models.Model):
    userId = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField("Amount of money", max_digits=15, decimal_places=2,
                                 validators=[MinValueValidator(0, "Budget goal amount must be > 0")])
    source = models.CharField("Money source", max_length=30, blank=True)
    date = models.DateTimeField("Date", default=now)

    def __str__(self):
        return '{} {} {} {}'.format(self.userId, self.amount, self.source, self.date)


class Category(models.Model):
    categoryId = models.AutoField("Category ID", primary_key=True, serialize=True, unique=True)
    categoryName = models.CharField("Name of the category", max_length=30, unique=True, default="Other")

    def __str__(self):
        return '{}'.format(self.categoryName)


class Transaction(models.Model):
    userId = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="User")
    amount = models.DecimalField("Amount of money in the transaction", max_digits=15, decimal_places=2, default=0,
                                 validators=[MinValueValidator(0, "Transaction amount must be >= 0.")])
    time = models.DateTimeField("Time on the transaction", null=True)
    categoryId = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Category",
                                   related_name='transactions', null=True)
    note = models.CharField("Note", max_length=150, blank=True)

    def __str__(self):
        return '{} {} {} {} {}'.format(self.userId, self.amount, self.time, self.categoryId, self.note)


class BudgetGoal(models.Model):
    userId = models.ForeignKey(User, on_delete=models.CASCADE)
    cycleTimeStart = models.DateTimeField("Start date", blank=False)
    cycleTimeEnd = models.DateTimeField("End date", blank=False)

    def __str__(self):
        return '{} {} {}'.format(self.id, self.cycleTimeStart, self.cycleTimeEnd)


class SavingGoal(models.Model):
    userId = models.ForeignKey(User, on_delete=models.CASCADE)
    goalAmount = models.DecimalField("Amount of money user want to save", max_digits=15, decimal_places=2, default=0,
                                     validators=[MinValueValidator(0, "Saving goal amount must be > 0")])
    currentAmount = models.DecimalField("Current amount", max_digits=15, decimal_places=2, default=0,
                                        validators=[MinValueValidator(0, "Current amount must be > 0")])
    duration = models.IntegerField("Duration of the goal (days)", default=0,
                                   validators=[MinValueValidator(0, "Saving goal duration must be > 1 day")])
    startDate = models.DateTimeField("Start Date", blank=True, default=now)
    endDate = models.DateTimeField("End Date", blank=True, default=now)
    isComplete = models.BooleanField(default=False)

    def __str__(self):
        return '{} {} {} {}'.format(self.userId, self.amount, self.duration, self.startDate)

    def save(self, *args, **kwargs):
        if not self.pk and SavingGoal.objects.exists():
            # if you'll not check for self.pk
            # then error will also raised in update of exists model
            raise ValidationError('There is can be only one Saving Goal instance')
        return super(SavingGoal, self).save(*args, **kwargs)


class BudgetGoalCategory(models.Model):
    budgetGoalid = models.ForeignKey(BudgetGoal, on_delete=models.CASCADE)
    categoryId = models.ForeignKey(Category, on_delete=models.CASCADE)
    amount = models.DecimalField("Amount of money", max_digits=15, decimal_places=2, default=0,
                                 validators=[MinValueValidator(0, "Budget goal amount must be > 0")])

    class Meta:
        unique_together = ('budgetGoalid', 'categoryId',)
