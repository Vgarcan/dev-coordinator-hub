from django.core.validators import RegexValidator
from django.db import models

# Create your models here.


class Repository(models.Model):
    """Represent a GitHub repository in the local, non-executable inventory."""

    class TrackingStatus(models.TextChoices):
        CANDIDATE = 'candidate', 'Candidate'
        TRACKED = 'tracked', 'Tracked'
        ARCHIVED = 'archived', 'Archived'

    # Restrict identifiers to a GitHub owner/repository pair; no credentials or API URLs.
    full_name = models.CharField(
        max_length=200,
        unique=True,
        validators=[
            RegexValidator(
                regex=r'\A[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+\Z',
                message='Use GitHub owner/repository format.',
            ),
        ],
    )
    description = models.TextField(blank=True)
    tracking_status = models.CharField(
        max_length=12,
        choices=TrackingStatus.choices,
        default=TrackingStatus.CANDIDATE,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['full_name']

    def __str__(self):
        return self.full_name

    @property
    def github_url(self):
        """Produce a link without requiring GitHub credentials or network calls."""
        return f'https://github.com/{self.full_name}'
