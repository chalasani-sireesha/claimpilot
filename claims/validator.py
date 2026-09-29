from datetime import datetime


# -----------------------------------------
# Mandatory fields
# -----------------------------------------

MANDATORY_FIELDS = {

    "policyNumber": "Policy Number",

    "policyholderName": "Policyholder Name",

    "effectiveStartDate": "Effective Start Date",

    "effectiveEndDate": "Effective End Date",

    "incidentDate": "Incident Date",

    "incidentTime": "Incident Time",

    "location": "Location",

    "description": "Description",

    "claimant": "Claimant",

    "contactDetails": "Contact Details",

    "assetType": "Asset Type",

    "assetId": "Asset ID",

    "estimatedDamage": "Estimated Damage",

    "claimType": "Claim Type",

    "attachments": "Attachments",

    "initialEstimate": "Initial Estimate"
}


# -----------------------------------------
# Check missing fields
# -----------------------------------------

def find_missing_fields(extracted_fields):

    missing_fields = []

    for field_key, field_name in MANDATORY_FIELDS.items():

        value = extracted_fields.get(field_key)

        if value is None or str(value).strip() == "":

            missing_fields.append(field_name)

    return missing_fields


# -----------------------------------------
# Check inconsistencies
# -----------------------------------------

def find_inconsistencies(extracted_fields):

    inconsistencies = []

    # Get dates
    start_date = extracted_fields.get(
        "effectiveStartDate"
    )

    end_date = extracted_fields.get(
        "effectiveEndDate"
    )

    incident_date = extracted_fields.get(
        "incidentDate"
    )

    # -----------------------------------------
    # Check incident date against policy period
    # -----------------------------------------

    if start_date and end_date and incident_date:

        try:

            start = datetime.strptime(
                start_date,
                "%Y-%m-%d"
            ).date()

            end = datetime.strptime(
                end_date,
                "%Y-%m-%d"
            ).date()

            incident = datetime.strptime(
                incident_date,
                "%Y-%m-%d"
            ).date()

            if incident < start or incident > end:

                inconsistencies.append(
                    "Incident date is outside the policy effective period."
                )

        except ValueError:

            inconsistencies.append(
                "One or more dates could not be validated."
            )

    # -----------------------------------------
    # Compare damage and initial estimate
    # -----------------------------------------

    estimated_damage = extracted_fields.get(
        "estimatedDamage"
    )

    initial_estimate = extracted_fields.get(
        "initialEstimate"
    )

    if (
        estimated_damage is not None
        and initial_estimate is not None
    ):

        if estimated_damage != initial_estimate:

            difference = abs(
                estimated_damage - initial_estimate
            )

            inconsistencies.append(
                f"Estimated damage and initial estimate differ by ₹{difference:.2f}."
            )

    return inconsistencies


# -----------------------------------------
# Complete validation
# -----------------------------------------

def validate_claim(extracted_fields):

    missing_fields = find_missing_fields(
        extracted_fields
    )

    inconsistencies = find_inconsistencies(
        extracted_fields
    )

    return {
        "missingFields": missing_fields,
        "inconsistencies": inconsistencies
    }