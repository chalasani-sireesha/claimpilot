from django.urls import path

from .views import (ClaimListCreateAPIView,ClaimStatisticsAPIView,ClaimDocumentUploadAPIView)


urlpatterns = [

    path(
        'claims/',
        ClaimListCreateAPIView.as_view(),
        name='claims'
    ),
    path('process-claim/',ClaimDocumentUploadAPIView.as_view(),name='process-claim'),
    path(
    'statistics/',
    ClaimStatisticsAPIView.as_view(),
    name='claim-statistics'
),

]