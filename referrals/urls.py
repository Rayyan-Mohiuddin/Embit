from django.urls import path

from .views import (
    DepartmentListView,
    TestTypeListView,
    PatientListCreateView,
    HospitalListCreateView,
    ClinicListCreateView,
    ReferralListCreateView,
    ReferralDetailView,
    ReferralStatusUpdateView,
    ReferralNoteListCreateView,
)


urlpatterns = [
    path(
        "departments/",
        DepartmentListView.as_view(),
        name="department-list",
    ),

    path(
        "test-types/",
        TestTypeListView.as_view(),
        name="test-type-list",
    ),

    path(
        "patients/",
        PatientListCreateView.as_view(),
        name="patient-list-create",
    ),

    path(
        "hospitals/",
        HospitalListCreateView.as_view(),
        name="hospital-list-create",
    ),

    path(
        "clinics/",
        ClinicListCreateView.as_view(),
        name="clinic-list-create",
    ),

    path(
        "referrals/",
        ReferralListCreateView.as_view(),
        name="referral-list-create",
    ),

    path(
        "referrals/<int:pk>/",
        ReferralDetailView.as_view(),
        name="referral-detail",
    ),

    path(
        "referrals/<int:pk>/status/",
        ReferralStatusUpdateView.as_view(),
        name="referral-status-update",
    ),

    path(
        "referrals/<int:referral_id>/notes/",
        ReferralNoteListCreateView.as_view(),
        name="referral-notes",
    ),
]