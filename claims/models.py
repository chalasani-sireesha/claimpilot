from django.db import models

# Create your models here.
from django.db import models


class Claim(models.Model):

    policy_number = models.CharField(max_length=100, blank=True)
    policyholder_name = models.CharField(max_length=200, blank=True)

    effective_start_date = models.DateField(null=True, blank=True)
    effective_end_date = models.DateField(null=True, blank=True)

    incident_date = models.DateField(null=True, blank=True)
    incident_time = models.TimeField(null=True, blank=True)
    location = models.CharField(max_length=300, blank=True)
    description = models.TextField(blank=True)

    claimant = models.CharField(max_length=200, blank=True)
    third_parties = models.TextField(blank=True)
    contact_details = models.CharField(max_length=300, blank=True)

    asset_type = models.CharField(max_length=100, blank=True)
    asset_id = models.CharField(max_length=100, blank=True)

    estimated_damage = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True
    )

    claim_type = models.CharField(max_length=100, blank=True)

    attachments = models.TextField(blank=True)

    initial_estimate = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True
    )

    missing_fields = models.JSONField(default=list)

    inconsistencies = models.JSONField(default=list)

    recommended_route = models.CharField(
        max_length=100,
        blank=True
    )

    reasoning = models.TextField(blank=True)

    investigation_flag = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.policy_number or f"Claim {self.id}"