# Generated by Django 2.2 on 2020-03-12 08:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0031_auto_20200312_0835'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mainclass',
            name='name',
            field=models.CharField(max_length=8),
        ),
    ]
