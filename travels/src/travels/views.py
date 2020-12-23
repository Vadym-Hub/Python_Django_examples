from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views import generic

from .forms import RouteForm, RouteModelForm
from .models import Route, City, Train
from .services import get_routes


def home(request):
    """Обработчик главной страницы."""
    form = RouteForm()
    return render(request, 'travels/home.html', {'form': form})


def find_route(request):
    """Обработчик поиска маршрута."""
    if request.method == "POST":
        form = RouteForm(request.POST)
        if form.is_valid():
            try:
                context = get_routes(request, form)
            except ValueError as e:
                messages.error(request, e)
                return render(request, 'travels/home.html', {'form': form})
            return render(request, 'travels/home.html', context)
        return render(request, 'travels/home.html', {'form': form})
    else:
        form = RouteForm()
        messages.error(request, 'Нет данных для поиска')
        return render(request, 'travels/home.html', {'form': form})


def add_route(request):
    """Обработчик добавления маршрута."""
    if request.method == 'POST':
        context = {}
        data = request.POST
        if data:
            total_time = int(data['total_time'])
            from_city_id = int(data['from_city'])
            to_city_id = int(data['to_city'])
            trains = data['trains'].split(',')
            trains_lst = [int(t) for t in trains if t.isdigit()]
            qs = Train.objects.filter(id__in=trains_lst).select_related('from_city', 'to_city')
            cities = City.objects.filter(id__in=[from_city_id, to_city_id]).in_bulk()
            form = RouteModelForm(initial={'from_city': cities[from_city_id],
                                           'to_city': cities[to_city_id],
                                           'travel_times': total_time,
                                           'trains': qs})
            context['form'] = form
        return render(request, 'travels/route/route_create_form.html', context)
    else:
        messages.error(request, 'Невозможно сохранить несуществующий маршрут')
        return redirect('/')


def save_route(request):
    """Обработчик сохранения маршрута."""
    if request.method == "POST":
        form = RouteModelForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Маршрут успешно сохранен")
            return redirect('/')
        return render(request, 'travels/route/route_create.html', {'form': form})
    else:
        messages.error(request, 'Невозможно сохранить несуществующий маршрут')
        return redirect('/')


class RouteListView(generic.ListView):
    """Обработчик списка маршрутов."""
    model = Route
    template_name = 'travels/route/route_list.html'
    paginate_by = 5


class RouteDetailView(generic.DetailView):
    """Обработчик деталей маршрута."""
    model = Route
    template_name = 'travels/route/route_detail.html'


class RouteDeleteView(SuccessMessageMixin, LoginRequiredMixin, generic.DeleteView):
    """Обработчик удаления маршрута."""
    model = Route
    template_name = 'travels/route/route_confirm_delete.html'
    success_url = reverse_lazy('travels:route_list')
    success_message = 'Маршрут удален!'
    login_url = '/accounts/login/'


class CityListView(generic.ListView):
    """Обработчик спискак городов."""
    model = City
    template_name = 'travels/city/city_list.html'
    paginate_by = 5


class CityCreateView(SuccessMessageMixin, LoginRequiredMixin, generic.CreateView):
    """Обработчик создания города."""
    model = City
    fields = ('name',)
    template_name = 'travels/city/city_create_form.html'
    success_url = reverse_lazy('travels:city_list')
    success_message = 'Город создан!'
    login_url = '/accounts/login/'


class CityUpdateView(SuccessMessageMixin, LoginRequiredMixin, generic.UpdateView):
    """Обработчик редактирования города."""
    model = City
    fields = ('name',)
    template_name = 'travels/city/city_update_form.html'
    success_url = reverse_lazy('travels:city_list')
    success_message = 'Город отредактировано!'
    login_url = '/accounts/login/'


class CityDeleteView(SuccessMessageMixin, LoginRequiredMixin, generic.DeleteView):
    """Обработчик удаления города."""
    model = City
    template_name = 'travels/city/city_confirm_delete.html'
    success_url = reverse_lazy('travels:city_list')
    success_message = 'Город успешно удален!!'
    login_url = '/accounts/login/'

    # def get(self, request, *args, **kwargs):
    #     messages.success(request, 'Город успешно удален')
    #     return self.post(request, *args, **kwargs)


class TrainListView(generic.ListView):
    """Обработчик списка поездов."""
    model = Train
    template_name = 'travels/train/train_list.html'
    paginate_by = 5


class TrainCreateView(SuccessMessageMixin, LoginRequiredMixin, generic.CreateView):
    """Обработчик создания поезда."""
    model = Train
    fields = ('name', 'from_city', 'to_city', 'travel_time',)
    template_name = 'travels/train/train_create_form.html'
    success_url = reverse_lazy('travels:train_list')
    success_message = 'Поезд создан!'
    login_url = '/accounts/login/'


class TrainUpdateView(SuccessMessageMixin, LoginRequiredMixin, generic.UpdateView):
    """Обработчик редактирования поезда."""
    model = Train
    fields = ('name', 'from_city', 'to_city', 'travel_time',)
    template_name = 'travels/train/train_update_form.html'
    success_url = reverse_lazy('travels:train_list')
    success_message = 'Поезд отредактирован!'
    login_url = '/accounts/login/'


class TrainDeleteView(SuccessMessageMixin, LoginRequiredMixin, generic.DeleteView):
    """Обработчик удаления поезда."""
    model = Train
    template_name = 'travels/train/train_confirm_delete.html'
    success_url = reverse_lazy('travels:train_list')
    success_message = 'Поезд удален!'
    login_url = '/accounts/login/'
