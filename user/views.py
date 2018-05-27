from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, JsonResponse, HttpResponseForbidden
from django.urls import reverse

# Create your views here.

def register(request):
    user = User.objects.create_user(request.POST['email'], request.POST['email'], request.POST['password'])
    if user is not None:
        login(request, user)
        return JsonResponse({'status': 1, 'user_id': user.id})
    else:	
        return JsonResponse({'status': 0})

def auth(request):
	user = authenticate(username = request.POST['email'], password = request.POST['password'])
	if user is not None:
		login(request, user)
		return JsonResponse({'status': 1, 'user_id': user.id})
	else:	
	    return JsonResponse({'status': 0})

def account(request, user_id):
    if request.user.id == user_id:
        return render(request, 'user/account.html', {})
    else:
        return HttpResponseForbidden()
        '''return HttpResponseRedirect(reverse('mainapp:index'))'''

def logout_view(request):
	logout(request)
	return HttpResponseRedirect(reverse('mainapp:index'))