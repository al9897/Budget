from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('welcome', views.welcome, name='welcome'),
    path('users/', views.UserList.as_view()),
    path('users/<int:pk>/', views.UserDetail.as_view()),
    path('comments/', views.CommentList.as_view()),
    path('comments/<int:pk>/', views.CommentDetail.as_view()),
    path('follows/', views.FollowList.as_view()),
    path('follows/<int:pk>/', views.FollowDetail.as_view()),
    path('plans/', views.PlanList.as_view()),
    path('plans/<int:pk>/', views.PlanDetail.as_view()),
    path('plancomments/', views.PlanCommentList.as_view()),
    path('plancomments/<int:pk>/', views.PlanCommentDetail.as_view()),
    
]
