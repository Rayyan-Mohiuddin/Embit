from django.shortcuts import get_object_or_404
from django.utils import timezone

from rest_framework import generics

from .models import (
    Department,
    TestType,
    Referral,
    ReferralNote,
    Patient,
    Hospital,
    Clinic,
)

from .serializers import (
    DepartmentSerializer,
    TestTypeSerializer,
    ReferralSerializer,
    ReferralListSerializer,
    ReferralNoteSerializer,
    ReferralStatusSerializer,
    PatientSerializer,
    HospitalSerializer,
    ClinicSerializer,
)


class DepartmentListView(generics.ListAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer


class TestTypeListView(generics.ListAPIView):
    serializer_class = TestTypeSerializer

    def get_queryset(self):
        queryset = TestType.objects.select_related(
            "department"
        )

        department_id = self.request.query_params.get(
            "department"
        )

        if department_id:
            queryset = queryset.filter(
                department_id=department_id
            )

        return queryset


class PatientListCreateView(
    generics.ListCreateAPIView
):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer


class HospitalListCreateView(
    generics.ListCreateAPIView
):
    queryset = Hospital.objects.all()
    serializer_class = HospitalSerializer


class ClinicListCreateView(
    generics.ListCreateAPIView
):
    queryset = Clinic.objects.all()
    serializer_class = ClinicSerializer


class ReferralListCreateView(
    generics.ListCreateAPIView
):
    queryset = (
        Referral.objects
        .select_related(
            "patient",
            "hospital",
            "clinic",
            "department",
            "test_type",
        )
        .prefetch_related("notes")
    )

    def get_serializer_class(self):
        if self.request.method == "POST":
            return ReferralSerializer

        return ReferralListSerializer

    def get_queryset(self):
        queryset = super().get_queryset()

        status = self.request.query_params.get(
            "status"
        )

        clinic_id = self.request.query_params.get(
            "clinic"
        )

        hospital_id = self.request.query_params.get(
            "hospital"
        )

        patient_id = self.request.query_params.get(
            "patient"
        )

        if status:
            queryset = queryset.filter(
                status=status
            )

        if clinic_id:
            queryset = queryset.filter(
                clinic_id=clinic_id
            )

        if hospital_id:
            queryset = queryset.filter(
                hospital_id=hospital_id
            )

        if patient_id:
            queryset = queryset.filter(
                patient_id=patient_id
            )

        return queryset


class ReferralDetailView(
    generics.RetrieveUpdateAPIView
):
    queryset = (
        Referral.objects
        .select_related(
            "patient",
            "hospital",
            "clinic",
            "department",
            "test_type",
        )
        .prefetch_related("notes")
    )

    serializer_class = ReferralSerializer


class ReferralStatusUpdateView(
    generics.UpdateAPIView
):
    queryset = Referral.objects.all()

    serializer_class = ReferralStatusSerializer

    http_method_names = ["patch"]

    def perform_update(self, serializer):
        referral = serializer.instance

        new_status = serializer.validated_data[
            "status"
        ]

        if new_status == Referral.Status.CONFIRMED:
            serializer.save(
                confirmed_at=timezone.now()
            )

        elif new_status == Referral.Status.COMPLETED:
            serializer.save(
                completed_at=timezone.now()
            )

        else:
            serializer.save()


class ReferralNoteListCreateView(
    generics.ListCreateAPIView
):
    serializer_class = ReferralNoteSerializer

    def get_queryset(self):
        referral_id = self.kwargs[
            "referral_id"
        ]

        return (
            ReferralNote.objects
            .filter(referral_id=referral_id)
            .select_related("referral")
        )

    def perform_create(self, serializer):
        referral_id = self.kwargs[
            "referral_id"
        ]

        referral = get_object_or_404(
            Referral,
            id=referral_id,
        )

        serializer.save(
            referral=referral
        )