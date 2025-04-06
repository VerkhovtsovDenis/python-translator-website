from django.urls import include, path
from translator_project.settings import PREFIX

urlpatterns = [
    path(PREFIX[1:] + "/" if PREFIX else PREFIX, include('main.urls'), name='main'),
]
