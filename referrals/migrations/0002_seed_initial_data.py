from django.db import migrations


def seed_initial_data(apps, schema_editor):
    Department = apps.get_model("referrals", "Department")
    TestType = apps.get_model("referrals", "TestType")

    departments = {}

    department_names = [
        "Cardiology",
        "Orthopedics",
        "Oncology",
        "Neurology",
        "General Medicine",
    ]

    for name in department_names:
        department, _ = Department.objects.get_or_create(
            name=name
        )
        departments[name] = department

    tests = [
        {
            "department": "Cardiology",
            "name": "CT Coronary Angiography",
            "default_contrast_type": "IV contrast",
            "default_slice_thickness": "0.5 mm",
            "default_timing": "ECG-gated acquisition",
        },
        {
            "department": "Cardiology",
            "name": "Echocardiogram",
            "default_contrast_type": "Not applicable",
            "default_slice_thickness": "Not applicable",
            "default_timing": "Standard echocardiography protocol",
        },
        {
            "department": "Orthopedics",
            "name": "X-Ray Knee",
            "default_contrast_type": "No contrast",
            "default_slice_thickness": "Not applicable",
            "default_timing": "AP and lateral views",
        },
        {
            "department": "Orthopedics",
            "name": "MRI Knee",
            "default_contrast_type": "No contrast",
            "default_slice_thickness": "Standard MRI protocol",
            "default_timing": "Multiplanar sequences",
        },
        {
            "department": "Oncology",
            "name": "CT Chest",
            "default_contrast_type": "IV contrast",
            "default_slice_thickness": "1 mm",
            "default_timing": "70 seconds after contrast injection",
        },
        {
            "department": "Oncology",
            "name": "PET-CT",
            "default_contrast_type": "FDG",
            "default_slice_thickness": "Standard PET-CT protocol",
            "default_timing": "Approximately 60 minutes uptake time",
        },
        {
            "department": "Neurology",
            "name": "MRI Brain",
            "default_contrast_type": "No contrast",
            "default_slice_thickness": "Standard MRI protocol",
            "default_timing": "Multiplanar brain sequences",
        },
        {
            "department": "General Medicine",
            "name": "CT Abdomen",
            "default_contrast_type": "IV contrast",
            "default_slice_thickness": "1 mm",
            "default_timing": "Portal venous phase",
        },
    ]

    for test in tests:
        TestType.objects.get_or_create(
            department=departments[test["department"]],
            name=test["name"],
            defaults={
                "default_contrast_type": test["default_contrast_type"],
                "default_slice_thickness": test["default_slice_thickness"],
                "default_timing": test["default_timing"],
            },
        )


def remove_initial_data(apps, schema_editor):
    Department = apps.get_model("referrals", "Department")

    Department.objects.filter(
        name__in=[
            "Cardiology",
            "Orthopedics",
            "Oncology",
            "Neurology",
            "General Medicine",
        ]
    ).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("referrals", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(
            seed_initial_data,
            remove_initial_data,
        ),
    ]