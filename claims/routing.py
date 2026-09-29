INVESTIGATION_KEYWORDS = [
    "fraud",
    "inconsistent",
    "staged"
]


def check_investigation_flag(description):

    if not description:
        return False, []

    description_lower = description.lower()

    matched_keywords = []

    for keyword in INVESTIGATION_KEYWORDS:

        if keyword in description_lower:

            matched_keywords.append(keyword)

    if matched_keywords:

        return True, matched_keywords

    return False, []


def determine_route(
    extracted_fields,
    missing_fields,
    inconsistencies,
    claim_type
):

    estimated_damage = extracted_fields.get(
        "estimatedDamage"
    )

    description = extracted_fields.get(
        "description"
    )

    # -----------------------------------------
    # Rule 1: Investigation flag
    # -----------------------------------------

    investigation_flag, matched_keywords = (
        check_investigation_flag(description)
    )

    if investigation_flag:

        return {
            "recommendedRoute": "Investigation Flag",
            "investigationFlag": True,
            "matchedKeywords": matched_keywords,
            "reasoning": (
                "Investigation keywords were detected "
                "in the claim description."
            )
        }

    # -----------------------------------------
    # Rule 2: Missing mandatory fields
    # -----------------------------------------

    if missing_fields:

        return {
            "recommendedRoute": "Manual Review",
            "investigationFlag": False,
            "matchedKeywords": [],
            "reasoning": (
                "Mandatory fields are missing. "
                "The claim requires manual review."
            )
        }

    # -----------------------------------------
    # Rule 3: Injury claim
    # -----------------------------------------

    if claim_type == "Injury":

        return {
            "recommendedRoute": "Specialist Queue",
            "investigationFlag": False,
            "matchedKeywords": [],
            "reasoning": (
                "The claim is classified as an injury claim "
                "and should be handled by a specialist."
            )
        }

    # -----------------------------------------
    # Rule 4: Fast-track
    # -----------------------------------------

    if (
        estimated_damage is not None
        and estimated_damage < 25000
    ):

        return {
            "recommendedRoute": "Fast-track",
            "investigationFlag": False,
            "matchedKeywords": [],
            "reasoning": (
                "All mandatory fields are available and "
                "estimated damage is below ₹25,000."
            )
        }

    # -----------------------------------------
    # Default
    # -----------------------------------------

    return {
        "recommendedRoute": "Manual Review",
        "investigationFlag": False,
        "matchedKeywords": [],
        "reasoning": (
            "The claim does not qualify for fast-track "
            "processing and requires manual assessment."
        )
    }