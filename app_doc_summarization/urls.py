from django.urls import path, include, re_path
from . import views

urlpatterns = [
    path('getresponse/<path:json_file_url>/', views.ask_and_get_insights, name='getresponse'),
    # re_path(r'^.*', views.ask_and_get_insights, name='index'),
    # path('getresponse/', views.ask_and_get_insights, name='getresponse'),
]