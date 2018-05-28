from django.urls import path
from . import views

app_name = 'user'
urlpatterns = [
    path('register/', views.register, name = 'register'),
    path('auth/', views.auth, name = 'auth'),
    path('logout/', views.logout_view, name = 'logout')
]