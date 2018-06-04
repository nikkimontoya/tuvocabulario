from django.urls import path
from . import views

app_name = 'mainapp'
urlpatterns = [
    path('', views.index, name = 'index'),
    path('dictionary/', views.request_to_dictionary, name = 'dictionary'),
    path('add-to-dictionary/<int:translation_id>', views.add_to_dictionary, name = 'add_word'),
    path('get-dictionary-table/', views.get_dictionary_table, name = 'get_dictionary_table'),
    path('exercises/', views.exercises_page, name = 'exercises_page'),
    path('exercises/translation/', views.exercises_translation, name = 'exercises_translation'),
    path('exercises/translation/get-word-card/<int:user_word_id>/', views.get_exercises_translation_word_card, name = 'exercises_translation_word_card'),
    path('exercises/translation/get-words-list/', views.get_exercises_translation_word_list, name = 'exercises_translation_word_list')
]