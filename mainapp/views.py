from django.shortcuts import render
from django.http import JsonResponse, HttpResponseRedirect, HttpResponseForbidden
import requests, json, random
from django.urls import reverse
from .models import WordForms, UniversalDictionary, UserWords, UniversalTranslation
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

#from nltk.stem import SnowballStemmer

def index(request):
    if request.user.is_authenticated:
        return user_account(request, request.user.id)
    else:
	    return render(request, 'mainapp/index.html', {})

token = '';
def request_to_dictionary(request):
    '''wordForm = WordForms.objects.filter(form = request.POST['text'])
    responseObject = {}
  
    if wordForm.exists():
        word = wordForm.first().word
        responseObject['original'] = word.original
        responseObject['translation'] = word.translation
        responseObject['wordId'] = word.id
    else:
        global token
        if token == '':
            token = requests.post('https://developers.lingvolive.com/api/v1.1/authenticate', headers = {"Authorization": "Basic ZTc1ZDY2MmMtZjkxZi00NTNlLWExY2MtNjA3Y2RlNjJhMDYyOjQzOGZlNzcxNTAxODQzODI4OTA3OWI4MjQ2ZmExZTI1"}, verify = False).text
    
        response = requests.get('https://developers.lingvolive.com/api/v1/Minicard', headers = {"Authorization": "Bearer " + token}, params = {"text": request.POST['text'], "srcLang": 1034, "dstLang": 1049}, verify = False)
        response = json.loads(response.text)

        responseObject['original'] = response['Heading']
        responseObject['translation'] = response['Translation']['Translation']

        newWord = Dictionary.objects.filter(original = responseObject['original'])

        if newWord.exists():
            newWord = newWord.first()
        else:
            newWord = Dictionary(original = responseObject['original'], translation = responseObject['translation'], soundFileName = response['Translation']['SoundName'])
            newWord.save()

        responseObject['wordId'] = newWord.id
        newWord.wordforms_set.create(form = request.POST['text'])'''

    '''s = SnowballStemmer('spanish');
    stemed = s.stem(request.POST['text'])'''
    word = UniversalDictionary.objects.filter(original = request.POST['text'])

    if word.exists():
        word = word.first()
        content = {
            'original': word.original,
            'translations': []
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

    return render(request, 'mainapp/translation_card_content.html', {'content': content})

def add_to_dictionary(request, translation_id):
    q = UserWords.objects.filter(user = request.user.id, translation = translation_id)

    if not q.exists():
        request.user.userwords_set.create(translation_id = translation_id)

    return JsonResponse({})

def get_dictionary_table(request):
    return render(request, 'mainapp/dictionary_table.html', {'user': request.user})

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
        
    ]
    return render(request, 'mainapp/exercises/index.html', {'user': request.user, 'exercises': exercises_mapping})

def exercises_translation(request):
    return render(request, 'mainapp/exercises/translation/index.html', {})

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

        translations.append({'translation': UniversalTranslation.objects.get(pk = random_pk).translation, 'isRight': 0})

    random.shuffle(translations)

    return render(request, 'mainapp/exercises/translation/word_card.html', {'word': word, 'translations': translations})

def get_exercises_translation_word_list(request):
    user_words_ids = list(request.user.userwords_set.all().values_list('id', flat = True))
    print(user_words_ids)
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
        '''return HttpResponseRedirect(reverse('mainapp:index'))'''

def user_logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('mainapp:index'))   