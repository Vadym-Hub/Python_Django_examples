from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UsernameField
from django import forms

User = get_user_model()


class CustomUserCreationForm(UserCreationForm):
    """
    Кастомная форма регистрации нового пользователя.
    """

    class Meta:
        model = User
        fields = ('username', )
        field_classes = {'username': UsernameField}


class CarToPoolForm(forms.Form):
    """
    Форма для записи на курсы.
    """
    car = forms.BooleanField(widget=forms.HiddenInput)
