import os
import json

from groq import Groq


def ai_extract_fnol_fields(text):

    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        return {}

    try:

        client = Groq(
            api_key=api_key
        )

        prompt = f"""
You are an insurance claims document extraction assistant.

Extract these fields from the FNOL document.

Return ONLY valid JSON.

{{
    "policyNumber": null,
    "policyholderName": null,
    "effectiveStartDate": null,
    "effectiveEndDate": null,
    "incidentDate": null,
    "incidentTime": null,
    "location": null,
    "description": null,
    "claimant": null,
    "thirdParties": null,
    "contactDetails": null,
    "assetType": null,
    "assetId": null,
    "estimatedDamage": null,
    "claimType": null,
    "attachments": null,
    "initialEstimate": null
}}

Rules:
- Do not invent information.
- Missing values must be null.
- Dates should use YYYY-MM-DD.
- Amounts must be numbers.
- Return only JSON.

FNOL DOCUMENT:

{text}
"""

        response = client.chat.completions.create(

            model="openai/gpt-oss-20b",

            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],

            temperature=0
        )

        content = response.choices[0].message.content

        return json.loads(content)

    except Exception as error:

        print("AI extraction error:", error)

        return {}