from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="userprofile",
            name="otp_enabled",
            field=models.BooleanField(
                default=False,
                help_text="Require OTP verification for master module",
            ),
        ),
        migrations.AddField(
            model_name="userprofile",
            name="otp_last_verified",
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="userprofile",
            name="otp_secret",
            field=models.CharField(
                blank=True,
                help_text="Base32 secret for authenticator apps",
                max_length=32,
            ),
        ),
    ]
