from django.contrib import admin
from .models import Invitation, Person, Assignment
from django.urls import path, reverse
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.shortcuts import redirect, get_object_or_404, render
from django import forms
from django.forms.models import BaseInlineFormSet
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.forms import Media # Import Media
from django.db.models import Q, Prefetch # Import Prefetch

# Enforce only one gift handler per invitation
class AssignmentInlineFormset(BaseInlineFormSet):
    def clean(self):
        super().clean()
        # Check if at least one person is marked as is_gift_handler
        gift_handler_count = sum([form.cleaned_data.get('is_gift_handler', False) for form in self.forms if form.cleaned_data])
        if self.forms and gift_handler_count > 1:
             raise forms.ValidationError("You can select at most one person as a gift handler.")
        # Additional check: Ensure that if is_gift_handler is true, the person is also selected
        for form in self.forms:
            if form.cleaned_data.get('is_gift_handler') and not form.cleaned_data.get('person'):
                 raise forms.ValidationError("Gift handler must be a selected person.")

# Inline editing inside Invitation page
class AssignmentInline(admin.TabularInline):
    model = Assignment
    extra = 1
    fields = ('person', 'is_gift_handler')
    autocomplete_fields = ['person']
    formset = AssignmentInlineFormset  # Apply custom validation

@admin.register(Invitation)
class InvitationAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'name', 'invitation_type', 'event_date', 'mobile_number', 'mandal',
        'address_venue', 'area', 'file_upload', 'created_at', 'assign_button',
        'edit_link'
    )
    search_fields = ('name', 'mobile_number', 'mandal', 'area')
    list_filter = ('invitation_type', 'mandal', 'area')
    inlines = [AssignmentInline]
    change_list_template = 'admin/invitations/invitation/change_list.html'
    fields = ('name', 'invitation_type', 'event_date', 'mobile_number', 'mandal', 'address_venue', 'area', 'file_upload')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        
        # Get filter values from request
        mandal = request.GET.get('mandal', None) # Use None as default to check if parameter is present
        area = request.GET.get('area', None)   # Use None as default to check if parameter is present

        # Debugging print statements
        print(f"DEBUG: InvitationAdmin get_queryset - Received mandal: '{mandal}', type: {type(mandal)}, present in GET: {'mandal' in request.GET}")
        print(f"DEBUG: InvitationAdmin get_queryset - Received area: '{area}', type: {type(area)}, present in GET: {'area' in request.GET}")

        # Apply filters only if the parameter is present in GET and has a non-empty, non-'All' value
        if mandal is not None and mandal.strip() and mandal != 'All':
            print(f"DEBUG: InvitationAdmin get_queryset - Applying mandal filter: {mandal}")
            qs = qs.filter(mandal=mandal)
        else:
            print("DEBUG: InvitationAdmin get_queryset - Not applying mandal filter for value:", mandal)

        if area is not None and area.strip() and area != 'All':
            print(f"DEBUG: InvitationAdmin get_queryset - Applying area filter: {area}")
            qs = qs.filter(area=area)
        else:
            print("DEBUG: InvitationAdmin get_queryset - Not applying area filter for value:", area)

        print(f"DEBUG: InvitationAdmin get_queryset - Final queryset count: {qs.count()}")

        return qs

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}

        # Get unique values for horizontal filters from Invitations
        mandals = Invitation.objects.values_list('mandal', flat=True).distinct().order_by('mandal')
        areas = Invitation.objects.values_list('area', flat=True).distinct().order_by('area')

        extra_context['horizontal_filters'] = {
            'mandals': mandals,
            'areas': areas,
            'current_mandal': request.GET.get('mandal', ''),
            'current_area': request.GET.get('area', ''),
        }

        return super().changelist_view(request, extra_context=extra_context)

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('add/', self.admin_site.admin_view(self.add_view), name='invitations_invitation_add'),
            path('<int:invitation_id>/assign/', self.admin_site.admin_view(render), kwargs={'template_name': 'invitations/assign_persons.html'}),
            path('<int:invitation_id>/detail/', self.admin_site.admin_view(render), kwargs={'template_name': 'invitations/invitation_detail.html'}),
            path('<int:invitation_id>/assign_persons/', self.admin_site.admin_view(self.assign_persons_view), name='invitations_invitation_assign_persons'),
            path('<int:invitation_id>/detail/', self.admin_site.admin_view(self.invitation_detail_view), name='invitations_invitation_detail'),
            path('<int:invitation_id>/ajax_assign_persons/', self.admin_site.admin_view(self.ajax_assign_persons_view), name='invitations_invitation_ajax_assign_persons'),
            path('assign-form/<int:pk>/', self.admin_site.admin_view(self.assign_form_view), name='invitations_invitation_assign_form'),
            path('submit-assignment/<int:pk>/', self.admin_site.admin_view(self.submit_assignment), name='invitations_invitation_submit_assignment'),
        ]
        return custom_urls + urls

    def assign_button(self, obj):
        return format_html(
            '<button type="button" class="button assign-btn" data-id="{}">Assign</button>',
            obj.id
        )
    assign_button.short_description = 'Action'

    def edit_link(self, obj):
        return format_html(
            '<a href="{}">Edit</a>',
            reverse('admin:%s_%s_change' % (self.model._meta.app_label, self.model._meta.model_name), args=[obj.id])
        )
    edit_link.short_description = 'Edit'

    def assign_persons_view(self, request, invitation_id):
        from invitations.views import assign_persons
        return assign_persons(request, invitation_id)

    def invitation_detail_view(self, request, invitation_id):
        from invitations.views import invitation_detail
        return invitation_detail(request, invitation_id)

    def ajax_assign_persons_view(self, request, invitation_id):
        from invitations.views import ajax_assign_persons
        return ajax_assign_persons(request, invitation_id)

    def assign_form_view(self, request, pk):
        invitation = get_object_or_404(Invitation, pk=pk)
        # Fetch all persons for now, dynamic filtering will be done via JS
        persons = Person.objects.all().order_by('name')
        return render(request, 'admin/invitations/assign_form.html', {
            'invitation': invitation,
            'persons': persons,
            'mandals': sorted(list(Person.objects.values_list('mandal', flat=True).distinct())),
            'areas': sorted(list(Person.objects.values_list('area', flat=True).distinct())),
        })

    def submit_assignment(self, request, pk):
        invitation = get_object_or_404(Invitation, pk=pk)
        if request.method == 'POST':
            person_ids = request.POST.getlist('persons[]')
            gift_handler_id = request.POST.get('gift_handler')

            # Basic validation: Check if gift_handler_id is in selected person_ids (optional but good practice)
            if gift_handler_id and gift_handler_id not in person_ids:
                 return JsonResponse({'success': False, 'error': 'Gift handler must be one of the selected persons.'}, status=400)

            # Remove existing assignments for this invitation
            Assignment.objects.filter(invitation=invitation).delete()

            # Create new assignments
            for person_id in person_ids:
                Assignment.objects.create(
                    invitation=invitation,
                    person_id=person_id,
                    is_gift_handler=(str(person_id) == gift_handler_id)
                )

            return JsonResponse({'success': True, 'message': 'Assignments saved successfully!'})
        return JsonResponse({'success': False, 'error': 'Invalid request method.'}, status=405)

    # Use Media class to include the custom JS file
    class Media:
        js = (
            'invitations/js/assign_modal.js',
        )

