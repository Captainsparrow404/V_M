from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.contrib import messages
from .models import News, ArchivedNews

class NewsFormView(View):
    """Web view for news submission form"""
    def get(self, request):
        return render(request, 'news/news_form.html')

    def post(self, request):
        title = request.POST.get('title')
        description = request.POST.get('description')
        publish_date = request.POST.get('publish_date')
        image = request.FILES.get('image')
        third_party_link = request.POST.get('third_party_link')

        News.objects.create(
            title=title,
            description=description,
            publish_date=publish_date,
            featured_image=image,
            third_party_link=third_party_link
        )
        messages.success(request, 'News submitted successfully.')
        return redirect('/')

def preview_news(request, pk):
    """Web view for public news preview"""
    news = get_object_or_404(News, pk=pk)
    return render(request, "news/preview.html", {"news": news})

def archive_news(request, pk):
    """Web view for archiving news"""
    news = get_object_or_404(News, pk=pk)
    news.archived = True
    news.save()
    ArchivedNews.objects.get_or_create(news=news)
    messages.success(request, 'News archived successfully.')
    return redirect('/admin/news/news/')

def unarchive_news(request, pk):
    """Web view for unarchiving news"""
    news = get_object_or_404(News, pk=pk)
    news.archived = False
    news.save()
    ArchivedNews.objects.filter(news=news).delete()
    messages.success(request, 'News unarchived successfully.')
    return redirect('/admin/news/news/')
