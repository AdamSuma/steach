# Generated by Django 2.2 on 2020-03-12 08:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0029_auto_20200302_1548'),
    ]

    operations = [
        migrations.RenameField(
            model_name='mainclass',
            old_name='year',
            new_name='semester',
        ),
    ]
