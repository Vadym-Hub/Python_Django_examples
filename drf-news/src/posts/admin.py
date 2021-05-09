from django.contrib import admin

from .models import Post, Comment


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """
    Register base model Post in Django-admin.
    """

    pass


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """
    Register base model Comment in Django-admin.
    """

    pass
