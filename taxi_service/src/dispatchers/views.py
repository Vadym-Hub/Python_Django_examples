from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views import generic

from .forms import CustomUserCreationForm
from .models import Car

User = get_user_model()


class UserSignupView(generic.CreateView):
    """
    Обработчик регистрации пользователя.
    """
    form_class = CustomUserCreationForm
    template_name = 'registration/signup_form.html'
    success_url = reverse_lazy('dispatchers:login')


class CarListView(LoginRequiredMixin, generic.ListView):
    """
    Обработчик списка машин в автопарке.
    """
    model = Car
    template_name = 'dispatchers/car_list.html'
    paginate_by = 5
