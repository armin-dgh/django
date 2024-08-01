# Generated by Django 5.0.6 on 2024-07-18 05:26

import django.db.models.deletion
import django_jalali.db.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_rename_readinf_time_post_reading_time'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CreatPost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=250, verbose_name='عنوان')),
                ('description', models.TextField(verbose_name='توضیحات')),
                ('reading_time', models.PositiveIntegerField(verbose_name='زمان مطالعه')),
                ('create', django_jalali.db.models.jDateTimeField(auto_now_add=True)),
                ('update', django_jalali.db.models.jDateTimeField(auto_now=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'ایجاد پست',
                'ordering': ['-create'],
                'indexes': [models.Index(fields=['-create'], name='blog_creatp_create_aa7a0e_idx')],
            },
        ),
    ]