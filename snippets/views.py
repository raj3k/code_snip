from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .forms import SnippetCreateForm
from .models import Snippet


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


def snippet_detail(request, id, slug):
    snippet = get_object_or_404(Snippet, id=id, slug=slug)
    # string: language,style,linenos for custom template tag
    snippet_config = f"{snippet.language},{snippet.style},{snippet.linenos}"
    return render(request, 'snippets/snippet/detail.html', {'section': 'snippets', 'snippet': snippet,
                                                            'snippet_config': snippet_config})


@login_required
@require_POST
def snippet_like(request):
    snippet_id = request.POST.get('id')
    action = request.POST.get('action')
    if snippet_id and action:
        try:
            snippet = Snippet.objects.get(id=snippet_id)
            if action == 'like':
                snippet.users_like.add(request.user)
            else:
                snippet.users_like.remove(request.user)
            return JsonResponse({'status': 'ok'})
        except:
            pass
    return JsonResponse({'status': 'error'})
