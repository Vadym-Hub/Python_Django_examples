from django.contrib.auth.models import User
from django import forms

from .models import Profile


class UserRegistrationForm(forms.ModelForm):
    """Форма регистрации пользователей"""
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'email')

    def clean_password2(self):
        """Проверка на некоректные данные"""
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Пароли не совпадают')
        return cd['password2']


class UserEditForm(forms.ModelForm):
    """Форма редактирования стандартного пользователя"""
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class ProfileEditForm(forms.ModelForm):
    """Форма редактирования дополнительных сведений"""

    class Meta:
        model = Profile
        fields = ('date_of_birth', 'photo')
