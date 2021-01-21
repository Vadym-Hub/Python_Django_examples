from django.urls import reverse_lazy
from django.views import generic

from ..forms import CustomUserCreationForm
from ..models import Organisation


class OrganisationCreateView(generic.CreateView):
    """
    Обработчик для кастомной регистрации.
    Когда создается User, одновременно с ним создается
    организация и привязуется к нему.
    Название организации берется из user.username.
    """

    template_name = 'registration/signup.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')


class LandingPageView(generic.TemplateView):
    """
    Обработчик страницы приветствия.
    """
    template_name = 'crm/landing.html'
