# Generated by Django 4.2.3 on 2023-07-27 10:40

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("rbac_app", "0002_customuser_token_userapiaccess_tokens"),
    ]

    operations = [
        migrations.RenameField(
            model_name="customuser",
            old_name="token",
            new_name="tokens",
        ),
    ]