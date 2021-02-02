from django.urls import path

from . import views

app_name = 'notifier'
urlpatterns = [
    path('', views.home, name='home'),
]
