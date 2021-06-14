from django.db import models
from datetime import datetime, date
from budget_backend.models import User

# Create your models here.

#class User(models.Model):
#    userId = models.CharField("User Id", primary_key=True, unique=True,
#                              null=False, max_length=30)
#    first_name = models.CharField("User's first name", max_length=30)
#    last_name = models.CharField("User's last name", max_length=30)
#    email = models.CharField("User's email", max_length=30, unique=True)
#    password = models.CharField("User's password", max_length=30)
#    profile_pic = models.ImageField("Profile picture", null=True)

#    def __str__(self):
#        return '{} {} {}'.format(self.first_name, self.last_name, self.email)

class Follow(models.Model):
    followed_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="%(app_label)s_%(class)s_related")
    following_user = models.ForeignKey(User, on_delete=models.CASCADE)

class Comment(models.Model):
    comment_id = models.CharField(primary_key=True, unique=True, null=False, max_length=30)
    commenter = models.ForeignKey(User, on_delete=models.CASCADE, related_name="%(app_label)s_%(class)s_related")
    content = models.CharField(max_length=300)
    point = models.IntegerField(default=0)
    post_date = models.DateField(default=date.today)

class Plan(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="%(app_label)s_%(class)s_related")
    point = models.IntegerField(default=0)
    post_date = models.DateField(default=date.today)

class ParentChildComment(models.Model):
    parent_comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name="%(app_label)s_%(class)s_related")
    child_comment = models.ForeignKey(Comment, on_delete=models.CASCADE)

class PlanComment(models.Model):
    parent_plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
    child_comment = models.ForeignKey(Comment, on_delete=models.CASCADE)


    