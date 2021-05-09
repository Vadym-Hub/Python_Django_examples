from celery import shared_task

from .models import Post


@shared_task
def reset_post_votes():
    """
    Function clear votes in Post.
    """
    posts = Post.objects.all()
    for post in posts:
        post.votes.clear()
