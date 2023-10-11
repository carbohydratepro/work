from django.urls import path
from . import views
from django.contrib import admin

urlpatterns = [
    path('', views.display_calendar, name='display-calendar'),
    path('details/<str:date>/', views.detail, name='detail'),
    path('new/', views.new, name='new'), # 投稿用WebページのURL
    path('get-events/', views.get_events, name='get-events'),
    path('edit/<int:shift_id>/', views.edit, name='edit'),
    path('delete/<int:shift_id>/', views.delete, name='delete'),
    path('check-shift-exists/<str:date>/', views.check_shift_exists, name='check_shift_exists'),
    path('update_user_view_type', views.update_user_view_type, name='update_user_view_type'),
    path('admin/', admin.site.urls),
    # path('test', views.test, name='test'),
]