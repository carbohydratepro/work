from django.urls import path
from . import views

urlpatterns = [
    path('', views.display_calendar, name='display_calendar'),
]
