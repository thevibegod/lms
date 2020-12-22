"""lms URL Configuration

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
from django.urls import path

from .views import *


urlpatterns = [
    path('manage/', manage_contests, name='view-contests'),
    path('create/', create_contest, name='create-contest'),
    path('delete/<int:pk>/', delete_contest, name='delete-contest'),
    path('edit/<int:pk>/', edit_contest, name='edit-contest'),
    path('manage/<int:id>/', view_questions, name='view-questions'),
    path('', view_contests, name='view-contests-student'),
    path('<int:id>/', view_contest_detail, name='view-contest-student'),
    path('start/<int:id>/',start_contest,name='start-contest')


]
