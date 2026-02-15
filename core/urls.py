from django.urls import path
from . import views
from .views import TestView

urlpatterns = [
    path('health/', views.health_check, name='health_check'),
    path("test/", TestView.as_view()),
]
