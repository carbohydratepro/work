from django.urls import path
from . import views

urlpatterns = [
    path('', views.display_calendar, name='display-calendar'),
    path('details/<str:date>/', views.date_specific_page, name='date-specific-page'),
]
