from django.urls import path, include
from django.contrib.auth.views import LoginView
from .forms import CustomLoginForm


urlpatterns = [
    path('login/', LoginView.as_view(authentication_form=CustomLoginForm)),
    path('', include('django.contrib.auth.urls')),
]
