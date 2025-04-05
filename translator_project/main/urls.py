from . import views
from django.urls import path

app_name = 'main'

BASE_PATH = 'translator-website/'

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('history/del/', views.history_del, name='history_del'),
    path('history/', views.history, name='history'),
]