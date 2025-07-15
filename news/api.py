# news/api.py

from rest_framework import viewsets
from .models import News
from .serializers import NewsSerializer
from rest_framework.permissions import IsAuthenticated

class NewsViewSet(viewsets.ModelViewSet):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    permission_classes = [IsAuthenticated]
