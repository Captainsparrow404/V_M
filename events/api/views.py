from rest_framework import generics, permissions, filters
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils.timezone import now
from ..models import Event, EventCategory
from ..serializers import EventSerializer, EventCategorySerializer

class EventListAPIView(generics.ListAPIView):
    serializer_class = EventSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'description', 'location_name']
    ordering_fields = ['event_date', 'created_at']

    def get_queryset(self):
        queryset = Event.objects.filter(is_published=True)
        category = self.request.query_params.get('category', None)
        is_featured = self.request.query_params.get('featured', None)
        is_archived = self.request.query_params.get('archived', None)

        if category:
            queryset = queryset.filter(category_id=category)
        if is_featured:
            queryset = queryset.filter(is_featured=is_featured.lower() == 'true')
        if is_archived:
            queryset = queryset.filter(is_archived=is_archived.lower() == 'true')

        return queryset.order_by('-event_date')

class EventDetailAPIView(generics.RetrieveAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = 'slug'

class UpcomingEventsAPIView(generics.ListAPIView):
    serializer_class = EventSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        return Event.objects.filter(
            event_date__gte=now(),
            is_published=True,
            is_archived=False
        ).order_by('event_date')

class PastEventsAPIView(generics.ListAPIView):
    serializer_class = EventSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        return Event.objects.filter(
            event_date__lt=now(),
            is_published=True
        ).order_by('-event_date')

class EventCategoryListAPIView(generics.ListAPIView):
    queryset = EventCategory.objects.all()
    serializer_class = EventCategorySerializer
    permission_classes = [permissions.AllowAny]

class EventsByCategoryAPIView(generics.ListAPIView):
    serializer_class = EventSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        category_id = self.kwargs.get('category_id')
        return Event.objects.filter(
            category_id=category_id,
            is_published=True
        ).order_by('-event_date')