from django.conf import settings
from django.db import models

class UserProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile"
    )

    contact_number = models.CharField(max_length=20, blank=True, null=True)
    language = models.CharField(
        max_length=5,
        choices=[("en", "English"), ("sin", "Sinhala"), ("tl", "Tamil")],
        default="en"
    )
    other_details = models.JSONField(blank=True, null=True)

    def __str__(self):
        return self.user.username
