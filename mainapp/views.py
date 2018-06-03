from django.shortcuts import render
from django.http import JsonResponse, HttpResponseRedirect
import requests, json
from django.urls import reverse
from user.views import account
from .models import WordForms, UniversalDictionary, UserWords
from django.contrib.auth.models import User
#from nltk.stem import SnowballStemmer

def index(request):
    if request.user.is_authenticated:
        return account(request, request.user.id)
    else:
	    return render(request, 'mainapp/index_no_auth.html', {})

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
            'link': '/excercises/translation/' 
        },
        {
            'header': 'Обратный перевод',
            'description': 'Выберите перевод предложенного слова на испанский из нескольких вариантов',
            'link': '/excercises/reverse-translation/' 
        },
        {
            'header': 'Собери слово',
            'description': 'Соберите слово из букв',
            'link': '/excercises/construct-the-word/' 
        },        
        
    ]
    return render(request, 'mainapp/exercises.html', {'user': request.user, 'exercises': exercises_mapping})