from django.contrib.auth.models import User
from django.db import models


class Post(models.Model):
    """
    Post Model.
    """

    author = models.ForeignKey(User, on_delete=models.CASCADE)
    votes = models.ManyToManyField(User, related_name="votes", blank=True)
    title = models.CharField(max_length=200, unique=True)
    link = models.URLField(max_length=200, unique=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-created",)

    def __str__(self):
        return self.title


class Comment(models.Model):
    """
    Comment Model.
    """

    post = models.ForeignKey(Post, related_name="comments", on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    parent = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="children",
    )
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.author} - {self.post}: {self.content}"
