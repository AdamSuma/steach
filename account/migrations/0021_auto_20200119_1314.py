# Generated by Django 2.2 on 2020-01-19 13:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0020_auto_20200119_1307'),
    ]

    operations = [
        migrations.RenameField(
            model_name='grade',
            old_name='subclass',
            new_name='sub_class',
        ),
    ]
