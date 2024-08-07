# Generated by Django 5.0.6 on 2024-07-27 18:02

import django_resized.forms
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0010_alter_image_options_alter_image_image_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='image_file',
            field=django_resized.forms.ResizedImageField(crop=None, force_format=None, keep_meta=True, quality=70, scale=None, size=[500, 500], upload_to='image_path'),
        ),
    ]
