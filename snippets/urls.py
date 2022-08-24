from django.urls import path
from . import views

app_name = 'snippets'

urlpatterns = [
    path('create/', views.snippet_create, name='create'),
    path('detail/<int:id>/<slug:slug>/', views.snippet_detail, name='detail'),
    path('like/', views.snippet_like, name='like'),
]
