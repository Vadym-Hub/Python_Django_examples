from django.urls import path

from . import views


app_name = 'travels'

urlpatterns = [
    # URLS городов.
    path('city/update/<int:pk>/', views.CityUpdateView.as_view(), name='city_update'),
    path('city/delete/<int:pk>/', views.CityDeleteView.as_view(), name='city_delete'),
    path('city/create/', views.CityCreateView.as_view(), name='city_create'),
    path('city/', views.CityListView.as_view(), name='city_list'),
    # URLS поездов.
    path('train/update/<int:pk>/', views.TrainUpdateView.as_view(), name='train_update'),
    path('train/delete/<int:pk>/', views.TrainDeleteView.as_view(), name='train_delete'),
    path('train/create/', views.TrainCreateView.as_view(), name='train_create'),
    path('train/', views.TrainListView.as_view(), name='train_list'),
    # URLS маршрутов.
    path('route/save_route/', views.save_route, name='route_save'),
    path('route/find_route/', views.find_route, name='route_find'),
    path('route/create_route/', views.add_route, name='route_create'),
    path('route/', views.RouteListView.as_view(), name='route_list'),
    path('route/detail/<int:pk>/', views.RouteDetailView.as_view(), name='route_detail'),
    path('route/delete/<int:pk>/', views.RouteDeleteView.as_view(), name='route_delete'),

    path('', views.home, name='home'),
]
