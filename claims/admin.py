from django.contrib import admin

from .models import Claim


@admin.register(Claim)
class ClaimAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "policy_number",
        "policyholder_name",
        "claim_type",
        "estimated_damage",
        "recommended_route",
        "investigation_flag",
        "created_at",
    )

    list_filter = (
        "recommended_route",
        "claim_type",
        "investigation_flag",
    )

    search_fields = (
        "policy_number",
        "policyholder_name",
        "claimant",
        "asset_id",
    )

    readonly_fields = (
        "created_at",
    )

    ordering = (
        "-created_at",
    )