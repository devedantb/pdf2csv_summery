from django.urls import path, include
from . import views

urlpatterns = [
    path('getresponse/<path:json_file_url>/', views.ask_and_get_insights, name='getresponse')
]