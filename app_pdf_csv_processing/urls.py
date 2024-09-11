from django.urls import path, include, re_path
from . import views

urlpatterns = [
    path('',views.index,name='index'),
    path('getdata/<path:csv_file_url>/',views.download_csv,name='csv_summery'),
    re_path(r'^.*', views.index, name='index'),
    # path('download/<path:csv_file_url>/', views.download_file, name='download_file'),
]