from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from .models import Invitation, Person, Assignment
from .forms import InvitationForm, PersonForm


def invitations_list(request):
    invitations = Invitation.objects.all().order_by('-created_at')
    return render(request, 'invitations/invitations_list.html', {'invitations': invitations})


def add_invitation(request):
    if request.method == 'POST':
        form = InvitationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Invitation added successfully!')
            return redirect('invitations:invitations_list')
    else:
        form = InvitationForm()
    return render(request, 'invitations/add_invitation.html', {'form': form})


def persons_list(request):
    persons = Person.objects.all().order_by('name')
    return render(request, 'invitations/persons_list.html', {'persons': persons})


def add_person(request):
    if request.method == 'POST':
        form = PersonForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Person added successfully!')
            return redirect('invitations:persons_list')
    else:
        form = PersonForm()
    return render(request, 'invitations/add_person.html', {'form': form})


def assign_persons(request, invitation_id):
    invitation = get_object_or_404(Invitation, pk=invitation_id)
    if request.method == 'POST':
        person_ids = request.POST.getlist('persons')
        Assignment.objects.filter(invitation=invitation).delete()
        for person_id in person_ids:
            Assignment.objects.create(invitation=invitation, person_id=person_id)
        messages.success(request, 'Persons assigned successfully!')
        return redirect('invitations:invitation_detail', invitation_id=invitation.id)

    persons = Person.objects.all()
    assigned_persons = invitation.assignments.values_list('person_id', flat=True)
    return render(request, 'invitations/assign_persons.html', {
        'invitation': invitation,
        'persons': persons,
        'assigned_persons': assigned_persons,
    })


def ajax_assign_persons(request, invitation_id):
    if request.method == 'POST':
        invitation = get_object_or_404(Invitation, pk=invitation_id)
        person_ids = request.POST.getlist('persons[]')
        Assignment.objects.filter(invitation=invitation).delete()
        for person_id in person_ids:
            Assignment.objects.create(invitation=invitation, person_id=person_id)
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)


def invitation_detail(request, invitation_id):
    invitation = get_object_or_404(Invitation, pk=invitation_id)
    return render(request, 'invitations/invitation_detail.html', {
        'invitation': invitation
    })