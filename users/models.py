from django.conf import settings
from django.db import models


class UserProfile(models.Model):

    class Role(models.TextChoices):
        SUPER_ADMIN = 'SUPER_ADMIN', 'Super Admin'
        ADMIN = 'ADMIN', 'Admin'
        REGISTERED_USER = 'REGISTERED_USER', 'Registered User'
        VIEWER = 'VIEWER', 'Viewer'

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile"
    )

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.VIEWER,
    )
    contact_number = models.CharField(max_length=20, blank=True, null=True)
    language = models.CharField(
        max_length=5,
        choices=[("en", "English"), ("sin", "Sinhala"), ("tl", "Tamil")],
        default="en"
    )
    other_details = models.JSONField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} ({self.get_role_display()})"
