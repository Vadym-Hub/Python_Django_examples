from rest_framework import serializers

from .models import Post, Comment


class RecursiveSerializer(serializers.Serializer):
    """
    Serializer for recursive output comments in comments.
    """

    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data


class CommentSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for comments.
    """

    author = serializers.SlugRelatedField(slug_field="username", read_only=True)
    children = RecursiveSerializer(many=True)

    class Meta:
        model = Comment
        fields = ("id", "author", "content", "children")


class PostSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for posts.
    """

    author = serializers.SlugRelatedField(slug_field="username", read_only=True)
    comments = CommentSerializer(many=True)
    count_votes = serializers.IntegerField(read_only=True)

    class Meta:
        model = Post
        exclude = ("votes",)
