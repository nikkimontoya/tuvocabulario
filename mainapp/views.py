from django.shortcuts import render
from django.http import JsonResponse, HttpResponseRedirect, HttpResponseForbidden
import requests, json, random
from django.urls import reverse
from .models import WordForms, UniversalDictionary, UserWords, UniversalTranslation
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from .utilities.genxword import Crossword
from .utilities.utilities import get_sound_file_name
from django.template import loader
from pprint import pprint
import base64
import os

from pattern import es

def index(request):
    if request.user.is_authenticated:
        return user_account(request, request.user.id)
    else:
	    return render(request, 'mainapp/index.html', {})

@csrf_exempt
def request_to_dictionary(request):
    word = UniversalDictionary.objects.filter(original = request.GET['text'])

    if not word.exists():
        word = UniversalDictionary.objects.filter(original__iexact = request.GET['text'])
    if not word.exists():
        text = es.parse(request.GET['text'], lemmata = True).split('/')[4]
        word = UniversalDictionary.objects.filter(original__iexact = text)

    if word.exists():
        word = word.first()
        content = {
            'original': word.original,
            'translations': [],
            'sound': get_sound_file_name(word)
        }

        for translation in word.universaltranslation_set.all():
            content['translations'].append({
                'translation': translation.translation,
                'translationId': translation.id
            }) 
    else:
        content = {
            'original': 'Перевод не найден'
        }           

    response = render(request, 'mainapp/account/translation_card_content.html', {'content': content})

    if request.META.get('HTTP_ORIGIN'):
        response['Access-Control-Allow-Origin'] = request.META['HTTP_ORIGIN']

    return response

def add_to_dictionary(request, translation_id):
    if request.user.is_authenticated:
        q = UserWords.objects.filter(user = request.user.id, translation = translation_id)

        if not q.exists():
            request.user.userwords_set.create(translation_id = translation_id)

        return JsonResponse({'status': 1})
    else:
        return JsonResponse({'status': 0, 'message': 'Пожалуйста, авторизуйтесь, чтобы иметь возможность добавлять слова'})    

def remove_from_dictionary(request):
    UserWords.objects.get(pk = request.POST['word_id']).delete()
    return JsonResponse({})

def get_dictionary_table(request):
    words = []
    user_words = request.user.userwords_set.all()
    soundsDir = os.path.dirname(__file__) + '/static/mainapp/sounds/'
    for word in user_words:
        translation_object = word.translation
        word_object = translation_object.original
        soundFileName = get_sound_file_name(word_object)

        words.append({
            'word': word_object.original,
            'translation': translation_object.translation,
            'sound': soundFileName,
            'user_word_id': word.id
            })           

    return render(request, 'mainapp/account/dictionary_table.html', {'words': words})

def exercises_page(request):
    exercises_mapping = [
        {
            'header': 'Перевод',
            'description': 'Выберите перевод предложенного слова на русский из нескольких вариантов',
            'link': '/exercises/translation/' 
        },
        {
            'header': 'Обратный перевод',
            'description': 'Выберите перевод предложенного слова на испанский из нескольких вариантов',
            'link': '/exercises/reverse-translation/' 
        },
        {
            'header': 'Собери слово',
            'description': 'Соберите слово из букв',
            'link': '/exercises/construct-the-word/' 
        },        
        {
            'header': 'Кроссворд',
            'description': 'Разгадайте кроссворд, составленный из ваших слов',
            'link': '/exercises/crossword/' 
        },
        {
            'header': 'Аудирование',
            'description': 'Запишите слово, прослушав его произношение',
            'link': '/exercises/audio/' 
        },  
    ]
    return render(request, 'mainapp/exercises/index.html', {'user': request.user, 'exercises': exercises_mapping})

def exercises_translation(request):
    return render(request, 'mainapp/exercises/translation/index.html', {})

def exercises_reverse_translation(request):
    return render(request, 'mainapp/exercises/reverse-translation/index.html', {})

def exercises_construct_the_word(request):
    return render(request, 'mainapp/exercises/construct-the-word/index.html', {})

