from django.contrib.auth.models import AbstractUser
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import UserLoginForm, UserRegistrationForm

AbstractUser


def login_view(request):
    """Вхід в систему"""
    form = UserLoginForm(request.POST or None)
    next_ = request.GET.get('next')
    if form.is_valid():
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username.strip(),
                            password=password.strip())
        login(request, user)
        next_post = request.POST.get('next')
        rederict_path = next_ or next_post or '/'
        return redirect(rederict_path)
    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    """Вихід із системи"""
    logout(request)
    return redirect('home')


def register_view(request):
    """Регістрація"""
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Створюємо нового користувача, но покищо не зберігаєм в базу данних.
            new_user = user_form.save(commit=False)
            # Задаем користувачу зашифрованний пароль.
            new_user.set_password(user_form.cleaned_data['password'])
            # зберігаєм користувача в базі данних.
            new_user.save()
            return render(request, 'accounts/register_done.html', {'new_user': new_user})
        return render(request, 'accounts/register.html', {'form': user_form})
    else:
        user_form = UserRegistrationForm()
        return render(request, 'accounts/register.html', {'form': user_form})
