from django.urls import path
from . import views

urlpatterns = [
    path('', views.ai_analysis, name='ai_analysis'),
]