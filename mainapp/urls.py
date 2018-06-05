from django.urls import path
from . import views

app_name = 'mainapp'
urlpatterns = [
    path('', views.index, name = 'index'),
    path('user/register/', views.user_register, name = 'register'),
    path('user/auth/', views.user_auth, name = 'auth'),
    path('user/logout/', views.user_logout_view, name = 'logout'),
    path('dictionary/', views.request_to_dictionary, name = 'dictionary'),
    path('add-to-dictionary/<int:translation_id>', views.add_to_dictionary, name = 'add_word'),
    path('get-dictionary-table/', views.get_dictionary_table, name = 'get_dictionary_table'),
    path('exercises/', views.exercises_page, name = 'exercises_page'),
    path('exercises/translation/', views.exercises_translation, name = 'exercises_translation'),
    path('exercises/translation/get-word-card/<int:user_word_id>/', views.get_exercises_translation_word_card, name = 'exercises_translation_word_card'),
    path('exercises/translation/get-words-list/', views.get_exercises_translation_word_list, name = 'exercises_translation_word_list'),
    path('exercises/reverse-translation/', views.exercises_reverse_translation, name = 'exercises_reverse_translation'),
    path('exercises/reverse-translation/get-word-card/<int:user_word_id>/', views.get_exercises_reverse_translation_word_card, name = 'get_exercises_reverse_translation_word_card'),
    path('exercises/reverse-translation/get-words-list/', views.get_exercises_translation_word_list, name = 'exercises_translation_word_card'),
    path('exercises/construct-the-word/', views.exercises_construct_the_word, name = 'exercises_construct_the_word'),
    path('exercises/construct-the-word/get-word-card/<int:user_word_id>/', views.get_exercises_construct_the_word_card, name = 'get_exercises_construct_the_word_card'),
    path('exercises/construct-the-word/get-words-list/', views.get_exercises_translation_word_list, name = 'exercises_translation_word_card')
]