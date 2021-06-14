from datetime import date, datetime
from django.utils import timezone
from rest_framework import serializers
from .models import User
from .models import SavingGoal
from .models import Transaction
from .models import Category
from .models import Income
from .models import BudgetGoal, BudgetGoalCategory


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class SavingSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavingGoal
        fields = ('amount', 'duration')


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'

    def to_representation(self, instance):
        self.fields['categoryId'] = CategorySerializer(read_only=True)
        return super(TransactionSerializer, self).to_representation(instance)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class IncomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Income
        fields = '__all__'


class IncomeBySourceSerializer(serializers.ModelSerializer):
    total_income_per_source = serializers.DecimalField(max_digits=15, decimal_places=2)

    class Meta:
        model = Income
        fields = ('source', 'total_income_per_source')


class BudgetGoalCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = BudgetGoalCategory
        fields = '__all__'

    def to_representation(self, instance):
        self.fields['categoryId'] = CategorySerializer(read_only=True)
        return super(BudgetGoalCategorySerializer, self).to_representation(instance)


class BudgetGoalSerializer(serializers.ModelSerializer):
    class Meta:
        model = BudgetGoal
        fields = '__all__'

    def validate(self, data):
        """
        Check that the start is before the stop.
        """
        today = timezone.localtime(timezone.now())
        if (data['cycleTimeStart'] >= data['cycleTimeEnd']):
            raise serializers.ValidationError("finish must occur after start")
        if (today >= data['cycleTimeEnd']):
            raise serializers.ValidationError("Budget goal end date must be after today")
        return data


class SavingGoalSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavingGoal
        fields = '__all__'



