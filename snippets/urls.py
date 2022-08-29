from django.urls import path
from . import views

app_name = 'snippets'

urlpatterns = [
    path('', views.snippet_list, name='list'),
    path('tag/<slug:tag_slug>/', views.snippet_list, name='snippet_list_by_tag'),
    path('create/', views.snippet_create, name='create'),
    path('detail/<int:id>/<slug:slug>/', views.snippet_detail, name='detail'),
    path('like/', views.snippet_like, name='like'),
    path('search/', views.snippet_search, name='search'),
]
