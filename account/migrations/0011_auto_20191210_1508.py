# Generated by Django 2.2 on 2019-12-10 15:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0010_auto_20191127_1631'),
    ]

    operations = [
        migrations.RenameField(
            model_name='lesson',
            old_name='subclass',
            new_name='sub_class',
        ),
    ]
