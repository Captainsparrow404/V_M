from django import forms
from django.forms.models import BaseInlineFormSet
from .models import Invitation, Person, Assignment

class InvitationForm(forms.ModelForm):
    class Meta:
        model = Invitation
        fields = ['name', 'mobile_number', 'mandal', 'address_venue', 'area', 'file_upload']

class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = ['name', 'phone_number', 'email', 'address', 'assembly', 'mandal', 'area']

class AssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ['person', 'is_gift_handler']

class BaseAssignmentFormSet(BaseInlineFormSet):
    def clean(self):
        super().clean()
        # Add any custom formset cleaning here if needed
        pass 