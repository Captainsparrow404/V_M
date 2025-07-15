# from django.db import models
# from django.utils import timezone
# from django.contrib.auth import get_user_model
# from django.core.validators import MinValueValidator, MaxValueValidator
#
#
# class Pass(models.Model):
#     STATUS_CHOICES = [
#         ('PENDING', 'Pending'),
#         ('APPROVED', 'Approved'),
#         ('REJECTED', 'Rejected'),
#     ]
#
#     TEMPLE_CHOICES = [
#         ('Sri Mahakaaleshwar Mandir', 'Sri Mahakaaleshwar Mandir'),
#         ('Tirumala Tirupati Devasthanam', 'Tirumala Tirupati Devasthanam'),
#         ('Dwaraka Tirumala Devasthanam', 'Dwaraka Tirumala Devasthanam'),
#         ('Sree Padmanabha Swamy Devasthanam', 'Sree Padmanabha Swamy Devasthanam'),
#         (
#         'Sri Bhramaramba Mallikarjuna Swamy Varla Devasthanam', 'Sri Bhramaramba Mallikarjuna Swamy Varla Devasthanam'),
#         ('Sri Gnanaprasunambika Sametha Srikalahasteeswara Temple',
#          'Sri Gnanaprasunambika Sametha Srikalahasteeswara Temple'),
#         ('Shri Shirdi Sayee Samsthan', 'Shri Shirdi Sayee Samsthan'),
#         ('Sabarimala Sree Ayyappa Devasthanam', 'Sabarimala Sree Ayyappa Devasthanam'),
#         ('Shree Jagannath Temple', 'Shree Jagannath Temple'),
#         ('Shri Kashi Vishwanath Temple', 'Shri Kashi Vishwanath Temple'),
#         ('Swayambhu Sri Varasiddhi Vinayaka Swamy', 'Swayambhu Sri Varasiddhi Vinayaka Swamy'),
#         ('Sri Kamakshi Ambal Devasthanam', 'Sri Kamakshi Ambal Devasthanam'),
#         ('Ram Lala Ayodha', 'Ram Lala Ayodha'),
#         ('Arulmigu Arunachaleswarar Temple', 'Arulmigu Arunachaleswarar Temple'),
#     ]
#
#     ID_PROOF_CHOICES = [
#         ('AADHAR', 'Aadhar Card'),
#         ('VOTER', 'Voter ID'),
#         ('PAN', 'PAN Card'),
#         ('DL', 'Driving License'),
#     ]
#
#     name = models.CharField(max_length=100)
#     email = models.EmailField()
#     phone = models.CharField(max_length=15)
#     temple = models.CharField(max_length=100, choices=TEMPLE_CHOICES)
#     num_persons = models.PositiveIntegerField(
#         validators=[
#             MinValueValidator(1, message="Number of persons must be at least 1"),
#             MaxValueValidator(6, message="Maximum 6 persons allowed per pass")
#         ],
#         help_text="Maximum 6 persons allowed per pass"
#     )
#     visit_date = models.DateField()
#     # Add ID proof fields
#     id_proof_type = models.CharField(
#         max_length=10,
#         choices=ID_PROOF_CHOICES,
#         verbose_name='ID Proof Type'
#     )
#     id_proof_number = models.CharField(
#         max_length=50,
#         verbose_name='ID Proof Number'
#     )
#     status = models.CharField(
#         max_length=10,
#         choices=STATUS_CHOICES,
#         default='PENDING'
#     )
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#
#     # Making these fields hidden from regular API responses
#     processed_at = models.DateTimeField(null=True, blank=True, editable=False)
#     processed_by = models.ForeignKey(
#         get_user_model(),
#         on_delete=models.SET_NULL,
#         null=True,
#         blank=True,
#         editable=False
#     )
#
#     class Meta:
#         verbose_name = 'Pass'
#         verbose_name_plural = 'Passes'
#         ordering = ['-created_at']
#
#     def __str__(self):
#         return f"{self.name} - {self.temple} - {self.status}"
#
#     def save(self, *args, **kwargs):
#         # Capitalize ID proof number
#         if self.id_proof_number:
#             self.id_proof_number = self.id_proof_number.upper()
#         super().save(*args, **kwargs)
#
#     @staticmethod
#     def has_approval_today():
#         return Pass.objects.filter(
#             status='APPROVED',
#             processed_at__date=timezone.now().date()
#         ).exists()

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.contrib.auth import get_user_model


