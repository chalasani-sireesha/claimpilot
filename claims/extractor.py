import re
from datetime import datetime


def extract_value(text, field_name):

    pattern = rf"{re.escape(field_name)}\s*:\s*(.+)"

    match = re.search(
        pattern,
        text,
        re.IGNORECASE
    )

    if match:
        return match.group(1).strip()

    return None


def extract_date(value):

    if not value:
        return None

    formats = [
        "%d/%m/%Y",
        "%d-%m-%Y",
        "%Y-%m-%d"
    ]

    for date_format in formats:

        try:

            date_object = datetime.strptime(
                value.strip(),
                date_format
            )

            return date_object.strftime("%Y-%m-%d")

        except ValueError:
            continue

    return value


def extract_amount(value):

    if not value:
        return None

    value = value.replace(",", "")
    value = value.replace("₹", "")
    value = value.strip()

    try:
        return float(value)

    except ValueError:
        return None

def extract_description(text):

    pattern = (
        r"Description\s*:\s*"
        r"(.*?)(?=\n\s*(Claimant|Third Parties|"
        r"Contact Details|Asset Type|Asset ID|"
        r"Estimated Damage|Claim Type|Attachments|"
        r"Initial Estimate)\s*:)"
    )

    match = re.search(
        pattern,
        text,
        re.IGNORECASE | re.DOTALL
    )

    if match:

        return " ".join(
            match.group(1).split()
        )

    return None


def extract_fnol_fields(text):

    extracted = {

        "policyNumber": extract_value(
            text,
            "Policy Number"
        ),

        "policyholderName": extract_value(
            text,
            "Policyholder Name"
        ),

        "effectiveStartDate": extract_date(
            extract_value(
                text,
                "Effective Start Date"
            )
        ),

        "effectiveEndDate": extract_date(
            extract_value(
                text,
                "Effective End Date"
            )
        ),

        "incidentDate": extract_date(
            extract_value(
                text,
                "Incident Date"
            )
        ),

        "incidentTime": extract_value(
            text,
            "Incident Time"
        ),

        "location": extract_value(
            text,
            "Location"
        ),

        "description": extract_description(
            text
        ),

        "claimant": extract_value(
            text,
            "Claimant"
        ),

        "thirdParties": extract_value(
            text,
            "Third Parties"
        ),

        "contactDetails": extract_value(
            text,
            "Contact Details"
        ),

        "assetType": extract_value(
            text,
            "Asset Type"
        ),

        "assetId": extract_value(
            text,
            "Asset ID"
        ),

        "estimatedDamage": extract_amount(
            extract_value(
                text,
                "Estimated Damage"
            )
        ),

        "claimType": extract_value(
            text,
            "Claim Type"
        ),

        "attachments": extract_value(
            text,
            "Attachments"
        ),

        "initialEstimate": extract_amount(
            extract_value(
                text,
                "Initial Estimate"
            )
        )
    }

    return extracted