def exercises_crossword(request):
    user_words = request.user.userwords_set.all()
    word_list = []

    for user_word in user_words:
        translation_object = user_word.translation
        word_list.append([
            translation_object.original.original,
            translation_object.translation
            ])

    crossword_object = Crossword(rows = 10, cols = 10, available_words = word_list)
    crossword_object.compute_crossword()
    crossword = crossword_object.best_grid
    index_list = crossword_object.best_grid
    translations_list = {
        'horizontal': [],
        'vertical': []
    }

    
    rows = len(index_list)
    cols = len(index_list[0])

    for i in range(rows):
        for j in range(cols):
            index_list[i][j] = {
                'indexhor': 0,
                'indexver': 0,
                'letter': ' ',
                'first_letter_hor': False,
                'first_letter_ver': False
            }

    hor_counter = 0
    ver_counter = 0
    for word_l in crossword_object.best_wordlist:
        word = word_l[0]
        translation = word_l[1]
        row = word_l[2]
        col = word_l[3]
        isHorisontal = word_l[4] == 0
        
        tr_obj = {
            'translation': translation
            }

        if isHorisontal:
            hor_counter += 1
            tr_obj['index'] = hor_counter
            translations_list['horizontal'].append(tr_obj)
        else:
            ver_counter += 1
            tr_obj['index'] = ver_counter
            translations_list['vertical'].append(tr_obj)
        
        first_letter = True
        for letter in word:            
            index_list[row][col]['letter'] = letter;            
            if isHorisontal:
                index_list[row][col]['indexhor'] = hor_counter;
                index_list[row][col]['first_letter_hor'] = first_letter;
                col += 1
            else:
                index_list[row][col]['indexver'] = ver_counter;
                index_list[row][col]['first_letter_ver'] = first_letter;
                row +=1
            first_letter = False                

    crossword_table_template = loader.get_template('mainapp/exercises/crossword/crossword.html')
    crossword_table = crossword_table_template.render({'crossword': index_list, 'translations': translations_list}, request)

    return render(request, 'mainapp/exercises/crossword/index.html', {'crossword': crossword_table})  

def exercises_audio(request):
    return render(request, 'mainapp/exercises/audio/index.html', {})

def get_exercises_translation_word_card(request, user_word_id):
    user_word = UserWords.objects.get(pk = user_word_id)
    translation = user_word.translation.translation
    word_object = user_word.translation.original
    word = word_object.original

    # Количество переводов в базе. 
    # Их всегда столько, и первичные ключи располагаются от 1 до этого числа
    # Сделано, чтобы не запрашивать каждый раз количество записей
    translations_count = 146518

    random.seed()
    translations = []
    translations.append({'translation': translation, 'isRight': 1})
    # Идентификаторы всех переводов текущего слова, т.к. мы не хотим получить один из них
    current_word_translations_ids = list(word_object.universaltranslation_set.all().values_list('id', flat = True))
    # Получение четырех случайных переводов в дополение к одному правильному
    for i in range(4):
        # Получаем рандомный идентификатор перевода
        random_pk = random.randint(1, translations_count)
        # Гарантируем, что не получим id одного из переводов текущего слова
        while current_word_translations_ids.count(random_pk) != 0:
            random_pk = random.randint(1, translations_count)

        translation = UniversalTranslation.objects.get(pk = random_pk).translation
        # Гарантируем, что перевод не содержит "см.": сокращение от "смотри", отсылающее к другому испанскому слову
        while translation.find('см.') != -1:
            random_pk = random.randint(1, translations_count)
            translation = UniversalTranslation.objects.get(pk = random_pk).translation

        translations.append({'translation': translation, 'isRight': 0})

    random.shuffle(translations)

    return render(request, 'mainapp/exercises/translation/word_card.html', {
        'word': word,
        'translations': translations
        })

