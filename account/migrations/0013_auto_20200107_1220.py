# Generated by Django 2.2 on 2020-01-07 12:20

import account.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0012_lesson_date_added'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lesson',
            name='pdf',
            field=models.FileField(blank=True, null=True, upload_to=account.models.Lesson.pdf_upload_path),
        ),
    ]
