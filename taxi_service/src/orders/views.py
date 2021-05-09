from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic

from dispatchers.models import Car
from .models import Order
from .forms import OrderForm


class OrderCreateView(generic.CreateView):
    """
    Обработчик вывода формы для создания заказа.
    """
    model = Order
    form_class = OrderForm
    template_name = 'orders/order_create_form.html'

    def form_valid(self, form):
        """
        Если форма валидна, назначаем свободное авто.
        """
        # Берем первый елемент из списка свободных авто.
        try:
            car = Car.objects.filter(is_busy=False).first()
            form.instance.car = car
            # Ставим флаг, что авто зайнято.
            car.is_busy = True
            car.save()
            return super().form_valid(form)
        except:
            return HttpResponseRedirect('/error/')

    def get_success_url(self):
        return reverse('orders:order_success', kwargs={'pk': self.object.pk})


class OrderDetailView(LoginRequiredMixin, generic.DetailView):
    """
    Обработчик вывода деталей заказа.
    """
    model = Order
    template_name = 'orders/order_detail.html'


class OrderListView(LoginRequiredMixin, generic.ListView):
    """
    Обработчик вывода списка заказов.
    """
    model = Order
    template_name = 'orders/order_list.html'
    paginate_by = 5


class OrderSuccessView(generic.DetailView):
    """
    Выводит страницу с оформленным заказом.
    """
    model = Order
    template_name = 'orders/order_success.html'


class OrderErrorView(generic.TemplateView):
    """
    Выводит страницу с извинениями если свободной машины нет.
    """
    template_name = 'orders/order_error.html'
