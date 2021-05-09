from django.urls import path

from . import views


app_name = 'orders'

urlpatterns = [
    path('', views.OrderCreateView.as_view(), name='order_create'),
    path('list/', views.OrderListView.as_view(), name='order_list'),
    path('error/', views.OrderErrorView.as_view(), name='order_error'),
    path('<int:pk>/', views.OrderDetailView.as_view(), name='order_detail'),
    path('<int:pk>/success/', views.OrderSuccessView.as_view(), name='order_success'),
]
