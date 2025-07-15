from rest_framework import serializers
from .models import News, ArchivedNews

class NewsSerializer(serializers.ModelSerializer):
    featured_image_url = serializers.SerializerMethodField()
    formatted_publish_date = serializers.SerializerMethodField()

    class Meta:
        model = News
        fields = ['id', 'title', 'description', 'featured_image', 'featured_image_url', 
                 'third_party_link', 'publish_date', 'formatted_publish_date', 'archived']

    def get_featured_image_url(self, obj):
        if obj.featured_image:
            return self.context['request'].build_absolute_uri(obj.featured_image.url)
        return None

    def get_formatted_publish_date(self, obj):
        return obj.publish_date.strftime("%B %d, %Y")

class ArchivedNewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArchivedNews
        fields = '__all__'