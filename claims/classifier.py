def classify_claim(extracted_fields):

    claim_type = extracted_fields.get("claimType")

    if not claim_type:
        return "Other"

    claim_type = claim_type.lower().strip()

    if "injury" in claim_type:
        return "Injury"

    if "vehicle" in claim_type or "auto" in claim_type or "car" in claim_type:
        return "Vehicle"

    if "property" in claim_type or "home" in claim_type:
        return "Property"

    if "theft" in claim_type or "stolen" in claim_type:
        return "Theft"

    if "fire" in claim_type:
        return "Fire"

    return "Other"