from django.contrib import admin
from django.urls import path, reverse
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.shortcuts import redirect, get_object_or_404, render
from django import forms
from ckeditor.widgets import CKEditorWidget
from .models import News, ArchivedNews

class NewsAdminForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorWidget())
    
    class Meta:
        model = News
        fields = '__all__'

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    form = NewsAdminForm
    list_display = ('title', 'formatted_description', 'publish_date', 'is_archived', 'action_buttons')
    search_fields = ('title', 'description')
    actions = ['archive_selected']
    change_list_template = 'admin/news/news_changelist.html'

    def formatted_description(self, obj):
        return mark_safe(f'<div style="max-width: 400px;">{obj.description[:150]}...</div>')
    formatted_description.short_description = 'Description'

    def is_archived(self, obj):
        return obj.archived
    is_archived.boolean = True
    is_archived.short_description = 'Archived'

    def action_buttons(self, obj):
        preview_url = reverse('admin:news_news_preview', args=[obj.pk])
        archive_url = reverse('admin:news_news_archive', args=[obj.pk]) if not obj.archived else reverse('admin:news_news_unarchive', args=[obj.pk])
        archive_label = 'Unarchive' if obj.archived else 'Archive'
        return format_html(
            f'<a class="button" href="{preview_url}" style="background-color: #417690; color: white; padding: 5px 10px; text-decoration: none; margin-right: 5px; border-radius: 3px;">Preview</a>'
            f'<a class="button" href="{reverse("admin:news_news_change", args=[obj.pk])}" style="background-color: #79aec8; color: white; padding: 5px 10px; text-decoration: none; margin-right: 5px; border-radius: 3px;">Edit</a>'
            f'<a class="button" href="{archive_url}" style="background-color: {"#c4c4c4" if obj.archived else "#ba2121"}; color: white; padding: 5px 10px; text-decoration: none; border-radius: 3px;">{archive_label}</a>'
        )
    action_buttons.short_description = 'Actions'

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('news/preview/<int:pk>/', self.admin_site.admin_view(self.preview_news), name='news_news_preview'),
            path('news/archive/<int:pk>/', self.admin_site.admin_view(self.archive_news), name='news_news_archive'),
            path('news/unarchive/<int:pk>/', self.admin_site.admin_view(self.unarchive_news), name='news_news_unarchive'),
        ]
        return custom_urls + urls

    def preview_news(self, request, pk):
        news_item = get_object_or_404(News, pk=pk)
        return render(request, 'admin/news/preview.html', {'news': news_item})

    def archive_news(self, request, pk):
        news = get_object_or_404(News, pk=pk)
        news.archived = True
        news.save()
        ArchivedNews.objects.get_or_create(news=news)
        return redirect('admin:news_news_changelist')

    def unarchive_news(self, request, pk):
        news = get_object_or_404(News, pk=pk)
        news.archived = False
        news.save()
        ArchivedNews.objects.filter(news=news).delete()
        return redirect('admin:news_news_changelist')

    def archive_selected(self, request, queryset):
        for news in queryset:
            news.archived = True
            news.save()
            ArchivedNews.objects.get_or_create(news=news)
        self.message_user(request, f"{queryset.count()} news item(s) archived.")
    archive_selected.short_description = "Archive selected news"

@admin.register(ArchivedNews)
class ArchivedNewsAdmin(admin.ModelAdmin):
    list_display = ('news', 'archived_at')
