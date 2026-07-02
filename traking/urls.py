from django.urls import path, include
from . import views


app_name = "traking"
urlpatterns = [
    path('', views.HomeAPIView.as_view(), name='home'),
]