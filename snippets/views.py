from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import SnippetCreateForm


@login_required
def snippet_create(request):
    if request.method == 'POST':
        form = SnippetCreateForm(data=request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            new_snippet = form.save(commit=False)
            #  assign current user to the item
            new_snippet.user = request.user
            new_snippet.save()
            messages.success(request, 'Snippet added successfully')
            #  redirect to new created item detail view
            return redirect(new_snippet.get_absolute_url())
    else:
        form = SnippetCreateForm()
    return render(request, 'snippets/snippet/create.html', {'section': 'snippets', 'form': form})


