from django.urls import path
from . import views

app_name = 'snippets'

urlpatterns = [
    path('create/', views.snippet_create, name='create'),
]
