from . import views
from django.urls import path

app_name = 'main'

urlpatterns = [
    # Главная страница.
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('history/', views.history, name='history'),
    path('history/del/', views.history_del, name='history_del'),
]
