from django.shortcuts import render, HttpResponse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from snippets.models import Snippet
from .forms import UserRegistrationForm, UserEditForm, ProfileEditForm
from django.contrib import messages


@login_required
def dashboard(request):
    snippets = Snippet.objects.filter(user=request.user)
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
        return render(request, 'snippets/snippet/list_snippets.html', {'section': 'dashboard', 'snippets': snippets})
    return render(request, 'account/dashboard.html', {'section': 'dashboard', 'snippets': snippets})


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            return render(request,
                          'account/register_done.html',
                          {'new_user': new_user})
        else:
            messages.error(request, 'Error with creating your account', extra_tags='danger')
    else:
        user_form = UserRegistrationForm()
    return render(request, 'account/register.html', {'user_form': user_form})


@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile, data=request.POST, files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated successfully')
        else:
            messages.error(request, 'Error updating your profile', extra_tags='danger')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(request, 'account/edit.html', {'user_form': user_form, 'profile_form': profile_form})
