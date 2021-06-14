from django.contrib import admin
from budget_backend.models import User
from .models import Follow
from .models import Comment
from .models import Plan
from .models import ParentChildComment
from .models import PlanComment

# admin.site.register(User)
admin.site.register(Follow)
admin.site.register(Comment)
admin.site.register(Plan)
admin.site.register(ParentChildComment)
admin.site.register(PlanComment)
# Register your models here.
