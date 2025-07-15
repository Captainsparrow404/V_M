from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import Invitation, Person, Assignment
from .serializers import InvitationSerializer, PersonSerializer, AssignmentSerializer

class InvitationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing invitations.
    """
    queryset = Invitation.objects.all()
    serializer_class = InvitationSerializer
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_summary="List invitations",
        operation_description="Get a list of all invitations"
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Create invitation",
        operation_description="Create a new invitation"
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Get invitation details",
        operation_description="Get details of a specific invitation"
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Update invitation",
        operation_description="Update an existing invitation"
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Delete invitation",
        operation_description="Delete an invitation"
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

class PersonViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing persons.
    """
    queryset = Person.objects.all()
    serializer_class = PersonSerializer
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_summary="List persons",
        operation_description="Get a list of all persons"
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

class AssignmentViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing assignments.
    """
    queryset = Assignment.objects.all()
    serializer_class = AssignmentSerializer
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_summary="List assignments",
        operation_description="Get a list of all assignments"
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)