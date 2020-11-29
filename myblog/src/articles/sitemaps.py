from django.contrib.sitemaps import Sitemap
from .models import Article


class ArticleSitemap(Sitemap):
    """Объект карты сайта"""
    changefreq = 'weekly'
    priority = 0.9

    def items(self):
        return Article.objects.filter(status='опубликовано')

    def lastmod(self, obj):
        return obj.updated
