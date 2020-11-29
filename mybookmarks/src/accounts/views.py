from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django.views.decorators.http import require_POST

from actions.utils import create_action
from actions.models import Action

from .forms import UserRegistrationForm, UserEditForm, ProfileEditForm
from .models import Profile, Contact


@login_required
def dashboard(request):
    """Обработчик робочего стола"""
    # По умолчанию отображаем все действия.
    actions = Action.objects.exclude(user=request.user)
    following_ids = request.user.following.values_list('id', flat=True)
    if following_ids:
        # Если текущий пользователь подписался на кого-то, отображаем только действия этих пользователей.
        actions = actions.filter(user_id__in=following_ids)
    # actions = actions[:10]
    # Оптимизированый вариант QuerySet со связанными объектами
    actions = actions.select_related('user', 'user__profile').prefetch_related('target')[:10]
    return render(request, 'accounts/dashboard.html', {'section': 'dashboard',
                                                       'actions': actions})


def register(request):
    """Обработчик регистрации"""
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Создаем нового пользователя, но пока не сохраняем в базу данных.
            new_user = user_form.save(commit=False)
            # Задаем пользователю зашифрованный пароль.
            new_user.set_password(user_form.cleaned_data['password'])
            # Сохраняем пользователя в базе данных.
            new_user.save()
            # Создание профиля пользователя.
            Profile.objects.create(user=new_user)
            create_action(new_user, 'has created an account')
            return render(request, 'accounts/register_done.html', {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'accounts/register.html', {'user_form': user_form})


@login_required
def edit(request):
    """Обработчик для сохранения изменений в профиле"""
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile,
                                       data=request.POST,
                                       files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Профиль удачно обновлен')
        else:
            messages.error(request, 'Ошибка обновления профиля')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(request, 'accounts/edit.html', {'user_form': user_form,
                                                  'profile_form': profile_form})


@login_required
def user_list(request):
    """Обработчик списка пользователей"""
    users = User.objects.filter(is_active=True)
    return render(request, 'accounts/user/list.html', {'section': 'people',
                                                       'users': users})


@login_required
def user_detail(request, username):
    """Обработчик подробностей профиля"""
    user = get_object_or_404(User, username=username, is_active=True)
    return render(request, 'accounts/user/detail.html', {'section': 'people',
                                                         'user': user})


@login_required
@require_POST
@login_required
def user_follow(request):
    """AJAX-обработчик для создания подписчика"""
    user_id = request.POST.get('id')
    action = request.POST.get('action')
    if user_id and action:
        try:
            user = User.objects.get(id=user_id)
            if action == 'follow':
                Contact.objects.get_or_create(user_from=request.user, user_to=user)
                create_action(request.user, 'is following', user)
            else:
                Contact.objects.filter(user_from=request.user, user_to=user).delete()
            return JsonResponse({'status': 'ok'})
        except User.DoesNotExist:
            return JsonResponse({'status': 'ok'})
    return JsonResponse({'status': 'ok'})
