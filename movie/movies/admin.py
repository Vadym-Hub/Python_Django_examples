from django import forms
from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import Category, Genre, Movie, MovieShots, Actor, Rating, RatingStar, Reviews

from ckeditor_uploader.widgets import CKEditorUploadingWidget


class MovieAdminForm(forms.ModelForm):
    description = forms.CharField(label='Опис', widget=CKEditorUploadingWidget())

    class Meta:
        model = Movie
        fields = '__all__'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Категорії"""
    list_display = ('id', 'name', 'url')
    list_display_links = ('name',)


class ReviewInline(admin.TabularInline):
    """Відгуки на сторінці фільму"""
    model = Reviews
    extra = 1
    readonly_fields = ('name', 'email')


class MovieShotsInLine(admin.TabularInline):
    model = MovieShots
    extra = 1
    readonly_fields = ('get_image',)

    def get_image(self, obj):  # вивід кадра в адмінку
        return mark_safe(f'<img src={obj.image.url} width="100" height="110"')

    get_image.short_description = 'Кадр'


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    """Фільми"""
    list_display = ('title', 'category', 'url', 'draft')
    list_filter = ('category', 'year',)
    search_fields = ('title', 'category__name')
    inlines = [MovieShotsInLine, ReviewInline]
    save_on_top = True
    save_as = True
    list_editable = ('draft', )
    actions = ['publish', 'unpublish']
    form = MovieAdminForm
    readonly_fields = ('get_image',)
    fieldsets = (
        (None, {
            'fields': (('title', 'tagline'),)
        }),
        (None, {
            'fields': ('description', ('poster', 'get_image'))
        }),
        (None, {
            'fields': (('year', 'world_premiere', 'country'),)
        }),
        (None, {
            'fields': (('actors', 'directors', 'genres', 'category'),)
        }),
        (None, {
            'fields': (('budget', 'fees_in_usa', 'fees_in_world'),)
        }),
        ('Options', {
            'fields': (('url', 'draft'),)
        }),
    )

    def get_image(self, obj):  # вивід кадра в адмінку
        return mark_safe(f'<img src={obj.poster.url} width="100" height="110"')

    def unpublish(self, request, queryset):
        """Зняти з публікації"""
        row_update = queryset.update(draft=True)
        if row_update == 1:
            message_bit = '1 запис було оновлено'
        else:
            message_bit = f'{row_update} записів було оновлено'
        self.message_user(request, f'{message_bit}')

    def publish(self, request, queryset):
        """Опублікувати"""
        row_update = queryset.update(draft=False)
        if row_update == 1:
            message_bit = '1 запис було оновлено'
        else:
            message_bit = f'{row_update} записів було оновлено'
        self.message_user(request, f'{message_bit}')

    publish.short_description = 'Опублікувати'
    publish.allowed_permissions = ('change', )

    unpublish.short_description = 'Зняти з публікації'
    unpublish.allowed_permission = ('change', )

    get_image.short_description = 'Постер'


@admin.register(Reviews)
class ReviewAdmin(admin.ModelAdmin):
    """Відгуки"""
    list_display = ('name', 'email', 'parent', 'movie', 'id')
    readonly_fields = ('name', 'email')


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    """Жанри"""
    list_display = ('name', 'url')


@admin.register(Actor)
class ActorAdmin(admin.ModelAdmin):
    """Актери та режисери"""
    list_display = ('name', 'age', 'get_image')
    readonly_fields = ('get_image',)

    def get_image(self, obj):  # вивід фотки в адмінку
        return mark_safe(f'<img src={obj.image.url} width="50" height="60"')

    get_image.short_description = 'Изображение'


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    """Рейтинг"""
    list_display = ('movie', 'ip', 'star')


@admin.register(MovieShots)
class MovieShotsAdmin(admin.ModelAdmin):
    """Кадри з фильму"""
    list_display = ('title', 'movie', 'get_image')
    readonly_fields = ('get_image',)

    def get_image(self, obj):  # вивід кадра в адмінку
        return mark_safe(f'<img src={obj.image.url} width="50" height="60"')

    get_image.short_description = 'Зображення'


admin.site.register(RatingStar)

admin.site.site_title = 'Django Movies :-)'
admin.site.site_header = 'Django Movies :-)'
