# Generated by Django 5.0.6 on 2024-08-04 15:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0014_account_job"),
    ]

    operations = [
        migrations.AddField(
            model_name="post",
            name="category",
            field=models.CharField(
                choices=[
                    ("تکنولوژی", "تکنولوژی"),
                    ("هوش مصنوعی", "هوش مصنوعی"),
                    ("برنامه نویسی", "برنامه نویسی"),
                    ("بلاکچین", "بلاکچین"),
                    ("سایر", "سایر"),
                ],
                default="سایر",
                max_length=20,
            ),
        ),
    ]
