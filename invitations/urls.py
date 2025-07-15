from django.urls import path
from . import views

app_name = 'invitations'

urlpatterns = [
    path('', views.invitations_list, name='invitations_list'),
    path('add/', views.add_invitation, name='add_invitation'),
    path('persons/', views.persons_list, name='persons_list'),
    path('persons/add/', views.add_person, name='add_person'),
    path('assign/<int:invitation_id>/', views.assign_persons, name='assign_persons'),
    path('ajax/assign/<int:invitation_id>/', views.ajax_assign_persons, name='ajax_assign_persons'),
    path('invitation/<int:invitation_id>/', views.invitation_detail, name='invitation_detail'),
]