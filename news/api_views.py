from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.template.loader import render_to_string
from django.http import HttpResponse
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import News, ArchivedNews
from .serializers import NewsSerializer
import logging

logger = logging.getLogger(__name__)


class NewsAPIViewSet(viewsets.ModelViewSet):
    """
    API endpoints for managing news items.

    This viewset provides CRUD operations for news items along with
    additional actions for preview, archive, and unarchive functionality.
    """
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    permission_classes = [AllowAny]  # Changed to AllowAny for easier testing

    def get_permissions(self):
        """
        Override to allow public access to preview endpoint.
        """
        if self.action in ['preview', 'retrieve', 'list']:
            logger.debug(f"Allowing access to {self.action} without authentication")
            return [AllowAny()]
        return [AllowAny()]  # For now, allowing all actions

    @swagger_auto_schema(
        operation_description="Get a preview of the news item in either HTML or JSON format",
        manual_parameters=[
            openapi.Parameter(
                'format',
                openapi.IN_QUERY,
                description="Response format (html or json)",
                type=openapi.TYPE_STRING,
                enum=['html', 'json']
            )
        ],
        responses={
            200: openapi.Response('Success', NewsSerializer),
            404: 'News item not found',
            500: 'Internal server error'
        }
    )
    @action(detail=True, methods=['get'])
    def preview(self, request, pk=None):
        """
        Get a preview of the news item in either HTML or JSON format.
        Add ?format=html to the URL for HTML format.
        """
        try:
            news = self.get_object()

            # Check if HTML format is explicitly requested
            if request.query_params.get('format') == 'html':
                logger.debug(f"Rendering HTML preview for news ID: {pk}")
                html_content = render_to_string('admin/news/preview.html', {'news': news})
                return HttpResponse(html_content, content_type='text/html')

            serializer = self.get_serializer(news)
            return Response(serializer.data)
        except Exception as e:
            logger.error(f"Error in preview: {str(e)}")
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @swagger_auto_schema(
        operation_description="Delete a news item and create an archive entry",
        responses={
            204: 'News item deleted successfully',
            404: 'News item not found'
        }
    )
    def destroy(self, request, *args, **kwargs):
        """
        Delete a news item and create an archive entry.
        """
        instance = self.get_object()
        ArchivedNews.objects.create(news=instance)
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @swagger_auto_schema(
        operation_description="Archive a news item",
        responses={
            200: openapi.Response('News archived successfully', openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={'status': openapi.Schema(type=openapi.TYPE_STRING)}
            )),
            404: 'News item not found'
        }
    )
    @action(detail=True, methods=['post'])
    def archive(self, request, pk=None):
        """
        Archive a news item.
        POST /api/news/{id}/archive/
        """
        news = self.get_object()
        news.archived = True
        news.save()
        ArchivedNews.objects.get_or_create(news=news)
        return Response({'status': 'archived'})

    @swagger_auto_schema(
        operation_description="Unarchive a news item",
        responses={
            200: openapi.Response('News unarchived successfully', openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={'status': openapi.Schema(type=openapi.TYPE_STRING)}
            )),
            404: 'News item not found'
        }
    )
    @action(detail=True, methods=['post'])
    def unarchive(self, request, pk=None):
        """
        Unarchive a news item.
        POST /api/news/{id}/unarchive/
        """
        news = self.get_object()
        news.archived = False
        news.save()
        ArchivedNews.objects.filter(news=news).delete()
        return Response({'status': 'unarchived'})
