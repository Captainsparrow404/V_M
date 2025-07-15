from django.db import models
from django.utils import timezone

class Person(models.Model):
    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15, unique=True)
    email = models.EmailField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    assembly = models.CharField(max_length=100, blank=True, null=True)
    mandal = models.CharField(max_length=100, blank=True, null=True)
    area = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.name

class Invitation(models.Model):
    name = models.CharField(max_length=255)
    mobile_number = models.CharField(max_length=15, blank=True, null=True)
    mandal = models.CharField(max_length=100, blank=True, null=True)
    address_venue = models.TextField(blank=True, null=True)
    area = models.CharField(max_length=100, blank=True, null=True)
    file_upload = models.FileField(upload_to='invitations/', blank=True, null=True)
    invitation_type = models.CharField(max_length=255, blank=True, null=True)
    event_date = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    persons = models.ManyToManyField(Person, through='Assignment', related_name='invitations')

    def __str__(self):
        return self.name

class Assignment(models.Model):
    invitation = models.ForeignKey(Invitation, on_delete=models.CASCADE, related_name='assignments')
    person = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='assignments')
    is_gift_handler = models.BooleanField(default=False)

    class Meta:
        unique_together = ('invitation', 'person')

    def __str__(self):
        return f"{self.person.name} assigned to {self.invitation.name}" 