class Pass(models.Model):
    """Model for managing temple visit passes"""

    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
    ]

    TEMPLE_CHOICES = [
        ('Sri Mahakaaleshwar Mandir', 'Sri Mahakaaleshwar Mandir'),
        ('Tirumala Tirupati Devasthanam', 'Tirumala Tirupati Devasthanam'),
        ('Dwaraka Tirumala Devasthanam', 'Dwaraka Tirumala Devasthanam'),
        ('Sree Padmanabha Swamy Devasthanam', 'Sree Padmanabha Swamy Devasthanam'),
        ('Sri Bhramaramba Mallikarjuna Swamy Varla Devasthanam',
         'Sri Bhramaramba Mallikarjuna Swamy Varla Devasthanam'),
        ('Sri Gnanaprasunambika Sametha Srikalahasteeswara Temple',
         'Sri Gnanaprasunambika Sametha Srikalahasteeswara Temple'),
        ('Shri Shirdi Sayee Samsthan', 'Shri Shirdi Sayee Samsthan'),
        ('Sabarimala Sree Ayyappa Devasthanam', 'Sabarimala Sree Ayyappa Devasthanam'),
        ('Shree Jagannath Temple', 'Shree Jagannath Temple'),
        ('Shri Kashi Vishwanath Temple', 'Shri Kashi Vishwanath Temple'),
        ('Swayambhu Sri Varasiddhi Vinayaka Swamy', 'Swayambhu Sri Varasiddhi Vinayaka Swamy'),
        ('Sri Kamakshi Ambal Devasthanam', 'Sri Kamakshi Ambal Devasthanam'),
        ('Ram Lala Ayodha', 'Ram Lala Ayodha'),
        ('Arulmigu Arunachaleswarar Temple', 'Arulmigu Arunachaleswarar Temple'),
    ]

    ID_PROOF_CHOICES = [
        ('AADHAR', 'Aadhar Card'),
        ('VOTER', 'Voter ID'),
        ('PAN', 'PAN Card'),
        ('DL', 'Driving License'),
    ]

    # Personal Information
    name = models.CharField(
        max_length=100,
        help_text="Full name of the primary visitor"
    )

    email = models.EmailField(
        help_text="Email address for communication and pass delivery"
    )

    phone = models.CharField(
        max_length=15,
        help_text="10-digit mobile number"
    )

    # Visit Details
    temple = models.CharField(
        max_length=100,
        choices=TEMPLE_CHOICES,
        help_text="Select the temple you wish to visit"
    )

    num_persons = models.PositiveIntegerField(
        validators=[
            MinValueValidator(1, message="Number of persons must be at least 1")
        ],
        help_text="Number of persons visiting"
    )

    visit_date = models.DateField(
        help_text="Planned date of visit"
    )

    # ID Proof Information
    id_proof_type = models.CharField(
        max_length=10,
        choices=ID_PROOF_CHOICES,
        verbose_name='ID Proof Type',
        help_text="Type of ID proof being submitted"
    )

    id_proof_number = models.CharField(
        max_length=50,
        verbose_name='ID Proof Number',
        help_text="Number of the selected ID proof"
    )

    # Status and Processing Information
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='PENDING',
        help_text="Current status of the pass request"
    )

    # Timestamps and User Information
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Timestamp when the pass request was created"
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="Timestamp when the pass request was last updated"
    )

    processed_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Timestamp when the pass request was processed"
    )

    processed_by = models.ForeignKey(
        get_user_model(),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='processed_passes',
        help_text="Admin user who processed the pass request"
    )

    accommodation_date = models.DateField(null=True, blank=True, help_text="Accommodation date (if applicable)")
    darshan_date = models.DateField(null=True, blank=True, help_text="Darshan date (if applicable)")
    DARSHAN_TYPE_CHOICES = [
        ("REGULAR", "Regular"),
        ("SPECIAL", "Special"),
        ("VVIP", "VVIP"),
        ("SPARSHA", "Sparsha"),
    ]
    darshan_type = models.CharField(
        max_length=20,
        choices=DARSHAN_TYPE_CHOICES,
        null=True,
        blank=True,
        help_text="Type of darshan (admin can set this)"
    )

    class Meta:
        verbose_name = 'Pass'
        verbose_name_plural = 'Passes'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['temple', 'visit_date', 'status']),
            models.Index(fields=['status', 'created_at']),
        ]

    def __str__(self):
        return f"{self.name} - {self.temple} - {self.visit_date} - {self.status}"

        # Remove the default validators from num_persons field
        num_persons = models.PositiveIntegerField()

        def clean(self):
            super().clean()
            if self.temple == 'Tirumala Tirupati Devasthanam':
                if self.num_persons < 1 or self.num_persons > 6:
                    raise ValidationError({
                        'num_persons': 'For Tirumala Tirupati Devasthanam, number of persons must be between 1 and 6'
                    })

                # Check for existing approved pass
                existing_pass = Pass.objects.filter(
                    temple=self.temple,
                    visit_date=self.visit_date,
                    status='APPROVED'
                ).exclude(id=self.id).exists()

                if existing_pass:
                    raise ValidationError(
                        'An approved pass already exists for Tirumala Tirupati Devasthanam on this date'
                    )
            else:
                # Only validate that number of persons is at least 1 for other temples
                if self.num_persons < 1:
                    raise ValidationError({
                        'num_persons': 'Number of persons must be at least 1'
                    })

    def save(self, *args, **kwargs):
        """Override save method to perform additional operations"""
        # Capitalize ID proof number
        if self.id_proof_number:
            self.id_proof_number = self.id_proof_number.upper()

        # If status is being changed to APPROVED or REJECTED, set processed_at
        if self.pk:  # If this is an update
            old_instance = Pass.objects.get(pk=self.pk)
            if old_instance.status != self.status and self.status in ['APPROVED', 'REJECTED']:
                self.processed_at = timezone.now()

        self.full_clean()  # Run full validation
        super().save(*args, **kwargs)

    @staticmethod
    def has_approved_pass_for_date(temple, visit_date, exclude_id=None):
        """Check if there's an approved pass for given temple and date"""
        query = Pass.objects.filter(
            temple=temple,
            visit_date=visit_date,
            status='APPROVED'
        )

        if exclude_id:
            query = query.exclude(id=exclude_id)

        return query.exists()

    def can_be_cancelled(self):
        """Check if the pass can be cancelled"""
        return (
                self.status == 'APPROVED' and
                self.visit_date > timezone.now().date()
        )

    def can_be_modified(self):
        """Check if the pass can be modified"""
        return (
                self.status == 'PENDING' and
                self.visit_date > timezone.now().date()
        )