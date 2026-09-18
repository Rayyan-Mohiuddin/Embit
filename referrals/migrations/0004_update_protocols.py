from django.db import migrations


def update_protocols(apps, schema_editor):
    TestType = apps.get_model("referrals", "TestType")

    protocols = {
        "CT Coronary Angiography": """
Contrast: IV contrast
Slice thickness: 0.5 mm
Timing: ECG-gated acquisition
""".strip(),

        "Echocardiogram": """
Standard comprehensive transthoracic echocardiography protocol.

Views:
- Parasternal long-axis
- Parasternal short-axis
- Apical 4-chamber
- Apical 2-chamber
- Apical 3-chamber
- Apical 5-chamber
- Subcostal views

Assessment:
- LV size and systolic function
- RV size and function
- Atrial size
- Valvular assessment
- Pericardium
- Relevant Doppler measurements
- LV ejection fraction
""".strip(),

        "X-Ray Knee": """
Standard knee radiography.

Views:
- AP
- Lateral

Additional views as clinically indicated.
""".strip(),

        "MRI Knee": """
Standard MRI knee protocol.

Sequences:
- Multiplanar proton-density imaging
- T1-weighted imaging
- T2/STIR or fat-suppressed sequences

Contrast only when clinically indicated.
""".strip(),

        "CT Chest": """
Contrast: IV contrast
Slice thickness: 1 mm
Timing: 70 seconds after contrast injection

Acquire standard pre-operative chest CT views.
""".strip(),

        "PET-CT": """
Tracer: FDG

Standard PET-CT acquisition protocol.
Allow approximately 60 minutes uptake time
before imaging, according to local protocol.
""".strip(),

        "MRI Brain": """
Standard MRI brain protocol.

Sequences:
- T1
- T2
- FLAIR
- DWI
- ADC
- Susceptibility-sensitive sequence

Contrast when clinically indicated.
""".strip(),

        "CT Abdomen": """
Contrast: IV contrast
Slice thickness: 1 mm
Timing: Portal venous phase

Standard CT abdomen acquisition.
""".strip(),
    }

    for test_name, protocol in protocols.items():
        TestType.objects.filter(
            name=test_name
        ).update(
            default_protocol=protocol
        )


class Migration(migrations.Migration):

    dependencies = [
        ("referrals", "0003_flexible_protocol"),
    ]

    operations = [
        migrations.RunPython(
            update_protocols,
            migrations.RunPython.noop,
        ),
    ]