# Generated by Django 5.0.6 on 2024-07-15 18:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_post_readinf_time'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='readinf_time',
            new_name='reading_time',
        ),
    ]
