from django import forms
from .models import Pass
from django.utils import timezone
from django.core.exceptions import ValidationError



class PassRequestForm(forms.ModelForm):
    class Meta:
        model = Pass
        fields = [
            'name',
            'email',
            'phone',
            'temple',
            'num_persons',
            'visit_date',
            'accommodation_date',
            'darshan_date',
            'darshan_type',
            'id_proof_type',
            'id_proof_number'
        ]
        widgets = {
            'visit_date': forms.DateInput(attrs={
                'type': 'date',
                'min': timezone.now().date().isoformat(),
            }),
            'accommodation_date': forms.DateInput(attrs={'type': 'date'}),
            'darshan_date': forms.DateInput(attrs={'type': 'date'}),
            'phone': forms.TextInput(attrs={
                'pattern': '[0-9]{10}',
                'title': 'Enter 10 digit mobile number'
            }),
            'darshan_type': forms.Select(attrs={'disabled': 'disabled'})  # User cannot edit
        }

    def clean(self):
        cleaned_data = super().clean()
        temple = cleaned_data.get('temple')
        num_persons = cleaned_data.get('num_persons')
        visit_date = cleaned_data.get('visit_date')

        if temple == 'Tirumala Tirupati Devasthanam':
            if num_persons is not None:
                if num_persons < 1 or num_persons > 6:
                    raise ValidationError({
                        'num_persons': 'For Tirumala Tirupati Devasthanam, number of persons must be between 1 and 6'
                    })

            # Check for existing approved pass
            if visit_date:
                existing_pass = Pass.objects.filter(
                    temple=temple,
                    visit_date=visit_date,
                    status='APPROVED'
                ).exists()

                if existing_pass:
                    raise ValidationError({
                        'visit_date': 'An approved pass already exists for Tirumala Tirupati Devasthanam on this date'
                    })
        else:
            # Only validate that number of persons is at least 1 for other temples
            if num_persons is not None and num_persons < 1:
                raise ValidationError({
                    'num_persons': 'Number of persons must be at least 1'
                })

        return cleaned_data

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set base validation for num_persons
        self.fields['num_persons'].widget = forms.NumberInput(attrs={
            'min': '1',
            'title': 'Number of persons must be at least 1'
        })

        # Set ID proof type to Aadhar Card only
        self.fields['id_proof_type'].choices = [('AADHAR', 'Aadhar Card')]
        self.fields['id_proof_type'].initial = 'AADHAR'

        self.fields['darshan_type'].required = False
        self.fields['darshan_type'].widget.attrs['disabled'] = 'disabled'

    def clean_id_proof_number(self):
        id_proof_number = self.cleaned_data.get('id_proof_number')
        if not id_proof_number.isdigit() or len(id_proof_number) != 12:
            raise forms.ValidationError('Please enter a valid 12-digit Aadhar number')
        return id_proof_number

    def clean_visit_date(self):
        visit_date = self.cleaned_data.get('visit_date')
        if visit_date and visit_date < timezone.now().date():
            raise forms.ValidationError("Visit date cannot be in the past!")
        return visit_date

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if not phone.isdigit() or len(phone) != 10:
            raise forms.ValidationError("Please enter a valid 10-digit phone number!")
        return phone

    # def clean_num_persons(self):
    #     num_persons = self.cleaned_data.get('num_persons')
    #     if num_persons is not None:
    #         if num_persons < 1:
    #             raise forms.ValidationError("Number of persons must be at least 1!")
    #         if num_persons > 6:
    #             raise forms.ValidationError("Maximum 6 persons allowed per pass!")
    #     return num_persons