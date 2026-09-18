from django.contrib import admin

from .models import (
    Hospital,
    Clinic,
    Department,
    TestType,
    Patient,
    Referral,
    ReferralNote,
)


@admin.register(Hospital)
class HospitalAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "city",
        "contact_name",
        "contact_phone",
        "contact_email",
    )

    search_fields = (
        "name",
        "city",
        "contact_name",
    )


@admin.register(Clinic)
class ClinicAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "city",
        "contact_name",
        "contact_phone",
        "contact_email",
    )

    search_fields = (
        "name",
        "city",
        "contact_name",
    )


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(TestType)
class TestTypeAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "department",
        "created_at",
    )

    list_filter = ("department",)

    search_fields = (
        "name",
        "department__name",
    )


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = (
        "patient_ref",
        "name",
        "phone",
        "email",
        "created_at",
    )

    search_fields = (
        "patient_ref",
        "name",
        "phone",
        "email",
    )


@admin.register(Referral)
class ReferralAdmin(admin.ModelAdmin):
    list_display = (
        "patient",
        "hospital",
        "clinic",
        "department",
        "test_type",
        "urgency",
        "status",
        "created_at",
    )

    list_filter = (
        "status",
        "urgency",
        "department",
        "created_at",
    )

    search_fields = (
        "patient__patient_ref",
        "patient__name",
        "hospital__name",
        "clinic__name",
        "test_type__name",
    )


@admin.register(ReferralNote)
class ReferralNoteAdmin(admin.ModelAdmin):
    list_display = (
        "referral",
        "author_side",
        "created_at",
    )

    list_filter = ("author_side",)

    search_fields = (
        "referral__patient__patient_ref",
        "referral__patient__name",
        "message",
    )