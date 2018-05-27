from django.shortcuts import render
from django.http import JsonResponse, HttpResponseRedirect
import requests, json
from django.urls import reverse

def index(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('user:account', args = (request.user.id,)))
    else:
	    return render(request, 'mainapp/index_no_auth.html', {})

token = '';
def request_to_dictionary(request):
    global token
    if token == '':
        token = requests.post('https://developers.lingvolive.com/api/v1.1/authenticate', headers = {"Authorization": "Basic ZTc1ZDY2MmMtZjkxZi00NTNlLWExY2MtNjA3Y2RlNjJhMDYyOjQzOGZlNzcxNTAxODQzODI4OTA3OWI4MjQ2ZmExZTI1"}, verify = False).text
    
    response = requests.get('https://developers.lingvolive.com/api/v1/Minicard', headers = {"Authorization": "Bearer " + token}, params = {"text": request.POST['text'], "srcLang": 1034, "dstLang": 1049}, verify = False)
    response = json.loads(response.text)
    return JsonResponse(response)
