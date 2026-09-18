from django.db import migrations, models


def move_protocol_data(apps, schema_editor):
    TestType = apps.get_model("referrals", "TestType")

    for test in TestType.objects.all():
        parts = []

        if test.default_contrast_type:
            parts.append(
                f"Contrast: {test.default_contrast_type}"
            )

        if test.default_slice_thickness:
            parts.append(
                f"Slice thickness: {test.default_slice_thickness}"
            )

        if test.default_timing:
            parts.append(
                f"Timing: {test.default_timing}"
            )

        test.default_protocol = "\n".join(parts)
        test.save(update_fields=["default_protocol"])


class Migration(migrations.Migration):

    dependencies = [
        ("referrals", "0002_seed_initial_data"),
    ]

    operations = [
        migrations.AddField(
            model_name="testtype",
            name="default_protocol",
            field=models.TextField(
                blank=True,
                help_text="Default protocol shown when creating a referral.",
            ),
        ),

        migrations.RunPython(
            move_protocol_data,
            migrations.RunPython.noop,
        ),

        migrations.RemoveField(
            model_name="testtype",
            name="default_contrast_type",
        ),

        migrations.RemoveField(
            model_name="testtype",
            name="default_slice_thickness",
        ),

        migrations.RemoveField(
            model_name="testtype",
            name="default_timing",
        ),
    ]