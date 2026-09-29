from django.test import TestCase

from .extractor import extract_fnol_fields
from .validator import validate_claim
from .classifier import classify_claim
from .routing import determine_route


class ClaimPilotTests(TestCase):

    def test_fast_track_claim(self):

        fields = {
            "estimatedDamage": 18500,
            "description": "Vehicle accident",
            "claimType": "Vehicle"
        }

        validation = validate_claim(fields)

        claim_type = classify_claim(fields)

        result = determine_route(
            fields,
            validation["missingFields"],
            validation["inconsistencies"],
            claim_type
        )

        self.assertEqual(
            result["recommendedRoute"],
            "Fast-track"
        )


    def test_missing_field_claim(self):

        fields = {
            "estimatedDamage": 15000,
            "description": "Vehicle accident",
            "claimType": "Vehicle"
        }

        validation = validate_claim(fields)

        claim_type = classify_claim(fields)

        result = determine_route(
            fields,
            validation["missingFields"],
            validation["inconsistencies"],
            claim_type
        )

        self.assertEqual(
            result["recommendedRoute"],
            "Manual Review"
        )


    def test_injury_claim(self):

        fields = {
            "estimatedDamage": 10000,
            "description": "Accident caused injuries",
            "claimType": "Injury"
        }

        validation = validate_claim(fields)

        claim_type = classify_claim(fields)

        result = determine_route(
            fields,
            validation["missingFields"],
            validation["inconsistencies"],
            claim_type
        )

        self.assertEqual(
            result["recommendedRoute"],
            "Specialist Queue"
        )


    def test_investigation_claim(self):

        fields = {
            "estimatedDamage": 12000,
            "description": "The accident appears staged",
            "claimType": "Vehicle"
        }

        validation = validate_claim(fields)

        claim_type = classify_claim(fields)

        result = determine_route(
            fields,
            validation["missingFields"],
            validation["inconsistencies"],
            claim_type
        )

        self.assertEqual(
            result["recommendedRoute"],
            "Investigation Flag"
        )

        self.assertTrue(
            result["investigationFlag"]
        )


    def test_high_damage_claim(self):

        fields = {
            "estimatedDamage": 75000,
            "description": "Major vehicle accident",
            "claimType": "Vehicle"
        }

        validation = validate_claim(fields)

        claim_type = classify_claim(fields)

        result = determine_route(
            fields,
            validation["missingFields"],
            validation["inconsistencies"],
            claim_type
        )

        self.assertEqual(
            result["recommendedRoute"],
            "Manual Review"
        )