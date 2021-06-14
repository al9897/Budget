"""budget_backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    ##
    # Auth
    path('login', views.login, name='login'),
    path('loggedin', views.loggedIn, name='loghed'),
    path('register', views.register, name='register'),
    ##
    path('profil/<int:id>/', views.profil, name='profil'),
    path(r'budget/', include('Budget.urls')),
    path(r'fp/', include('Fp.urls')),
    path(r'investment/', include('Investment.urls')),
    path('admin/', admin.site.urls),
]
