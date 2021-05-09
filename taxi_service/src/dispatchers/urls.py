from django.urls import path, include

from . import views

app_name = 'dispatchers'

urlpatterns = [
    # Базовые URLs авторизации (путь: from django.contrib.auth.urls).
    path('', include('django.contrib.auth.urls')),
    # URL регистрации пользователя.
    path('signup/', views.UserSignupView.as_view(), name='signup'),
    # URL списка машин.
    path('cars/', views.CarListView.as_view(), name='car_list'),
]
