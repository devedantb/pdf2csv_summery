from django.urls import path, include
from . import views

urlpatterns = [
    path('',views.index,name='index'),
    path('getdata/<path:csv_file_url>/',views.download_csv,name='csv_summery'),
    # path('download/<path:csv_file_url>/', views.download_file, name='download_file'),
]