@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'phone_number', 'email', 'address', 'assembly', 'mandal', 'area')
    search_fields = ('name', 'phone_number', 'email', 'assembly', 'mandal', 'area')
    list_filter = ('assembly', 'mandal', 'area')
    change_list_template = 'admin/invitations/person/change_list.html'

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        
        # Get filter values from request
        assembly = request.GET.get('assembly', '')
        mandal = request.GET.get('mandal', '')
        area = request.GET.get('area', '')

        # Debugging print statements
        print(f"DEBUG: PersonAdmin get_queryset - assembly: {assembly}, mandal: {mandal}, area: {area}")

        # Apply filters only if they have non-empty values
        if assembly and assembly != 'All':
            qs = qs.filter(assembly=assembly)
        if mandal and mandal != 'All':
            qs = qs.filter(mandal=mandal)
        if area and area != 'All':
            qs = qs.filter(area=area)

        return qs

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}

        # Get unique values for horizontal filters
        assemblies = Person.objects.values_list('assembly', flat=True).distinct().order_by('assembly')
        mandals = Person.objects.values_list('mandal', flat=True).distinct().order_by('mandal')
        areas = Person.objects.values_list('area', flat=True).distinct().order_by('area')

        extra_context['horizontal_filters'] = {
            'assemblies': assemblies,
            'mandals': mandals,
            'areas': areas,
            'current_assembly': request.GET.get('assembly', ''),
            'current_mandal': request.GET.get('mandal', ''),
            'current_area': request.GET.get('area', ''),
        }

        return super().changelist_view(request, extra_context=extra_context)

@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ('invitation', 'person', 'is_gift_handler')
    list_filter = ('invitation', 'person', 'is_gift_handler')
    change_list_template = 'admin/invitations/assignment/change_list.html'

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.select_related('invitation', 'person')

        invitation_id = request.GET.get('invitation__id')
        person_id = request.GET.get('person__id')
        is_gift_handler = request.GET.get('is_gift_handler')

        if invitation_id:
            qs = qs.filter(invitation__id=invitation_id)
        if person_id:
            qs = qs.filter(person__id=person_id)
        if is_gift_handler is not None and is_gift_handler != '':
            qs = qs.filter(is_gift_handler=(is_gift_handler == 'True'))

        return qs

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}

        invitations = Invitation.objects.all().order_by('name')
        persons = Person.objects.all().order_by('name')
        gift_handler_options = [(True, 'Yes'), (False, 'No')]

        extra_context['horizontal_filters'] = {
            'invitations': invitations,
            'persons': persons,
            'gift_handler_options': gift_handler_options,
            'current_invitation': request.GET.get('invitation__id', ''),
            'current_person': request.GET.get('person__id', ''),
            'current_gift_handler': request.GET.get('is_gift_handler', ''),
        }

        return super().changelist_view(request, extra_context=extra_context) 