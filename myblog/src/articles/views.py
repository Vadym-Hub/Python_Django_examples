from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from django.core.mail import send_mail
from django.shortcuts import redirect, get_object_or_404, render
from django.views import generic
from django.views.generic.base import View

from .models import Article
from .forms import CommentForm, EmailArticleForm, SearchForm


class ArticlesListView(generic.ListView):
    """Вывод списка статей"""
    model = Article
    queryset = Article.objects.filter(status='опубликовано')
    paginate_by = 4


class ArticleDetailView(generic.DetailView):
    """Вывод одной статьи"""
    model = Article
    queryset = Article.objects.filter(status='опубликовано')


class AddReview(View):
    """Добавление комментария"""

    def post(self, request, pk):
        form = CommentForm(request.POST)
        article = Article.objects.get(id=pk)
        if form.is_valid():
            form = form.save(commit=False)
            if request.POST.get('parent', None):
                form.parent_id = int(request.POST.get('parent'))
            form.article = article
            form.save()
        return redirect(article.get_absolute_url())


def article_share(request, article_id):
    # Получение статьи по идентификатору.
    article = get_object_or_404(Article, id=article_id, status='опубликовано')
    sent = False
    if request.method == 'POST':
        # Форма была отправлена на сохранение.
        form = EmailArticleForm(request.POST)
        if form.is_valid():
            # Все поля формы прошли валидацию.
            cd = form.cleaned_data
            # Отправка электронной почты.
            article_url = request.build_absolute_uri(article.get_absolute_url())
            subject = f"{cd['name']} рекомендовал к прочтению '{article.title}'"
            message = f"Прочитай '{article.title}' по {article_url}\n\n{cd['name']}\'s коментарии: {cd['comments']}"
            send_mail(subject, message, 'test@gmail.com', [cd['email']])
            sent = True
    else:
        form = EmailArticleForm()
    return render(request, 'articles/article_share.html', {'article': article,
                                                           'form': form,
                                                           'sent': sent})


def article_search(request):
    """Функция обработки поиска(работает только с PostgreSQL)"""
    form = SearchForm()
    query = None
    results = []
    if 'query' in request.GET:
        form = SearchForm(request.GET)
    if form.is_valid():
        query = form.cleaned_data['query']
        search_vector = SearchVector('title', weight='A') + SearchVector('text', weight='B')
        search_query = SearchQuery(query)
        results = Article.objects.annotate(
            search=search_vector, rank=SearchRank(search_vector, search_query)).filter(
            rank__gte=0.3).order_by('-rank')
    return render(request, 'articles/article_search.html', {'form': form,
                                                            'query': query,
                                                            'results': results})
