from django import forms
from .models import Comment


class CommentForm(forms.ModelForm):
    """Форма комментария к статье"""
    class Meta:
        model = Comment
        fields = ('author_name', 'comment_text', 'parent')


class EmailArticleForm(forms.Form):
    """Форма отправки статьи на e-mail"""
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    comments = forms.CharField(required=False, widget=forms.Textarea)


class SearchForm(forms.Form):
    """рма для поиска"""
    query = forms.CharField()
