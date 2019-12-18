"""campus URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from CampusModel import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/', views.index),
    path('login/', views.login),
    path('forgot-password/', views.forgot_password),
    path('reset-password/', views.reset_password),
    path('logout/', views.logout),
    path('view-course/', views.view_course),
    path('search-result/', views.search_result),
    path('select-course/', views.select_course),
    path('start-select/', views.start_select),
    path('view-grade/', views.view_grade),
    path('calculate-grade/', views.calculate_grade),
    path('discussion-room/', views.discussion_room),
    path('classroom/', views.classroom),
]


