import os
from datetime import datetime
from decimal import Decimal

import fitz

from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.permissions import AllowAny

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Claim
from .serializers import ClaimSerializer

from .extractor import extract_fnol_fields
from .ai_extractor import ai_extract_fnol_fields
from .validator import validate_claim
from .classifier import classify_claim
from .routing import determine_route


def convert_date(value):

    if not value:
        return None

    try:
        return datetime.strptime(
            value,
            "%Y-%m-%d"
        ).date()

    except ValueError:
        return None


def convert_time(value):

    if not value:
        return None

    formats = [
        "%I:%M %p",
        "%H:%M"
    ]

    for time_format in formats:

        try:

            return datetime.strptime(
                value.strip(),
                time_format
            ).time()

        except ValueError:
            continue

    return None


def convert_amount(value):

    if value is None:
        return None

    return Decimal(str(value))


class ClaimListCreateAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):

        claims = Claim.objects.all().order_by(
            "-created_at"
        )

        serializer = ClaimSerializer(
            claims,
            many=True
        )

        return Response(
            serializer.data
        )


    def post(self, request):

        serializer = ClaimSerializer(
            data=request.data
        )

        if serializer.is_valid():

            claim = serializer.save()

            return Response(
                ClaimSerializer(claim).data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class ClaimStatisticsAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):

        total_claims = Claim.objects.count()

        fast_track = Claim.objects.filter(
            recommended_route="Fast-track"
        ).count()

        manual_review = Claim.objects.filter(
            recommended_route="Manual Review"
        ).count()

        investigation = Claim.objects.filter(
            recommended_route="Investigation Flag"
        ).count()

        specialist = Claim.objects.filter(
            recommended_route="Specialist Queue"
        ).count()

        return Response({

            "totalClaims": total_claims,

            "fastTrack": fast_track,

            "manualReview": manual_review,

            "investigation": investigation,

            "specialist": specialist

        })


class ClaimDocumentUploadAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):

        uploaded_file = request.FILES.get(
            "document"
        )

        if not uploaded_file:

            return Response(
                {
                    "error":
                    "Please upload a PDF or TXT file."
                },
                status=status.HTTP_400_BAD_REQUEST
            )


        file_name = uploaded_file.name

        extension = os.path.splitext(
            file_name
        )[1].lower()


        if extension not in [".pdf", ".txt"]:

            return Response(
                {
                    "error":
                    "Only PDF and TXT files are supported."
                },
                status=status.HTTP_400_BAD_REQUEST
            )


        os.makedirs(
            settings.MEDIA_ROOT,
            exist_ok=True
        )


        file_path = os.path.join(
            settings.MEDIA_ROOT,
            file_name
        )


        with open(
            file_path,
            "wb+"
        ) as destination:

            for chunk in uploaded_file.chunks():

                destination.write(chunk)


        extracted_text = ""


        if extension == ".pdf":

            document = fitz.open(
                file_path
            )

            for page in document:

                extracted_text += page.get_text()

            document.close()


        elif extension == ".txt":

            with open(
                file_path,
                "r",
                encoding="utf-8"
            ) as file:

                extracted_text = file.read()


        # ---------------------------------
        # NORMAL EXTRACTION
        # ---------------------------------

        extracted_fields = extract_fnol_fields(
            extracted_text
        )


        # ---------------------------------
        # AI FALLBACK
        # ---------------------------------

        important_fields = [

            "policyNumber",
            "policyholderName",
            "incidentDate",
            "description",
            "claimant",
            "estimatedDamage",
            "claimType"

        ]


        missing_important_fields = [

            field

            for field in important_fields

            if not extracted_fields.get(field)

        ]


        if len(missing_important_fields) >= 2:

            ai_fields = ai_extract_fnol_fields(
                extracted_text
            )


            for field, value in ai_fields.items():

                if (
                    not extracted_fields.get(field)
                    and value is not None
                ):

                    extracted_fields[field] = value


        # ---------------------------------
        # VALIDATION
        # ---------------------------------

        validation_result = validate_claim(
            extracted_fields
        )


        missing_fields = validation_result[
            "missingFields"
        ]


        inconsistencies = validation_result[
            "inconsistencies"
        ]


        # ---------------------------------
        # CLASSIFICATION
        # ---------------------------------

        claim_type = classify_claim(
            extracted_fields
        )


        # ---------------------------------
        # ROUTING
        # ---------------------------------

        routing_result = determine_route(

            extracted_fields,

            missing_fields,

            inconsistencies,

            claim_type

        )


        # ---------------------------------
        # SAVE CLAIM
        # ---------------------------------

        claim = Claim.objects.create(

            policy_number=
            extracted_fields.get(
                "policyNumber"
            ) or "",


            policyholder_name=
            extracted_fields.get(
                "policyholderName"
            ) or "",


            effective_start_date=
            convert_date(
                extracted_fields.get(
                    "effectiveStartDate"
                )
            ),


            effective_end_date=
            convert_date(
                extracted_fields.get(
                    "effectiveEndDate"
                )
            ),


            incident_date=
            convert_date(
                extracted_fields.get(
                    "incidentDate"
                )
            ),


            incident_time=
            convert_time(
                extracted_fields.get(
                    "incidentTime"
                )
            ),


            location=
            extracted_fields.get(
                "location"
            ) or "",


            description=
            extracted_fields.get(
                "description"
            ) or "",


            claimant=
            extracted_fields.get(
                "claimant"
            ) or "",


            third_parties=
            extracted_fields.get(
                "thirdParties"
            ) or "",


            contact_details=
            extracted_fields.get(
                "contactDetails"
            ) or "",


            asset_type=
            extracted_fields.get(
                "assetType"
            ) or "",


            asset_id=
            extracted_fields.get(
                "assetId"
            ) or "",


            estimated_damage=
            convert_amount(
                extracted_fields.get(
                    "estimatedDamage"
                )
            ),


            claim_type=
            extracted_fields.get(
                "claimType"
            ) or "",


            attachments=
            extracted_fields.get(
                "attachments"
            ) or "",


            initial_estimate=
            convert_amount(
                extracted_fields.get(
                    "initialEstimate"
                )
            ),


            missing_fields=
            missing_fields,


            inconsistencies=
            inconsistencies,


            recommended_route=
            routing_result[
                "recommendedRoute"
            ],


            reasoning=
            routing_result[
                "reasoning"
            ],


            investigation_flag=
            routing_result[
                "investigationFlag"
            ]

        )


        # ---------------------------------
        # FINAL RESPONSE
        # ---------------------------------

        return Response(

            {

                "claimId":
                claim.id,


                "extractedFields":
                extracted_fields,


                "missingFields":
                missing_fields,


                "inconsistencies":
                inconsistencies,


                "claimClassification":
                claim_type,


                "recommendedRoute":
                routing_result[
                    "recommendedRoute"
                ],


                "investigationFlag":
                routing_result[
                    "investigationFlag"
                ],


                "matchedKeywords":
                routing_result.get(
                    "matchedKeywords",
                    []
                ),


                "reasoning":
                routing_result[
                    "reasoning"
                ]

            },

            status=status.HTTP_200_OK

        )