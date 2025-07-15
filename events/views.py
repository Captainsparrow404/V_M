from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework import generics, permissions, filters
from django.utils.timezone import now
from .models import Event, EventCategory
from .serializers import EventSerializer, EventCategorySerializer
from django.shortcuts import get_object_or_404, render
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse, JsonResponse
from django.template.loader import render_to_string
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

class EventListView(ListView):
    model = Event
    template_name = 'events/event_list.html'
    context_object_name = 'events'
    
    def get_queryset(self):
        return Event.objects.filter(is_published=True, is_archived=False).order_by('-event_date')

class EventDetailView(DetailView):
    model = Event
    template_name = 'events/event_detail.html'
    context_object_name = 'event'

class EventCreateView(LoginRequiredMixin, CreateView):
    model = Event
    template_name = 'events/event_form.html'
    fields = ['title', 'category', 'description', 'event_date', 'end_time', 
              'location_name', 'address', 'map_embed_url', 'featured_image', 
              'event_video_url', 'is_published', 'is_featured']
    success_url = reverse_lazy('event_list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

class EventUpdateView(LoginRequiredMixin, UpdateView):
    model = Event
    template_name = 'events/event_form.html'
    fields = ['title', 'category', 'description', 'event_date', 'end_time', 
              'location_name', 'address', 'map_embed_url', 'featured_image', 
              'event_video_url', 'is_published', 'is_featured']
    success_url = reverse_lazy('event_list')

class EventDeleteView(LoginRequiredMixin, DeleteView):
    model = Event
    template_name = 'events/event_confirm_delete.html'
    success_url = reverse_lazy('event_list')

def event_detail_view(request, pk):
    event = get_object_or_404(Event, pk=pk)
    return render(request, 'events/event_detail.html', {'event': event})

class UpcomingEventsAPIView(generics.ListAPIView):
    serializer_class = EventSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        queryset = Event.objects.filter(event_date__gte=now(), is_published=True, is_archived=False).order_by(
            'event_date')
        is_featured = self.request.query_params.get('is_featured')
        category_id = self.request.query_params.get('category')
        if is_featured:
            queryset = queryset.filter(is_featured=is_featured.lower() == 'true')
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        return queryset

class PastEventsAPIView(generics.ListAPIView):
    serializer_class = EventSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        return Event.objects.filter(event_date__lt=now(), is_published=True).order_by('-event_date')

class EventsByCategoryAPIView(generics.ListAPIView):
    serializer_class = EventSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        category_id = self.kwargs.get("category_id")
        return Event.objects.filter(category_id=category_id, is_published=True).order_by('-event_date')

class EventPreviewAPIView(APIView):
    def get(self, request, pk):
        event = get_object_or_404(Event, pk=pk)
        serializer = EventSerializer(event)
        return Response(serializer.data)

class ArchiveEventAPIView(APIView):
    def post(self, request, pk):
        event = get_object_or_404(Event, pk=pk)
        event.is_archived = True
        event.save()
        return Response({'status': 'archived'}, status=status.HTTP_200_OK)

@staff_member_required
def preview_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    return render(request, 'admin/events/event_preview.html', {'event': event})

