from django.db.models import Count
from rest_framework import viewsets
from rest_framework.authentication import BasicAuthentication
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from .models import Post, Comment
from .permissions import IsOwnerOrReadOnly
from .serializers import PostSerializer, CommentSerializer


class PostViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to
    create, read, update, delete post
    end vote for post.
    """

    queryset = Post.objects.all().annotate(count_votes=Count("votes"))
    serializer_class = PostSerializer
    permission_classes = (IsOwnerOrReadOnly, IsAuthenticatedOrReadOnly)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(
        detail=True,
        methods=["post"],
        authentication_classes=[BasicAuthentication],
        permission_classes=[IsAuthenticated],
    )
    def upvote(self, request, *args, **kwargs):
        """
        Method allows users to vote for a post.
        """
        post = self.get_object()
        if post.votes.filter(id=self.request.user.id).exists():
            post.votes.remove(self.request.user)
            return Response(status=201)
        post.votes.add(self.request.user)
        return Response(status=201)


class CommentViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to
    Create, read, update and delete a comment.
    """

    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
    permission_classes = (IsOwnerOrReadOnly, IsAuthenticatedOrReadOnly)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
