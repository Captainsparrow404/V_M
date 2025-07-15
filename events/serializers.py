from rest_framework import serializers
from .models import Event, EventCategory

class EventCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = EventCategory
        fields = ['id', 'name']

class EventListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = [
            'id',
            'title',
            'short_description',
            'event_date',
            'end_time',
            'location_name',
            'featured_image',
            'is_featured',
        ]

class EventSerializer(serializers.ModelSerializer):
    category = EventCategorySerializer(read_only=True)
    
    class Meta:
        model = Event
        fields = [
            'id',
            'title',
            'slug',
            'category',
            'short_description',
            'description',
            'event_date',
            # 'end_time',
            'location_name',
            # 'address',
            # 'map_embed_url',
            'featured_image',
            'event_video_url',
            'is_published',
            'is_featured',
            'is_archived',
            'created_at',
            'updated_at'
        ]