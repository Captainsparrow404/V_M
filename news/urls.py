from django.urls import path
from .views import NewsFormView, preview_news, archive_news, unarchive_news

urlpatterns = [
    path('', NewsFormView.as_view(), name='news_form'),
    path('preview/<int:pk>/', preview_news, name='preview_news'),
    path('archive/<int:pk>/', archive_news, name='archive_news'),
    path('unarchive/<int:pk>/', unarchive_news, name='unarchive_news'),
]
