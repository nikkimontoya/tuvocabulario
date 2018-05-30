from django.urls import path
from . import views

app_name = 'mainapp'
urlpatterns = [
    path('', views.index, name = 'index'),
    path('dictionary/', views.request_to_dictionary, name = 'dictionary'),
    path('add-to-dictionary/<int:word_id>/', views.add_to_dictionary, name = 'add_word'),
    path('get-dictionary-table/', views.get_dictionary_table, name = 'get_dictionary_table'),
]