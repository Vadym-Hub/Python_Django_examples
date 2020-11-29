from django.urls import path

from . import views
from .feeds import LatestArticlesFeed

app_name = 'articles'

urlpatterns = [
    path('', views.ArticlesListView.as_view(), name='article_list'),
    path('<int:year>/<int:month>/<int:day>/<slug:slug>/', views.ArticleDetailView.as_view(), name='article_detail'),
    path("review/<int:pk>/", views.AddReview.as_view(), name='add_comment'),
    path('<int:article_id>/share/', views.article_share, name='article_share'),
    path('feed/', LatestArticlesFeed(), name='article_feed'),
    path('search/', views.article_search, name='article_search'),
]
