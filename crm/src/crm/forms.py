from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UsernameField
from .models import Lead, Agent

User = get_user_model()


class CustomUserCreationForm(UserCreationForm):
    """Кастомная форма регистрации нового пользователя."""
    class Meta:
        model = User
        fields = ('username',)
        field_classes = {'username': UsernameField}


class AgentModelForm(forms.ModelForm):
    """
    Базовая форма для модели агента.
    """
    class Meta:
        model = User
        fields = (
            'email',
            'username',
            'first_name',
            'last_name',
        )


class AgentAssignToLeadForm(forms.Form):
    """
    Форма назначения агента свободному лиду.
    """
    agent = forms.ModelChoiceField(queryset=Agent.objects.none())

    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request')
        agents = Agent.objects.filter(organisation=request.user.organisation)
        super(AgentAssignToLeadForm, self).__init__(*args, **kwargs)
        self.fields["agent"].queryset = agents


class LeadModelForm(forms.ModelForm):
    """
    Базовая форма для модели лида.
    """
    class Meta:
        model = Lead
        fields = (
            'first_name',
            'last_name',
            'age',
            'agent',
            'phone_number',
            'email',
            'description',
        )


class LeadStatusUpdateForm(forms.ModelForm):
    """
    Форма обновления статуса лида.
    """
    class Meta:
        model = Lead
        fields = (
            'status',
        )
