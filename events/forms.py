
from django import forms
from ckeditor.widgets import CKEditorWidget
from .models import Event

class EventForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = Event
        fields = '__all__'