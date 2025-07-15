from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api_views import InvitationViewSet, PersonViewSet, AssignmentViewSet

router = DefaultRouter()
router.register('invitations', InvitationViewSet, basename='invitation-api')
router.register('persons', PersonViewSet, basename='person-api')
router.register('assignments', AssignmentViewSet, basename='assignment-api')

urlpatterns = [
    path('', include(router.urls)),
]