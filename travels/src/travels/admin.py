from django.contrib import admin

from .models import City, Route, Train


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    """Города в админке."""
    pass


@admin.register(Train)
class TrainAdmin(admin.ModelAdmin):
    """Поезда в админке."""
    list_display = ('name', 'from_city', 'to_city', 'travel_time')
    list_editable = ['travel_time']


@admin.register(Route)
class RouteAdmin(admin.ModelAdmin):
    """Маршруты в админке."""
    list_display = ('id', 'name', 'from_city', 'to_city', 'travel_times')
    list_editable = ['name']
