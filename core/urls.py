from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.views.decorators.csrf import csrf_exempt

schema_view = get_schema_view(
    openapi.Info(
        title="Voter Management API",
        default_version='v1',
        description="API Documentation for Voter Management System",
        terms_of_service="https://www.yourapp.com/terms/",
        contact=openapi.Contact(email="contact@yourapp.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
    authentication_classes=[],
)

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),

    # API Documentation
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),

    # API URLs
    path('api/invitations/', include('invitations.api_urls')),
    path('api/news/', include('news.api_urls')),
    path('api/events/', include('events.api.urls')),

    # Web URLs
    path('invitations/', include('invitations.urls', namespace='invitations')),
    path('voters/', include('voters.urls')),
    path('notifications/', include('notifications.urls')),
    path('', include('passes.urls')),
    path('news/', include('news.urls')),
    path('', include('blogs.urls')),
    path('', include('Media_Management.urls')),
    path('events/', include('events.urls')),

    # CKEditor
    path('ckeditor/', include('ckeditor_uploader.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

admin.site.site_header = 'Voter Management System'
admin.site.site_title = 'Voter Management'
admin.site.index_title = 'Welcome to Voter Management System'

# Customize admin site
admin.site.site_header = 'Voter Management System'
admin.site.site_title = 'Voter Management'
admin.site.index_title = 'Welcome to Voter Management System'