from django.urls import path
from . import views

app_name = 'rest_api'

urlpatterns = [
    path('points/', views.api_points),
]
