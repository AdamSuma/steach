# Generated by Django 2.2 on 2020-01-11 13:41

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0016_grade'),
    ]

    operations = [
        migrations.AlterField(
            model_name='grade',
            name='actual_value',
            field=models.FloatField(blank=True, null=True, validators=[django.core.validators.MaxValueValidator(10)]),
        ),
    ]
