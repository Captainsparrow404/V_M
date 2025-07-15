from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from django.shortcuts import render, get_object_or_404
from django.conf import settings
from ..models import Blog
from .serializers import BlogSerializer, BlogListSerializer

class BlogViewSet(viewsets.ModelViewSet):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    permission_classes = []
    lookup_field = 'pk'

    def get_serializer_context(self):
        """
        Add request to serializer context to generate proper URLs
        """
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

    def get_serializer_class(self):
        if self.action == 'list':
            return BlogListSerializer
        return BlogSerializer

    def perform_create(self, serializer):
        serializer.save(
            created_at=timezone.now()
        )

    def get_queryset(self):
        queryset = Blog.objects.all().order_by('-created_at')
        status_param = self.request.query_params.get('status', None)
        category = self.request.query_params.get('category', None)

        if status_param:
            queryset = queryset.filter(status=status_param)
        if category:
            queryset = queryset.filter(category=category)

        return queryset

    def retrieve(self, request, *args, **kwargs):
        """
        Override retrieve to handle errors gracefully
        """
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        except Blog.DoesNotExist:
            return Response(
                {'error': 'Blog post not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=True, methods=['post'])
    def archive(self, request, pk=None):
        blog = self.get_object()
        blog.status = 'archived'
        blog.save()
        return Response({
            'status': 'success',
            'message': 'Blog archived successfully'
        })

    @action(detail=True, methods=['post'])
    def publish(self, request, pk=None):
        blog = self.get_object()
        blog.status = 'published'
        blog.save()
        return Response({
            'status': 'success',
            'message': 'Blog published successfully'
        })

    @action(detail=True, methods=['get'])
    def preview(self, request, pk=None):
        blog = self.get_object()
        serializer = self.get_serializer(blog)
        return Response(serializer.data)