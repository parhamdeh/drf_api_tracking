from django.urls import path
from . import views


app_name = "traking"
urlpatterns = [
    path('', views.HomeAPIView.as_view(), name='home'),
]