from django.urls import path, include
from django.contrib.auth.views import LoginView, LogoutView
from .forms import CustomLoginForm


urlpatterns = [
    path('login/', LoginView.as_view(authentication_form=CustomLoginForm), name='login'),
    path('logout/', LogoutView.as_view()),
    path('', include('django.contrib.auth.urls')),
]
