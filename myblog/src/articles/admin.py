from django.contrib import admin

from .models import Article, Category, Comment


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Отображение категорий"""
    list_display = ('name',)


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    """Отображение статьи в админке"""
    list_display = ('title', 'slug', 'author', 'publish', 'status')
    list_filter = ('status', 'created', 'publish', 'author')
    search_fields = ('title', 'text', 'author__username', 'category')
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ('author',)
    date_hierarchy = 'publish'
    ordering = ['status', 'publish']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """Отображение комментариев в админке"""
    list_display = ('author_name', 'article', 'parent', 'comment_text', 'created')
    list_filter = ('created', 'article')
    search_fields = ('author_name', 'comment_text')
