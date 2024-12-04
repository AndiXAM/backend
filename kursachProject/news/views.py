from django.shortcuts import render, get_object_or_404
from .models import NewsArticle


def news_list(request):
    articles = NewsArticle.objects.all().order_by('-published_date')
    return render(request, 'news/news_list.html', {'articles': articles})

def news_detail(request, article_id):
    article = get_object_or_404(NewsArticle, id=article_id)
    return render(request, 'news/news_detail.html', {'article': article})