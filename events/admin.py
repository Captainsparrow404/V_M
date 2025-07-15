from django.contrib import admin
from django.utils.html import format_html
from django.urls import path, reverse
from django.template.response import TemplateResponse
from django.http import HttpResponseRedirect
from .models import Event, EventCategory
from django import forms
from ckeditor.widgets import CKEditorWidget

class EventAdminForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorWidget())
    
    class Meta:
        model = Event
        fields = '__all__'

class NoRightSideFilterAdmin(admin.ModelAdmin):
    """Custom ModelAdmin that removes right-side filters"""
    
    def changelist_view(self, request, extra_context=None):
        # Get the original response
        response = super().changelist_view(request, extra_context)
        
        # Check if the response has a context data attribute
        if hasattr(response, 'context_data'):
            # Remove filter_specs from the response context
            response.context_data['filter_specs'] = []
            
        return response

@admin.register(Event)
class EventAdmin(NoRightSideFilterAdmin):
    form = EventAdminForm
    list_display = ('title', 'event_date', 'location_name', 'is_featured', 'action_buttons')
    search_fields = ('title', 'description', 'location_name')
    list_filter = ('event_date', 'is_featured', 'is_published', 'is_archived')
    date_hierarchy = 'event_date'
    list_filter_position = 'top'
    
    def get_changelist_template(self):
        return 'admin/events/event_changelist.html'
    
    def action_buttons(self, obj):
        preview_url = reverse('admin:event-preview', args=[obj.id])
        edit_url = reverse('admin:events_event_change', args=[obj.id])
        archive_url = reverse('admin:event-archive', args=[obj.id])
        
        archive_text = 'Unarchive' if obj.is_archived else 'Archive'
        archive_style = 'background: #dc3545;' if not obj.is_archived else 'background: #28a745;'
        
        return format_html(
            '<div style="display: flex; gap: 10px;">'
            '<a href="{}" class="button" target="_blank" style="background: #417690; color: white; padding: 5px 10px; text-decoration: none; border-radius: 4px;">Preview</a>'
            '<a href="{}" class="button" style="background: #79aec8; color: white; padding: 5px 10px; text-decoration: none; border-radius: 4px;">Edit</a>'
            '<a href="{}" class="button" style="{}; color: white; padding: 5px 10px; text-decoration: none; border-radius: 4px;">{}</a>'
            '</div>',
            preview_url,
            edit_url,
            archive_url,
            archive_style,
            archive_text
        )
    action_buttons.short_description = 'Actions'
    action_buttons.allow_tags = True

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                '<int:event_id>/preview/',
                self.admin_site.admin_view(self.preview_view),
                name='event-preview',
            ),
            path(
                '<int:event_id>/archive/',
                self.admin_site.admin_view(self.archive_view),
                name='event-archive',
            ),
        ]
        return custom_urls + urls
    
    def archive_view(self, request, event_id):
        event = Event.objects.get(pk=event_id)
        event.is_archived = not event.is_archived
        event.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    
    def preview_view(self, request, event_id):
        event = Event.objects.get(pk=event_id)
        context = {
            'event': event,
            'title': f'Preview: {event.title}',
            'is_popup': '_popup' in request.GET,
            'has_permission': True,
            'site_header': self.admin_site.site_header,
            'site_title': self.admin_site.site_title,
            'opts': self.model._meta
        }
        return TemplateResponse(request, 'admin/events/event_preview.html', context)

    class Media:
        css = {
            'all': ('admin/css/custom_admin.css',)
        }
        js = ('admin/js/custom_admin.js',)

@admin.register(EventCategory)
class EventCategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']