from rest_framework import serializers

from .models import (
    Patient,
    Hospital,
    Clinic,
    Department,
    TestType,
    Referral,
    ReferralNote,
)


class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = [
            "id",
            "patient_ref",
            "name",
            "phone",
            "email",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
        ]


class HospitalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hospital
        fields = [
            "id",
            "name",
            "city",
            "contact_name",
            "contact_phone",
            "contact_email",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
        ]


class ClinicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clinic
        fields = [
            "id",
            "name",
            "city",
            "contact_name",
            "contact_phone",
            "contact_email",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
        ]


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = [
            "id",
            "name",
            "created_at",
        ]
        read_only_fields = [
            "id",
            "created_at",
        ]


class TestTypeSerializer(serializers.ModelSerializer):
    department_name = serializers.CharField(
        source="department.name",
        read_only=True,
    )

    class Meta:
        model = TestType

        fields = [
            "id",
            "department",
            "department_name",
            "name",
            "default_protocol",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "department_name",
            "created_at",
            "updated_at",
        ]


class ReferralNoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReferralNote
        fields = [
            "id",
            "referral",
            "author_side",
            "message",
            "created_at",
        ]
        read_only_fields = [
            "id",
            "created_at",
        ]


class ReferralSerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(
        source="patient.name",
        read_only=True,
    )

    patient_ref = serializers.CharField(
        source="patient.patient_ref",
        read_only=True,
    )

    hospital_name = serializers.CharField(
        source="hospital.name",
        read_only=True,
    )

    clinic_name = serializers.CharField(
        source="clinic.name",
        read_only=True,
    )

    department_name = serializers.CharField(
        source="department.name",
        read_only=True,
    )

    test_type_name = serializers.CharField(
        source="test_type.name",
        read_only=True,
    )

    notes = ReferralNoteSerializer(
        many=True,
        read_only=True,
    )

    protocol_details = serializers.CharField(
        required=False,
        allow_blank=True,
    )

    class Meta:
        model = Referral
        fields = [
            "id",

            "patient",
            "patient_name",
            "patient_ref",

            "hospital",
            "hospital_name",

            "clinic",
            "clinic_name",

            "department",
            "department_name",

            "test_type",
            "test_type_name",

            "protocol_details",

            "urgency",
            "status",

            "confirmed_at",
            "completed_at",

            "created_at",
            "updated_at",

            "notes",
        ]

        read_only_fields = [
            "id",
            "patient_name",
            "patient_ref",
            "hospital_name",
            "clinic_name",
            "department_name",
            "test_type_name",
            "status",
            "confirmed_at",
            "completed_at",
            "created_at",
            "updated_at",
            "notes",
        ]

    def validate(self, attrs):
        department = attrs.get("department")
        test_type = attrs.get("test_type")

        if department and test_type:
            if test_type.department_id != department.id:
                raise serializers.ValidationError({
                    "test_type": (
                        f"'{test_type.name}' does not belong to "
                        f"the '{department.name}' department."
                    )
                })

        return attrs

    def create(self, validated_data):
        if not validated_data.get("protocol_details"):
            test_type = validated_data["test_type"]

            validated_data["protocol_details"] = (
                test_type.default_protocol
            )

        return super().create(validated_data)


class ReferralListSerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(
        source="patient.name",
        read_only=True,
    )

    patient_ref = serializers.CharField(
        source="patient.patient_ref",
        read_only=True,
    )

    hospital_name = serializers.CharField(
        source="hospital.name",
        read_only=True,
    )

    clinic_name = serializers.CharField(
        source="clinic.name",
        read_only=True,
    )

    department_name = serializers.CharField(
        source="department.name",
        read_only=True,
    )

    test_type_name = serializers.CharField(
        source="test_type.name",
        read_only=True,
    )

    class Meta:
        model = Referral
        fields = [
            "id",

            "patient",
            "patient_name",
            "patient_ref",

            "hospital",
            "hospital_name",

            "clinic",
            "clinic_name",

            "department_name",
            "test_type_name",

            "urgency",
            "status",

            "created_at",
            "updated_at",
        ]


class ReferralStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Referral
        fields = [
            "id",
            "status",
            "confirmed_at",
            "completed_at",
        ]

        read_only_fields = [
            "id",
            "confirmed_at",
            "completed_at",
        ]

    def validate_status(self, new_status):
        referral = self.instance
        current_status = referral.status

        allowed_transitions = {
            Referral.Status.SENT: {
                Referral.Status.CONFIRMED,
                Referral.Status.NEEDS_CLARIFICATION,
            },
            Referral.Status.NEEDS_CLARIFICATION: {
                Referral.Status.CONFIRMED,
            },
            Referral.Status.CONFIRMED: {
                Referral.Status.NEEDS_CLARIFICATION,
                Referral.Status.COMPLETED,
            },
            Referral.Status.COMPLETED: set(),
        }

        allowed = allowed_transitions.get(
            current_status,
            set(),
        )

        if new_status not in allowed:
            raise serializers.ValidationError(
                f"Cannot change referral status from "
                f"'{current_status}' to '{new_status}'."
            )

        return new_status