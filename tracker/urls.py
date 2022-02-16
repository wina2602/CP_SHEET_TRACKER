from django.urls import path
from . import views
urlpatterns = [
    path('', views.home , name = "tracker-home"),
    path('invalid_username/',views.invalid_username , name = 'invalidusername')
]
