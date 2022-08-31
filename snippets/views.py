from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.postgres.search import TrigramSimilarity
from taggit.models import Tag
from .forms import SnippetCreateForm, SearchForm
from .models import Snippet


import redis
from django.conf import settings
# connect to redis
r = redis.Redis(host=settings.REDIS_HOST,
                port=settings.REDIS_PORT,
                db=settings.REDIS_DB)

@login_required
def snippet_create(request):
    if request.method == 'POST':
        form = SnippetCreateForm(data=request.POST)
        if form.is_valid():
            new_snippet = form.save(commit=False)
            #  assign current user to the item
            new_snippet.user = request.user
            new_snippet.save()
            form.save_m2m()
            messages.success(request, 'Snippet added successfully')
            #  redirect to new created item detail view
            return redirect(new_snippet.get_absolute_url())
    else:
        form = SnippetCreateForm()
    return render(request, 'snippets/snippet/create.html', {'section': 'snippets', 'form': form})


def snippet_detail(request, id, slug):
    snippet = get_object_or_404(Snippet, id=id, slug=slug)
    total_views = r.incr(f'snippet:{snippet.id}:views')
    # string: language,style,linenos for custom template tag
    snippet_config = f"{snippet.language},{snippet.style},{snippet.linenos}"
    return render(request, 'snippets/snippet/detail.html', {'section': 'snippets', 'snippet': snippet,
                                                            'snippet_config': snippet_config,
                                                            'total_views': total_views})


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


def snippet_list(request, tag_slug=None):
    snippets = Snippet.objects.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        snippets = snippets.filter(tags__in=[tag])
    paginator = Paginator(snippets, 8)
    page = request.GET.get('page')
    snippets_only = request.GET.get('snippets_only')
    try:
        snippets = paginator.page(page)
    except PageNotAnInteger:
        snippets = paginator.page(1)
    except EmptyPage:
        if snippets_only:
            return HttpResponse('')
        snippets = paginator.page(paginator.num_pages)
    if snippets_only:
        return render(request, 'snippets/snippet/list_snippets.html', {'section': 'images', 'snippets': snippets, 'tag': tag})
    return render(request, 'snippets/snippet/list.html', {'section': 'snippets', 'snippets': snippets, 'tag': tag})


def snippet_search(request):
    form = SearchForm()
    query = None
    results = []
    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            results = Snippet.objects.annotate(
                similarity=TrigramSimilarity('title', query),
            ).filter(similarity__gt=0.1).order_by('-similarity')
    return render(request, 'snippets/snippet/search.html', {'form': form, 'query': query, 'results': results})