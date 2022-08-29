from django import forms
from .models import Snippet


class SnippetCreateForm(forms.ModelForm):
    class Meta:
        model = Snippet
        fields = ['title', 'code', 'linenos', 'language', 'style', 'tags']


class SearchForm(forms.Form):
    query = forms.CharField()