def get_exercises_reverse_translation_word_card(request, user_word_id):
    user_word = UserWords.objects.get(pk = user_word_id)
    translation_object = user_word.translation
    translation = translation_object.translation
    word_object = translation_object.original
    word = word_object.original

    # Количество слов в базе. 
    # Их всегда столько, и первичные ключи располагаются от 1 до этого числа
    # Сделано, чтобы не запрашивать каждый раз количество записей
    words_count = 77182

    random.seed()
    words = []
    words.append({'word': word, 'isRight': 1})

    # Получение четырех случайных переводов в дополение к одному правильному
    for i in range(4):
        # Получаем рандомный идентификатор перевода (с двойки, т.к. первое слово в базе пустое)
        random_pk = random.randint(2, words_count)
        # Гарантируем, что не получим id изначального слова
        while random_pk == word_object.id:
            random_pk = random.randint(2, words_count)

        word = UniversalDictionary.objects.get(pk = random_pk).original

        words.append({'word': word, 'isRight': 0})

    random.shuffle(words)

    return render(request, 'mainapp/exercises/reverse-translation/word_card.html', {
        'translation': translation,
        'words': words
        })

def get_exercises_construct_the_word_card(request, user_word_id):
    user_word = UserWords.objects.get(pk = user_word_id)
    translation_object = user_word.translation
    translation = translation_object.translation
    word = translation_object.original.original
    word_list = list(word)
    letters_list = []

    while word_list != []:
        letter_dict = {
            'letter': word_list[0],
            'count': word_list.count(word_list[0])
            }
        

        for j in range(letter_dict['count']):
            word_list.remove(letter_dict['letter'])

        letters_list.append(letter_dict)

    random.seed()
    random.shuffle(letters_list)

    return render(request, 'mainapp/exercises/construct-the-word/word_card.html', {
        'word': word,
        'translation': translation,
        'letters_list': letters_list
        })

def get_exercises_audio_word_card(request, user_word_id):
    user_word = UserWords.objects.get(pk = user_word_id)
    word_object = user_word.translation.original

    return render(request, 'mainapp/exercises/audio/word_card.html', {
        'word': word_object.original,
        'sound': '/static/mainapp/sounds/' + word_object.universalsounds_set.all().first().soundfile
        })    

def get_exercises_audio_word_list(request):
    # Получение всех id всех слов пользователя, у которых есть звуковые файлы
    user_words_ids = list(request.user.userwords_set.exclude(translation__original__universalsounds__soundfile = '').values_list('id', flat = True))
    responseObject = {
        'wordList': []
    }

    random.seed()
    user_words_count = len(user_words_ids)
    if user_words_count <= 10:
        random.shuffle(user_words_ids)
        responseObject['wordList'] = user_words_ids
    else:
        random_list = list(range(user_words_count))
        
        random.shuffle(random_list)
        print(random_list)
        for i in range(10):
            responseObject['wordList'].append(user_words_ids[random_list[i]])

    return JsonResponse(responseObject)


def get_exercises_translation_word_list(request):
    user_words_ids = list(request.user.userwords_set.all().values_list('id', flat = True))

    responseObject = {
        'wordList': []
    }

    random.seed()
    user_words_count = len(user_words_ids)
    if user_words_count <= 10:
        random.shuffle(user_words_ids)
        responseObject['wordList'] = user_words_ids
    else:
        random_list = list(range(user_words_count))
        
        random.shuffle(random_list)
        print(random_list)
        for i in range(10):
            responseObject['wordList'].append(user_words_ids[random_list[i]])

    return JsonResponse(responseObject)           

def user_register(request):
    user = User.objects.create_user(request.POST['email'], request.POST['email'], request.POST['password'])
    if user is not None:
        login(request, user)
        return JsonResponse({'status': 1, 'user_id': user.id})
    else:   
        return JsonResponse({'status': 0})

def user_auth(request):
    user = authenticate(username = request.POST['email'], password = request.POST['password'])
    if user is not None:
        login(request, user)
        return JsonResponse({'status': 1})
    else:   
        return JsonResponse({'status': 0})

def user_account(request, user_id):
    if request.user.id == user_id:
        return render(request, 'mainapp/account/index.html', {})
    else:
        return HttpResponseForbidden()

def user_logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('mainapp:index'))   