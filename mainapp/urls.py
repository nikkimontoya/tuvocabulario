from django.urls import path
from . import views

app_name = 'mainapp'
urlpatterns = [
    path('', views.index, name = 'index'),
    path('dictionary/', views.request_to_dictionary, name = 'dictionary')
]