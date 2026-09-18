from django.db import models


class Hospital(models.Model):
    name = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    contact_name = models.CharField(max_length=255, blank=True)
    contact_phone = models.CharField(max_length=30, blank=True)
    contact_email = models.EmailField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Clinic(models.Model):
    name = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    contact_name = models.CharField(max_length=255, blank=True)
    contact_phone = models.CharField(max_length=30, blank=True)
    contact_email = models.EmailField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class TestType(models.Model):
    department = models.ForeignKey(
        Department,
        on_delete=models.PROTECT,
        related_name="test_types",
    )

    name = models.CharField(max_length=255)

    # Flexible default protocol template.
    # This is copied into Referral.protocol_details
    # when a referral is created.
    default_protocol = models.TextField(
        blank=True,
        help_text="Default protocol shown when creating a referral.",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["department__name", "name"]

        constraints = [
            models.UniqueConstraint(
                fields=["department", "name"],
                name="unique_test_type_per_department",
            )
        ]

    def __str__(self):
        return f"{self.department.name} - {self.name}"


class Patient(models.Model):
    patient_ref = models.CharField(
        max_length=100,
        unique=True,
    )

    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=30, blank=True)
    email = models.EmailField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} ({self.patient_ref})"


class Referral(models.Model):

    class Urgency(models.TextChoices):
        ROUTINE = "routine", "Routine"
        URGENT = "urgent", "Urgent"
        PRE_OP = "pre-op", "Pre-op"

    class Status(models.TextChoices):
        SENT = "sent", "Sent"
        CONFIRMED = "confirmed", "Confirmed"
        NEEDS_CLARIFICATION = (
            "needs_clarification",
            "Needs clarification",
        )
        COMPLETED = "completed", "Completed"

    patient = models.ForeignKey(
        Patient,
        on_delete=models.PROTECT,
        related_name="referrals",
    )

    hospital = models.ForeignKey(
        Hospital,
        on_delete=models.PROTECT,
        related_name="referrals",
    )

    clinic = models.ForeignKey(
        Clinic,
        on_delete=models.PROTECT,
        related_name="referrals",
    )

    department = models.ForeignKey(
        Department,
        on_delete=models.PROTECT,
        related_name="referrals",
    )

    test_type = models.ForeignKey(
        TestType,
        on_delete=models.PROTECT,
        related_name="referrals",
    )

    protocol_details = models.TextField()

    urgency = models.CharField(
        max_length=20,
        choices=Urgency.choices,
        default=Urgency.ROUTINE,
    )

    status = models.CharField(
        max_length=30,
        choices=Status.choices,
        default=Status.SENT,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    confirmed_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return (
            f"{self.patient.patient_ref} - "
            f"{self.test_type.name}"
        )


class ReferralNote(models.Model):

    class AuthorSide(models.TextChoices):
        HOSPITAL = "hospital", "Hospital"
        CLINIC = "clinic", "Clinic"

    referral = models.ForeignKey(
        Referral,
        on_delete=models.CASCADE,
        related_name="notes",
    )

    author_side = models.CharField(
        max_length=20,
        choices=AuthorSide.choices,
    )

    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return (
            f"{self.referral.patient.patient_ref} - "
            f"{self.author_side}"
        )