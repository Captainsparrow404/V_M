from django.urls import path
from . import views

app_name = 'events'

urlpatterns = [
    # Admin preview URL
    path('admin/events/<int:event_id>/preview/', views.preview_event, name='event_preview'),
]