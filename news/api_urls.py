from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api_views import NewsAPIViewSet

# Create router and register viewsets
router = DefaultRouter()
router.register(r'', NewsAPIViewSet, basename='news')

# Define the URL patterns
urlpatterns = [
    path('', include(router.urls)),
]
