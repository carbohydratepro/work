from django.urls import path
from . import views

urlpatterns = [
    path('', views.display_calendar, name='display-calendar'),
    path('details/<str:date>/', views.detail, name='detail'),
    path('new', views.new, name='new'), # 投稿用WebページのURL
    path('create', views.create, name='create'), # 新規投稿をデータベースに保存するためのURL
]
