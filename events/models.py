from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField

class EventCategory(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Event Categories"

class Event(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    category = models.ForeignKey(EventCategory, on_delete=models.SET_NULL, null=True)
    short_description = models.CharField(max_length=300)
    description = RichTextField()
    event_date = models.DateTimeField()
    # end_time = models.DateTimeField(null=True, blank=True)
    location_name = models.CharField(max_length=255)
    # address = models.TextField()
    # map_embed_url = models.URLField(blank=True)
    featured_image = models.ImageField(upload_to='events/')
    event_video_url = models.URLField(blank=True)
    
    is_published = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    is_archived = models.BooleanField(default=False)
    
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-event_date']





