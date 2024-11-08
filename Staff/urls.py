"""
URL configuration for Staff project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from app01 import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('depart/list/', views.depart_list),
    path('depart/add/', views.adddepart),
    path('depart/delete/', views.depart_delete),
    path('depart/<int:nid>/edit/', views.depart_edit),
    path('depart/listpro/', views.depart_listpro),
    path('depart/addpro/', views.depart_addpro),
    path('depart/<int:nid>/editpro/', views.depart_editpro),
    path('User/list/', views.User_list),
    path('User/add/', views.User_add),
    path('yunge/<str:classname>/<str:methodname>/', views.yunge),


]
