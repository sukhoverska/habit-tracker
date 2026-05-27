from django.urls import path
from . import views

urlpatterns = [
    path('', views.habit_list, name='habit_list'),
    path('create/', views.habit_create, name='habit_create'),
    path('complete/<int:habit_id>/', views.habit_complete, name='habit_complete'),
    path('delete/<int:habit_id>/', views.habit_delete, name='habit_delete'),
    path('edit/<int:habit_id>/', views.habit_edit, name='habit_edit'),
]