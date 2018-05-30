from django.shortcuts import render
from django.http import JsonResponse, HttpResponseRedirect
import requests, json
from django.urls import reverse
from user.views import account
from .models import WordForms, Dictionary

def index(request):
    if request.user.is_authenticated:
        return account(request, request.user.id)
    else:
	    return render(request, 'mainapp/index_no_auth.html', {})

token = '';
def request_to_dictionary(request):
    wordForm = WordForms.objects.filter(form = request.POST['text'])
    responseObject = {}
  
    if wordForm.exists():
        word = wordForm.first().word
        responseObject['original'] = word.original
        responseObject['translation'] = word.translation
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
            
        newWord.wordforms_set.create(form = request.POST['text'])        

    return JsonResponse(responseObject)
