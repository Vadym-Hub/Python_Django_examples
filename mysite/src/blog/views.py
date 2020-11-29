from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, FormView, DetailView
from django.core.mail import send_mail
from django.db.models import Count
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank

from .models import Post, Comment
from .forms import EmailPostForm, CommentForm, SearchForm


class PostListView(ListView):
    """Обработчик для отображения статьи."""
    model = Post
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'

    def get_queryset(self):
        if self.kwargs:
            return Post.objects.filter(status='published').filter(tags__slug=self.kwargs.get('tag_slug'))
        else:
            return Post.objects.filter(status='published')


def post_detail(request, year, month, day, post):
    """Обработчик для отображения статьи."""
    post = get_object_or_404(Post,
                             slug=post,
                             status='published',
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)
    
    # Список активных комментариев для этой статьи.
    comments = post.comments.filter(active=True)
    new_comment = None

    if request.method == 'POST':
        # Пользователь отправил комментарий.
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # Создаем комментарий, но пока не сохраняем в базе данных.
            new_comment = comment_form.save(commit=False)
            # Привязываем комментарий к текущей статье.
            new_comment.post = post
            # Сохраняем комментарий в базе данных.
            new_comment.save()

    else:
        comment_form = CommentForm()

    # Формирование списка похожих статей.
    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags', '-publish')[:4]

    return render(request, 'blog/post/detail.html', {'post': post,
                                                     'comments': comments,
                                                     'new_comment': new_comment,
                                                     'comment_form': comment_form,
                                                     'similar_posts': similar_posts})


def post_share(request, post_id):
    """Обработчик для отправки статьи по e-mail"""
    # Получение статьи по идентификатору.
    post = get_object_or_404(Post, id=post_id, status='published')
    sent = False 
 
    if request.method == 'POST':
        # Форма была отправлена на сохранение.
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # Все поля формы прошли валидацию.
            cd = form.cleaned_data
            # Отправка электронной почты.
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} ({cd['email']}) рекомендовано к прочтению '{post.title}'"
            message = f'Прочитай "{post.title}" к {post_url}\n\n{cd["name"]}\'s комментарии: {cd["comments"]}'
            send_mail(subject, message, 'admin@myblog.com', [cd['to']])
            sent = True
    else:
        form = EmailPostForm()
    return render(request, 'blog/post/share.html', {'post': post,
                                                    'form': form,
                                                    'sent': sent})





# class PostShareView(FormView):
#     form_class = EmailPostForm
#     template_name = 'blog/post/share.html'
#     success_url = reverse_lazy('blog:contact-us')
#
#     def form_valid(self, form):
#         self.send_mail(form.cleaned_data)
#         return super(PostShareView, self).form_valid(form)
#
#     def form_valid(self, form):
#         cd = form.cleaned_data
#         mail_managers(u"{} {} зарегистрировался(лась) на мероприятие {}"
#                       u"".format(cd["first_name"], cd["last_name"], self.get_object.title)
#         messages.success(self.request, u"Ваша заявка принята")
#         return super(EventView, self).form_valid(form)
#
#
#     def send_mail(self, valid_data):
#         # Send mail logic
#         pass



def post_search(request):
    """Обработчик поиска (только для PostgreSQL)."""
    form = SearchForm()
    query = None
    results = []
    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            search_vector = SearchVector('title', weight='A') + SearchVector('body', weight='B')
            search_query = SearchQuery(query)
            query = form.cleaned_data['query']
            results = Post.objects.annotate(search=search_vector,  rank=SearchRank(search_vector, search_query)
                                            ).filter(rank__gte=0.3).order_by('-rank')
    return render(request, 'blog/post/search.html', {'form': form,
                                                     'query': query,
                                                     'results': results})
