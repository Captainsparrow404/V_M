from django.urls import path
from . import views

app_name = 'events_api'

urlpatterns = [
    path('events/', views.EventListAPIView.as_view(), name='event-list'),
    path('events/<slug:slug>/', views.EventDetailAPIView.as_view(), name='event-detail'),
    path('events/upcoming/', views.UpcomingEventsAPIView.as_view(), name='upcoming-events'),
    path('events/past/', views.PastEventsAPIView.as_view(), name='past-events'),
    path('categories/', views.EventCategoryListAPIView.as_view(), name='category-list'),
    path('categories/<int:category_id>/events/', views.EventsByCategoryAPIView.as_view(), name='category-events'),
] 