from django.urls import path
from . import views # type: ignore

urlpatterns = [
    path('', views.task_list, name='task_list'),
]